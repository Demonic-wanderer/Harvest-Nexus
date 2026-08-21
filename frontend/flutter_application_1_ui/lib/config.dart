class AppConfig {
  static const apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://127.0.0.1:5000',
  );

  static const oracleBaseUrl = String.fromEnvironment(
    'ORACLE_BASE_URL',
    defaultValue: 'http://127.0.0.1:8001',
  );

  // Helper for dynamic local IP testing (e.g. Android Emulator uses 10.0.2.2)
  static String resolveUrl(String url) {
    return url;
  }
}

