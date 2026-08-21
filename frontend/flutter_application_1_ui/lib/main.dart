import 'package:flutter/material.dart';

void main() {
  runApp(const HarvestNexusApp());
}

// ============================================================
// HARVEST NEXUS APP
// ============================================================

class HarvestNexusApp extends StatefulWidget {
  const HarvestNexusApp({super.key});

  @override
  State<HarvestNexusApp> createState() => _HarvestNexusAppState();
}

class _HarvestNexusAppState extends State<HarvestNexusApp> {
  bool hindi = false;

  void toggleLanguage() {
    setState(() {
      hindi = !hindi;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Harvest Nexus',
      theme: ThemeData(
        useMaterial3: true,
        fontFamily: 'sans',
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2E7D32),
        ),
        scaffoldBackgroundColor: const Color(0xFFF5F8F3),
      ),
      home: LoginScreen(
        hindi: hindi,
        onLanguageChanged: toggleLanguage,
      ),
    );
  }
}

// ============================================================
// TRANSLATIONS
// ============================================================

class T {
  static String get(String key, bool hindi) {
    final Map<String, List<String>> words = {
      'appName': ['Fasal Setu', 'फसल सेतु'],
      'welcome': ['Welcome, Farmer', 'स्वागत है, किसान'],
      'login': ['Login', 'लॉगिन'],
      'register': ['Register', 'रजिस्टर करें'],
      'phone': ['Phone Number', 'फ़ोन नंबर'],
      'password': ['Password', 'पासवर्ड'],
      'continue': ['Continue', 'जारी रखें'],
      'dashboard': ['Dashboard', 'डैशबोर्ड'],
      'disease': ['Disease Diagnosis', 'रोग पहचान'],
      'market': ['Market', 'बाज़ार'],
      'buyers': ['Buyers', 'खरीदार'],
      'logistics': ['Logistics', 'परिवहन'],
      'profile': ['Profile', 'प्रोफ़ाइल'],
      'notifications': ['Notifications', 'सूचनाएँ'],
      'chatbot': ['AI Assistant', 'AI सहायक'],
      'community': ['Community', 'किसान समुदाय'],
      'healthScore': ['Farm Health Score', 'खेत स्वास्थ्य स्कोर'],
      'todaysPlan': ["Today's Action Plan", 'आज की कार्य योजना'],
      'highPriority': ['HIGH PRIORITY', 'उच्च प्राथमिकता'],
      'mediumPriority': ['MEDIUM PRIORITY', 'मध्यम प्राथमिकता'],
      'opportunity': ['OPPORTUNITY', 'अवसर'],
      'treatBlight': ['Treat Early Blight', 'अर्ली ब्लाइट का उपचार करें'],
      'irrigate': ['Irrigate within 24 hours', '24 घंटे के अंदर सिंचाई करें'],
      'rising': ['Market prices are rising', 'बाज़ार भाव बढ़ रहे हैं'],
      'selling': ['Consider selling within window', 'उचित समय में बेचने पर विचार करें'],
      'weather': ['Weather', 'मौसम'],
      'temperature': ['Temperature', 'तापमान'],
      'humidity': ['Humidity', 'नमी'],
      'soilMoisture': ['Soil Moisture', 'मिट्टी की नमी'],
      'npk': ['NPK Values', 'NPK मान'],
      'crop': ['Crop', 'फसल'],
      'tomato': ['Tomato', 'टमाटर'],
      'diseaseDetected': ['Disease Detected', 'रोग पाया गया'],
      'earlyBlight': ['Early Blight', 'अर्ली ब्लाइट'],
      'confidence': ['Confidence', 'विश्वास स्तर'],
      'scanLeaf': ['Scan Leaf', 'पत्ती स्कैन करें'],
      'uploadLeaf': ['Upload Leaf Image', 'पत्ती की तस्वीर अपलोड करें'],
      'currentPrice': ['Current Price', 'वर्तमान भाव'],
      'trend': ['Trend', 'रुझान'],
      'demand': ['Demand', 'मांग'],
      'nearbyBuyers': ['Nearby Buyers', 'नज़दीकी खरीदार'],
      'nearbyMandis': ['Nearby Mandis', 'नज़दीकी मंडियाँ'],
      'contact': ['Contact', 'संपर्क करें'],
      'transport': ['Transport', 'परिवहन'],
      'availableVehicles': ['Available Vehicles', 'उपलब्ध वाहन'],
      'askAI': ['Ask AI Assistant', 'AI सहायक से पूछें'],
      'communityTitle': ['Farmer Community', 'किसान समुदाय'],
      'share': ['Share', 'साझा करें'],
      'save': ['Save', 'सहेजें'],
      'logout': ['Logout', 'लॉग आउट'],
      'farmProfile': ['Farm Profile', 'खेत प्रोफ़ाइल'],
      'myProfile': ['My Profile', 'मेरी प्रोफ़ाइल'],
      'location': ['Location', 'स्थान'],
      'landSize': ['Land Size', 'भूमि क्षेत्र'],
      'mainCrop': ['Main Crop', 'मुख्य फसल'],
    };

    return words[key]?[hindi ? 1 : 0] ?? key;
  }
}

