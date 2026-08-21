import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../api/forge_api.dart';

class SessionController extends ChangeNotifier {
  SessionController({ForgeApi? api}) : _api = api ?? ForgeApi();

  final ForgeApi _api;

  bool restoring = true;
  bool busy = false;
  String? error;
  String? token;
  Map<String, dynamic>? user;
  Map<String, dynamic>? farm;
  Map<String, dynamic>? crop;
  Map<String, dynamic>? advisory;
  Map<String, dynamic>? market;
  Map<String, dynamic>? weather;
  Map<String, dynamic>? disease;
  Map<String, dynamic>? scanResult;
  List<dynamic> buyers = [];
  List<dynamic> mandis = [];

  bool get isLoggedIn => token != null && token!.isNotEmpty;

  int get healthScore {
    final raw = advisory?['farm_health_score'];
    if (raw is num) return raw.round();
    return 0;
  }

  Future<void> restore() async {
    final prefs = await SharedPreferences.getInstance();
    token = prefs.getString('token');
    final rawUser = prefs.getString('user');
    if (rawUser != null && rawUser.isNotEmpty) {
      user = Map<String, dynamic>.from(jsonDecode(rawUser) as Map);
    }
    restoring = false;
    notifyListeners();
    if (isLoggedIn) {
      await refreshDashboard();
    }
  }

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    if (token == null) {
      await prefs.remove('token');
      await prefs.remove('user');
      return;
    }
    await prefs.setString('token', token!);
    await prefs.setString('user', jsonEncode(user ?? {}));
  }

  Future<bool> login(String identifier, String password) async {
    busy = true;
    error = null;
    notifyListeners();
    try {
      final data = await _api.login(identifier: identifier, password: password);
      token = data['token'] as String?;
      user = Map<String, dynamic>.from(data['user'] as Map);
      await _persist();
      await refreshDashboard();
      return true;
    } catch (err) {
      error = err.toString();
      return false;
    } finally {
      busy = false;
      notifyListeners();
    }
  }

  Future<bool> register({
    required String name,
    required String email,
    required String phone,
    required String password,
  }) async {
    busy = true;
    error = null;
    notifyListeners();
    try {
      await _api.register(name: name, email: email, phone: phone, password: password);
      return login(email, password);
    } catch (err) {
      error = err.toString();
      busy = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    token = null;
    user = null;
    farm = null;
    crop = null;
    advisory = null;
    market = null;
    weather = null;
    disease = null;
    scanResult = null;
    buyers = [];
    mandis = [];
    await _persist();
    notifyListeners();
  }

  Future<void> refreshDashboard() async {
    if (!isLoggedIn || user == null) return;
    final userId = user!['id']?.toString();
    if (userId == null) return;
    try {
      final profile = await _api.get('/api/farmer/$userId', token: token);
      user = Map<String, dynamic>.from(profile['user'] as Map? ?? user!);
      final farmsData = await _api.get('/api/farmer/$userId/farms', token: token);
      final farms = List<dynamic>.from(farmsData['farms'] ?? const []);
      farm = farms.isNotEmpty ? Map<String, dynamic>.from(farms.first as Map) : null;
      if (farm != null) {
        final farmId = farm!['id'].toString();
        final cropsData = await _api.get('/api/crop/farm/$farmId', token: token);
        final crops = List<dynamic>.from(cropsData['crops'] ?? const []);
        crop = crops.isNotEmpty ? Map<String, dynamic>.from(crops.first as Map) : null;
        final latest = await _api.get('/api/advisory/latest/$farmId', token: token);
        final latestMap = latest['latest'];
        advisory = latestMap is Map ? Map<String, dynamic>.from(latestMap) : null;
      }
      final region = farm?['location']?.toString() ?? 'Madhya Pradesh';
      final cropName = crop?['crop_name']?.toString() ?? 'Tomato';
      try {
        final marketData = await _api.get(
          '/api/market/search',
          token: token,
          query: {'crop': cropName, 'region': region},
        );
        final payload = marketData['data'];
        market = payload is Map ? Map<String, dynamic>.from(payload) : null;
      } catch (_) {
        market = null;
      }
      try {
        buyers = List<dynamic>.from(
          (await _api.get(
            '/api/buyer/crop/$cropName',
            token: token,
            query: {'location': region},
          ))['buyers'] ??
              const [],
        );
      } catch (_) {
        buyers = [];
      }
      try {
        mandis = List<dynamic>.from((await _api.get('/api/mandi', token: token))['mandis'] ?? const []);
      } catch (_) {
        mandis = [];
      }
      if (crop != null) {
        try {
          final latestDisease = await _api.get('/api/disease/latest/${crop!['id']}', token: token);
          final payload = latestDisease['latest'];
          disease = payload is Map ? Map<String, dynamic>.from(payload) : null;
        } catch (_) {
          disease = null;
        }
      }
      final lat = double.tryParse('${farm?['latitude'] ?? ''}') ?? 22.7196;
      final lon = double.tryParse('${farm?['longitude'] ?? ''}') ?? 75.8577;
      weather = await _api.fetchWeather(latitude: lat, longitude: lon);
    } catch (err) {
      error = err.toString();
    }
    notifyListeners();
  }

  Future<bool> scanLeaf(String filename, List<int> bytes) async {
    busy = true;
    error = null;
    notifyListeners();
    try {
      scanResult = await _api.predictLeaf(filename, bytes);
      if (crop != null && token != null) {
        await _api.post(
          '/api/disease/predict-result',
          {
            'crop_id': crop!['id'],
            'image_url': filename,
            'disease_name': scanResult!['disease'] ?? scanResult!['display_name'],
            'confidence': scanResult!['confidence'],
            'severity': scanResult!['severity'],
          },
          token: token,
        );
        disease = scanResult;
      }
      return true;
    } catch (err) {
      error = err.toString();
      return false;
    } finally {
      busy = false;
      notifyListeners();
    }
  }
}
