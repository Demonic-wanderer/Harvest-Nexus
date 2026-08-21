import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config.dart';

class ApiException implements Exception {
  ApiException(this.message);
  final String message;

  @override
  String toString() => message;
}

class ForgeApi {
  ForgeApi({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;

  Map<String, String> _headers({String? token, bool jsonBody = true}) {
    return {
      if (jsonBody) 'Content-Type': 'application/json',
      if (token != null && token.isNotEmpty) 'Authorization': 'Bearer $token',
    };
  }

  Future<Map<String, dynamic>> _parse(http.Response response) async {
    final decoded = response.body.isEmpty ? {} : jsonDecode(response.body);
    if (decoded is! Map<String, dynamic>) {
      throw ApiException('Unexpected response from server');
    }
    if (response.statusCode >= 400 || decoded['status'] == 'error') {
      throw ApiException(decoded['message']?.toString() ?? 'Request failed');
    }
    final data = decoded['data'];
    if (data is Map<String, dynamic>) return data;
    return decoded;
  }

  Future<Map<String, dynamic>> login({
    required String identifier,
    required String password,
  }) {
    final body = identifier.contains('@')
        ? {'email': identifier.trim(), 'password': password}
        : {'phone': identifier.trim(), 'password': password};
    return post('/api/auth/login', body);
  }

  Future<Map<String, dynamic>> register({
    required String name,
    required String email,
    required String phone,
    required String password,
  }) {
    return post('/api/auth/register', {
      'name': name,
      'email': email,
      'phone': phone,
      'password': password,
      'role': 'farmer',
    });
  }

  Future<Map<String, dynamic>> get(String path, {String? token, Map<String, String>? query}) async {
    final uri = Uri.parse('${AppConfig.apiBaseUrl}$path').replace(queryParameters: query);
    final response = await _client.get(uri, headers: _headers(token: token, jsonBody: false));
    return _parse(response);
  }

  Future<Map<String, dynamic>> post(String path, Map<String, dynamic> body, {String? token}) async {
    final uri = Uri.parse('${AppConfig.apiBaseUrl}$path');
    final response = await _client.post(
      uri,
      headers: _headers(token: token),
      body: jsonEncode(body),
    );
    return _parse(response);
  }

  Future<Map<String, dynamic>> predictLeaf(String filename, List<int> bytes) async {
    final uri = Uri.parse('${AppConfig.oracleBaseUrl}/predict-upload');
    final request = http.MultipartRequest('POST', uri)
      ..files.add(http.MultipartFile.fromBytes('file', bytes, filename: filename));
    final streamed = await _client.send(request);
    final response = await http.Response.fromStream(streamed);
    if (response.statusCode >= 400) {
      throw ApiException('Oracle scan failed (${response.statusCode})');
    }
    final decoded = jsonDecode(response.body);
    if (decoded is Map<String, dynamic>) return decoded;
    throw ApiException('Unexpected Oracle response');
  }

  Future<Map<String, dynamic>> fetchWeather({
    double latitude = 22.7196,
    double longitude = 75.8577,
  }) async {
    final uri = Uri.parse('https://api.open-meteo.com/v1/forecast').replace(
      queryParameters: {
        'latitude': '$latitude',
        'longitude': '$longitude',
        'current': 'temperature_2m,relative_humidity_2m,precipitation',
        'hourly': 'precipitation_probability',
        'forecast_days': '1',
        'timezone': 'auto',
      },
    );
    final response = await _client.get(uri);
    if (response.statusCode >= 400) {
      throw ApiException('Weather request failed');
    }
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    final current = Map<String, dynamic>.from(data['current'] as Map);
    final hourly = Map<String, dynamic>.from(data['hourly'] as Map? ?? {});
    final times = List<String>.from(hourly['time'] ?? const []);
    final probs = List<dynamic>.from(hourly['precipitation_probability'] ?? const []);
    final observed = current['time']?.toString();
    var rain = 0.0;
    if (observed != null && times.isNotEmpty) {
      final hour = observed.substring(0, observed.length >= 13 ? 13 : observed.length);
      final index = times.indexWhere((stamp) => stamp.startsWith(hour));
      if (index >= 0 && index < probs.length) {
        rain = (probs[index] as num).toDouble();
      }
    }
    return {
      'temperature': current['temperature_2m'],
      'humidity': current['relative_humidity_2m'],
      'rain_probability': rain,
    };
  }
}