// ============================================================
// COMMON WIDGETS
// ============================================================

class LanguageButton extends StatelessWidget {
  final bool hindi;
  final VoidCallback onChanged;

  const LanguageButton({
    super.key,
    required this.hindi,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return OutlinedButton(
      onPressed: onChanged,
      style: OutlinedButton.styleFrom(
        foregroundColor: const Color(0xFF2E7D32),
        side: const BorderSide(color: Color(0xFF2E7D32)),
      ),
      child: Text(hindi ? 'हिंदी' : 'EN'),
    );
  }
}

class SectionTitle extends StatelessWidget {
  final String title;
  final VoidCallback? onTap;

  const SectionTitle({
    super.key,
    required this.title,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Color(0xFF1B4332),
          ),
        ),
        if (onTap != null)
          TextButton(
            onPressed: onTap,
            child: const Text('View all'),
          ),
      ],
    );
  }
}

// ============================================================
// LOGIN
// ============================================================

class LoginScreen extends StatelessWidget {
  final bool hindi;
  final VoidCallback onLanguageChanged;

  const LoginScreen({
    super.key,
    required this.hindi,
    required this.onLanguageChanged,
  });

  @override
  Widget build(BuildContext context) {
    final phoneController = TextEditingController();
    final passwordController = TextEditingController();

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const SizedBox(height: 35),

              // Farmer illustration
              Container(
                height: 130,
                width: 130,
                decoration: BoxDecoration(
                  color: const Color(0xFFE8F5E9),
                  shape: BoxShape.circle,
                ),
                child: const Center(
                  child: Text(
                    '👨‍🌾',
                    style: TextStyle(fontSize: 70),
                  ),
                ),
              ),

              const SizedBox(height: 20),

              Text(
                T.get('appName', hindi),
                style: const TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF1B5E20),
                ),
              ),

              const SizedBox(height: 8),

              Text(
                T.get('welcome', hindi),
                style: const TextStyle(
                  fontSize: 18,
                  color: Colors.grey,
                ),
              ),

              const SizedBox(height: 35),

              Align(
                alignment: Alignment.centerRight,
                child: LanguageButton(
                  hindi: hindi,
                  onChanged: onLanguageChanged,
                ),
              ),

              const SizedBox(height: 20),

              TextField(
                controller: phoneController,
                keyboardType: TextInputType.phone,
                decoration: InputDecoration(
                  labelText: T.get('phone', hindi),
                  prefixIcon: const Icon(Icons.phone),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(14),
                  ),
                ),
              ),

              const SizedBox(height: 15),

              TextField(
                controller: passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: T.get('password', hindi),
                  prefixIcon: const Icon(Icons.lock),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(14),
                  ),
                ),
              ),

              const SizedBox(height: 25),

              SizedBox(
                width: double.infinity,
                height: 55,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const MainNavigation(),
                      ),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF2E7D32),
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14),
                    ),
                  ),
                  child: Text(
                    T.get('login', hindi),
                    style: const TextStyle(fontSize: 17),
                  ),
                ),
              ),

              const SizedBox(height: 12),

              TextButton(
                onPressed: () {},
                child: Text(T.get('register', hindi)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// ============================================================
// MAIN NAVIGATION
// ============================================================

// ============================================================
// MAIN NAVIGATION
// ============================================================

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int selectedIndex = 0;
  bool hindi = false;

  void toggleLanguage() {
    setState(() {
      hindi = !hindi;
    });
  }

  @override
  Widget build(BuildContext context) {
    final screens = [
      DashboardScreen(
        hindi: hindi,
        onLanguageChanged: toggleLanguage,
      ),
      DiseaseScreen(hindi: hindi),
      MarketScreen(hindi: hindi),
      CommunityScreen(hindi: hindi),
      ProfileScreen(hindi: hindi),
    ];

    return Scaffold(
      body: IndexedStack(
        index: selectedIndex,
        children: screens,
      ),

      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        onDestinationSelected: (index) {
          setState(() {
            selectedIndex = index;
          });
        },
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.home_outlined),
            selectedIcon: const Icon(Icons.home),
            label: T.get('dashboard', hindi),
          ),
          NavigationDestination(
            icon: const Icon(Icons.eco_outlined),
            selectedIcon: const Icon(Icons.eco),
            label: T.get('disease', hindi),
          ),
          NavigationDestination(
            icon: const Icon(Icons.storefront_outlined),
            selectedIcon: const Icon(Icons.storefront),
            label: T.get('market', hindi),
          ),
          NavigationDestination(
            icon: const Icon(Icons.groups_outlined),
            selectedIcon: const Icon(Icons.groups),
            label: T.get('community', hindi),
          ),
          NavigationDestination(
            icon: const Icon(Icons.person_outline),
            selectedIcon: const Icon(Icons.person),
            label: T.get('profile', hindi),
          ),
        ],
      ),
    );
  }
}

// ============================================================
// DASHBOARD
// ============================================================

class DashboardScreen extends StatelessWidget {
  final bool hindi;
  final VoidCallback onLanguageChanged;

  const DashboardScreen({
    super.key,
    required this.hindi,
    required this.onLanguageChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          T.get('appName', hindi),
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: Colors.transparent,
        actions: [
          LanguageButton(
            hindi: hindi,
            onChanged: onLanguageChanged,
          ),
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => NotificationsScreen(hindi: hindi),
                ),
              );
            },
          ),
        ],
      ),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            // Greeting
            Text(
              '${T.get('welcome', hindi)} 👋',
              style: const TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.bold,
                color: Color(0xFF1B4332),
              ),
            ),

            const SizedBox(height: 5),

            Text(
              '${T.get('crop', hindi)}: ${T.get('tomato', hindi)}',
              style: const TextStyle(
                color: Colors.grey,
                fontSize: 16,
              ),
            ),

            const SizedBox(height: 20),

            // Farm Health
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [
                    Color(0xFF2E7D32),
                    Color(0xFF43A047),
                  ],
                ),
                borderRadius: BorderRadius.circular(22),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          T.get('healthScore', hindi),
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                          ),
                        ),
                        const SizedBox(height: 8),
                        const Text(
                          '81/100',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 40,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const Text(
                          'Good condition',
                          style: TextStyle(
                            color: Colors.white70,
                          ),
                        ),
                      ],
                    ),
                  ),

                  SizedBox(
                    width: 85,
                    height: 85,
                    child: Stack(
                      alignment: Alignment.center,
                      children: [
                        CircularProgressIndicator(
                          value: .81,
                          strokeWidth: 9,
                          backgroundColor: Colors.white24,
                          color: Colors.white,
                        ),
                        const Text(
                          '81%',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 25),

            // Today's Action Plan
            SectionTitle(
              title: T.get('todaysPlan', hindi),
            ),

            const SizedBox(height: 10),

            ActionCard(
              icon: '🔴',
              title: T.get('highPriority', hindi),
              subtitle: T.get('treatBlight', hindi),
            ),

            ActionCard(
              icon: '🟠',
              title: T.get('mediumPriority', hindi),
              subtitle: T.get('irrigate', hindi),
            ),

            ActionCard(
              icon: '🟢',
              title: T.get('opportunity', hindi),
              subtitle:
                  '${T.get('rising', hindi)}\n${T.get('selling', hindi)}',
            ),

            const SizedBox(height: 20),

            // Weather + soil
            Row(
              children: [
                Expanded(
                  child: InfoCard(
                    icon: Icons.thermostat,
                    title: T.get('temperature', hindi),
                    value: '31°C',
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: InfoCard(
                    icon: Icons.water_drop,
                    title: T.get('humidity', hindi),
                    value: '78%',
                  ),
                ),
              ],
            ),

            const SizedBox(height: 10),

            Row(
              children: [
                Expanded(
                  child: InfoCard(
                    icon: Icons.grass,
                    title: T.get('soilMoisture', hindi),
                    value: '18%',
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: InfoCard(
                    icon: Icons.science,
                    title: T.get('npk', hindi),
                    value: 'N 42',
                  ),
                ),
              ],
            ),

            const SizedBox(height: 25),

            SectionTitle(
              title: T.get('disease', hindi),
            ),

            const SizedBox(height: 10),

            DiseaseSummaryCard(hindi: hindi),

            const SizedBox(height: 25),

            SectionTitle(
              title: T.get('market', hindi),
            ),

            const SizedBox(height: 10),

            MarketSummaryCard(hindi: hindi),

            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }
}

// ============================================================
// ACTION CARD
// ============================================================

class ActionCard extends StatelessWidget {
  final String icon;
  final String title;
  final String subtitle;

  const ActionCard({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      elevation: 0,
      child: ListTile(
        leading: Text(
          icon,
          style: const TextStyle(fontSize: 26),
        ),
        title: Text(
          title,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 13,
          ),
        ),
        subtitle: Text(subtitle),
      ),
    );
  }
}

// ============================================================
// INFO CARD
// ============================================================

class InfoCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;

  const InfoCard({
    super.key,
    required this.icon,
    required this.title,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      child: Padding(
        padding: const EdgeInsets.all(15),
        child: Column(
          children: [
            Icon(
              icon,
              color: const Color(0xFF2E7D32),
              size: 30,
            ),
            const SizedBox(height: 8),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 12,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              value,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================
// DISEASE SUMMARY
// ============================================================

class DiseaseSummaryCard extends StatelessWidget {
  final bool hindi;

  const DiseaseSummaryCard({
    super.key,
    required this.hindi,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Container(
              height: 70,
              width: 70,
              decoration: BoxDecoration(
                color: Colors.red.shade50,
                borderRadius: BorderRadius.circular(15),
              ),
              child: const Center(
                child: Text(
                  '🍅',
                  style: TextStyle(fontSize: 38),
                ),
              ),
            ),

            const SizedBox(width: 15),

            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    T.get('diseaseDetected', hindi),
                    style: const TextStyle(
                      color: Colors.grey,
                    ),
                  ),
                  Text(
                    T.get('earlyBlight', hindi),
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    '${T.get('confidence', hindi)}: 92%',
                    style: const TextStyle(
                      color: Colors.red,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================
// MARKET SUMMARY
// ============================================================

class MarketSummaryCard extends StatelessWidget {
  final bool hindi;

  const MarketSummaryCard({
    super.key,
    required this.hindi,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Row(
              children: [
                const Icon(
                  Icons.trending_up,
                  color: Colors.green,
                  size: 35,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    '${T.get('tomato', hindi)} Market',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                const Text(
                  '₹2300/q',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.green,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            LinearProgressIndicator(
              value: .78,
              minHeight: 7,
              borderRadius: BorderRadius.circular(10),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================
// DISEASE SCREEN
// ============================================================

class DiseaseScreen extends StatelessWidget {
  final bool hindi;

  const DiseaseScreen({
    super.key,
    required this.hindi,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(T.get('disease', hindi)),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [

            Container(
              height: 230,
              width: double.infinity,
              decoration: BoxDecoration(
                color: const Color(0xFFE8F5E9),
                borderRadius: BorderRadius.circular(25),
                border: Border.all(
                  color: Colors.green.shade200,
                ),
              ),
              child: const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.camera_alt_outlined,
                    size: 70,
                    color: Color(0xFF2E7D32),
                  ),
                  SizedBox(height: 15),
                  Text(
                    '📷',
                    style: TextStyle(fontSize: 35),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton.icon(
                onPressed: () {
                  showDialog(
                    context: context,
                    builder: (_) => AlertDialog(
                      title: Text(T.get('diseaseDetected', hindi)),
                      content: Text(
                        '${T.get('earlyBlight', hindi)}\n\n'
                        '${T.get('confidence', hindi)}: 92%\n'
                        'Severity: Moderate',
                      ),
                      actions: [
                        TextButton(
                          onPressed: () => Navigator.pop(context),
                          child: const Text('OK'),
                        ),
                      ],
                    ),
                  );
                },
                icon: const Icon(Icons.camera_alt),
                label: Text(T.get('scanLeaf', hindi)),
              ),
            ),

            const SizedBox(height: 12),

            OutlinedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.upload),
              label: Text(T.get('uploadLeaf', hindi)),
            ),

            const SizedBox(height: 30),

            Card(
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      T.get('diseaseDetected', hindi),
                      style: const TextStyle(
                        color: Colors.grey,
                      ),
                    ),
                    const SizedBox(height: 5),
                    Text(
                      T.get('earlyBlight', hindi),
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 15),
                    const LinearProgressIndicator(
                      value: .92,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '${T.get('confidence', hindi)}: 92%',
                    ),
                    const SizedBox(height: 20),
                    const Text(
                      'Recommended treatment will appear here '
                      'after Oracle AI prediction is connected.',
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================
// MARKET SCREEN
// ============================================================

class MarketScreen extends StatelessWidget {
  final bool hindi;

  const MarketScreen({
    super.key,
    required this.hindi,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(T.get('market', hindi)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [

          Card(
            color: const Color(0xFFE8F5E9),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    T.get('tomato', hindi),
                    style: const TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    '₹2300 / quintal',
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      const Icon(
                        Icons.trending_up,
                        color: Colors.green,
                      ),
                      const SizedBox(width: 5),
                      Text(
                        T.get('rising', hindi),
                        style: const TextStyle(
                          color: Colors.green,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(height: 20),

          Text(
            T.get('nearbyMandis', hindi),
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 10),

          MandiCard(
            name: 'Azadpur Mandi',
            distance: '18 km',
            price: '₹2300/q',
          ),

          MandiCard(
            name: 'Local Agricultural Market',
            distance: '9 km',
            price: '₹2180/q',
          ),

          const SizedBox(height: 25),

          Text(
            T.get('nearbyBuyers', hindi),
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 10),

          BuyerCard(
            name: 'Fresh Harvest Traders',
            location: 'Nearby',
          ),

          BuyerCard(
            name: 'Green Valley Foods',
            location: '25 km',
          ),
        ],
      ),
    );
  }
}

class MandiCard extends StatelessWidget {
  final String name;
  final String distance;
  final String price;

  const MandiCard({
    super.key,
    required this.name,
    required this.distance,
    required this.price,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: const CircleAvatar(
          child: Icon(Icons.store),
        ),
        title: Text(name),
        subtitle: Text(distance),
        trailing: Text(
          price,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            color: Colors.green,
          ),
        ),
      ),
    );
  }
}

class BuyerCard extends StatelessWidget {
  final String name;
  final String location;

  const BuyerCard({
    super.key,
    required this.name,
    required this.location,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: const CircleAvatar(
          child: Icon(Icons.person),
        ),
        title: Text(name),
        subtitle: Text(location),
        trailing: ElevatedButton(
          onPressed: () {},
          child: const Text('Contact'),
        ),
      ),
    );
  }
}

// ============================================================
// LOGISTICS SCREEN
// ============================================================

class LogisticsScreen extends StatelessWidget {
  final bool hindi;

  const LogisticsScreen({
    super.key,
    required this.hindi,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(T.get('logistics', hindi)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [

          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  const Icon(
                    Icons.local_shipping,
                    size: 60,
                    color: Color(0xFF2E7D32),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    T.get('availableVehicles', hindi),
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ),

          VehicleCard(
            type: 'Mini Truck',
            capacity: '1 Ton',
            distance: 'Available nearby',
          ),

          VehicleCard(
            type: 'Tractor Trolley',
            capacity: '2 Ton',
            distance: 'Available',
          ),

          VehicleCard(
            type: 'Large Truck',
            capacity: '5 Ton',
            distance: '25 km away',
          ),
        ],
      ),
    );
  }
}

class VehicleCard extends StatelessWidget {
  final String type;
  final String capacity;
  final String distance;

  const VehicleCard({
    super.key,
    required this.type,
    required this.capacity,
    required this.distance,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: const Icon(
          Icons.local_shipping,
          color: Color(0xFF2E7D32),
        ),
        title: Text(
          type,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
        subtitle: Text('$capacity • $distance'),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
      ),
    );
  }
}

// ============================================================
// COMMUNITY
// ============================================================

class CommunityScreen extends StatelessWidget {
  final bool hindi;

  const CommunityScreen({
    super.key,
    required this.hindi,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(T.get('communityTitle', hindi)),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [

          CommunityPost(
            farmer: 'Ramesh Kumar',
            text:
                'My tomato crop has started showing yellow spots. '
                'Has anyone faced this problem?',
            likes: 24,
          ),

          CommunityPost(
            farmer: 'Suresh Singh',
            text:
                'Market prices are rising this week. '
                'Check your nearby mandi before selling.',
            likes: 41,
          ),

          CommunityPost(
            farmer: 'Amit Sharma',
            text:
                'What fertilizer are you using for your tomato crop?',
            likes: 15,
          ),
        ],
      ),
    );
  }
}

class CommunityPost extends StatelessWidget {
  final String farmer;
  final String text;
  final int likes;

  const CommunityPost({
    super.key,
    required this.farmer,
    required this.text,
    required this.likes,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 15),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            Row(
              children: [
                const CircleAvatar(
                  child: Icon(Icons.person),
                ),
                const SizedBox(width: 10),
                Text(
                  farmer,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 15),

            Text(
              text,
              style: const TextStyle(fontSize: 16),
            ),

            const SizedBox(height: 15),

            Row(
              children: [
                const Icon(Icons.favorite_border),
                const SizedBox(width: 5),
                Text('$likes'),
                const SizedBox(width: 20),
                const Icon(Icons.comment_outlined),
                const SizedBox(width: 5),
                const Text('Comment'),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================
// NOTIFICATIONS
// ============================================================

class NotificationsScreen extends StatelessWidget {
  final bool hindi;

  const NotificationsScreen({
    super.key,
    required this.hindi,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(T.get('notifications', hindi)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [

          NotificationCard(
            icon: Icons.warning_amber,
            title: T.get('highPriority', hindi),
            text: T.get('treatBlight', hindi),
          ),

          NotificationCard(
            icon: Icons.water_drop,
            title: T.get('mediumPriority', hindi),
            text: T.get('irrigate', hindi),
          ),

          NotificationCard(
            icon: Icons.trending_up,
            title: T.get('opportunity', hindi),
            text: T.get('rising', hindi),
          ),
        ],
      ),
    );
  }
}

class NotificationCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String text;

  const NotificationCard({
    super.key,
    required this.icon,
    required this.title,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(
          icon,
          color: const Color(0xFF2E7D32),
        ),
        title: Text(
          title,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
        subtitle: Text(text),
      ),
    );
  }
}

// ============================================================
// PROFILE
// ============================================================

class ProfileScreen extends StatelessWidget {
  final bool hindi;

  const ProfileScreen({
    super.key,
    required this.hindi,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(T.get('profile', hindi)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [

          const CircleAvatar(
            radius: 50,
            child: Text(
              '👨‍🌾',
              style: TextStyle(fontSize: 45),
            ),
          ),

          const SizedBox(height: 15),

          const Center(
            child: Text(
              'Rajesh Kumar',
              style: TextStyle(
                fontSize: 23,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),

          const SizedBox(height: 25),

          ProfileItem(
            icon: Icons.person,
            title: T.get('myProfile', hindi),
          ),

          ProfileItem(
            icon: Icons.agriculture,
            title: T.get('farmProfile', hindi),
          ),

          ProfileItem(
            icon: Icons.location_on,
            title: '${T.get('location', hindi)}: Haryana',
          ),

          ProfileItem(
            icon: Icons.landscape,
            title: '${T.get('landSize', hindi)}: 5 Acres',
          ),

          ProfileItem(
            icon: Icons.eco,
            title: '${T.get('mainCrop', hindi)}: ${T.get('tomato', hindi)}',
          ),

          const SizedBox(height: 20),

          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: Text(T.get('logout', hindi)),
            onTap: () {},
          ),
        ],
      ),
    );
  }
}

class ProfileItem extends StatelessWidget {
  final IconData icon;
  final String title;

  const ProfileItem({
    super.key,
    required this.icon,
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(
          icon,
          color: const Color(0xFF2E7D32),
        ),
        title: Text(title),
        trailing: const Icon(Icons.arrow_forward_ios, size: 15),
      ),
    );
  }
}