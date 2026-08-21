import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Harvest Nexus',
      theme: ThemeData(
        scaffoldBackgroundColor: const Color(0xFFF7F8F3),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF238636),
        ),
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int selectedIndex = 0;

  final List<Widget> pages = const [
    DashboardPage(),
    DiseasePage(),
    MarketPage(),
    LogisticsPage(),
    ProfilePage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: pages[selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        backgroundColor: Colors.white,
        indicatorColor: const Color(0xFFDDF2DF),
        onDestinationSelected: (index) {
          setState(() {
            selectedIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.eco_outlined),
            selectedIcon: Icon(Icons.eco),
            label: 'Disease',
          ),
          NavigationDestination(
            icon: Icon(Icons.bar_chart_outlined),
            selectedIcon: Icon(Icons.bar_chart),
            label: 'Market',
          ),
          NavigationDestination(
            icon: Icon(Icons.local_shipping_outlined),
            selectedIcon: Icon(Icons.local_shipping),
            label: 'Logistics',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}

// ============================================================
// DASHBOARD
// ============================================================

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(
        child: Column(
          children: [
            // TOP HERO
            Container(
              height: 380,
              width: double.infinity,
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Color(0xFFEAF7F5),
                    Color(0xFFDCEFD9),
                  ],
                ),
              ),
              child: Stack(
                children: [
                  // Logo
                  const Positioned(
                    left: 22,
                    top: 22,
                    child: Row(
                      children: [
                        Icon(
                          Icons.eco,
                          size: 32,
                          color: Color(0xFF238636),
                        ),
                        SizedBox(width: 7),
                        Text(
                          'Harvest\nNexus',
                          style: TextStyle(
                            height: 0.9,
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF173D25),
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Notification
                  Positioned(
                    right: 20,
                    top: 20,
                    child: Container(
                      padding: const EdgeInsets.all(10),
                      decoration: const BoxDecoration(
                        color: Colors.white,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(
                        Icons.notifications_none,
                        color: Color(0xFF173D25),
                      ),
                    ),
                  ),

                  // Greeting
                  const Positioned(
                    left: 24,
                    top: 105,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Good Morning,',
                          style: TextStyle(
                            fontSize: 27,
                            color: Color(0xFF14251A),
                          ),
                        ),
                        Text(
                          'Farmer! 👋',
                          style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF238636),
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          "Let's make today a\nproductive day.",
                          style: TextStyle(
                            fontSize: 15,
                            height: 1.4,
                            color: Color(0xFF53635A),
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Farmer
                  Positioned(
                    right: -5,
                    bottom: 45,
                    child: Image.asset(
                      'assets/farmer_illustration.png',
                      height: 255,
                    ),
                  ),

                  // Health card
                  Positioned(
                    left: 18,
                    right: 18,
                    bottom: 0,
                    child: Container(
                      height: 120,
                      padding: const EdgeInsets.all(18),
                      decoration: BoxDecoration(
                        color: const Color(0xFF238636),
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: Row(
                        children: [
                          SizedBox(
                            width: 82,
                            height: 82,
                            child: Stack(
                              alignment: Alignment.center,
                              children: [
                                const CircularProgressIndicator(
                                  value: 0.81,
                                  strokeWidth: 7,
                                  backgroundColor: Color(0x5555AA55),
                                  valueColor:
                                      AlwaysStoppedAnimation<Color>(
                                    Color(0xFFEAF8C8),
                                  ),
                                ),
                                const Column(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Text(
                                      '81',
                                      style: TextStyle(
                                        fontSize: 25,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.white,
                                      ),
                                    ),
                                    Text(
                                      '/100',
                                      style: TextStyle(
                                        fontSize: 10,
                                        color: Colors.white70,
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(width: 18),
                          const Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Farm Health Score',
                                style: TextStyle(
                                  color: Colors.white70,
                                  fontSize: 14,
                                ),
                              ),
                              SizedBox(height: 6),
                              Text(
                                'Great job!',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 17,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                'Your farm is in good health.',
                                style: TextStyle(
                                  color: Colors.white70,
                                  fontSize: 12,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 25),

            // CONTENT
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Today's Action Plan",
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        'View All',
                        style: TextStyle(
                          color: Color(0xFF238636),
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 12),

                  ActionCard(
                    icon: Icons.coronavirus_outlined,
                    color: Colors.red,
                    title: 'Treat Early Blight',
                    subtitle: 'Affecting your tomato crop',
                    tag: 'High Priority',
                  ),

                  ActionCard(
                    icon: Icons.water_drop_outlined,
                    color: Colors.orange,
                    title: 'Irrigate within 24 hours',
                    subtitle: 'Soil moisture is low (18%)',
                    tag: 'Medium Priority',
                  ),

                  ActionCard(
                    icon: Icons.trending_up,
                    color: Colors.green,
                    title: 'Prices are rising',
                    subtitle: 'Good time to sell your produce',
                    tag: 'Opportunity',
                  ),

                  const SizedBox(height: 20),

                  const Text(
                    'Farm Overview',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 12),

                  Row(
                    children: const [
                      InfoCard(
                        emoji: '🍅',
                        title: 'Crop',
                        value: 'Tomato',
                      ),
                      SizedBox(width: 7),
                      InfoCard(
                        emoji: '☀️',
                        title: 'Temp',
                        value: '31°C',
                      ),
                      SizedBox(width: 7),
                      InfoCard(
                        emoji: '💧',
                        title: 'Humidity',
                        value: '78%',
                      ),
                      SizedBox(width: 7),
                      InfoCard(
                        emoji: '🌱',
                        title: 'Soil',
                        value: '18%',
                      ),
                    ],
                  ),

                  const SizedBox(height: 24),

                  const Text(
                    'Quick Access',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 12),

                  Row(
                    children: [
                      QuickButton(
                        icon: Icons.eco,
                        title: 'Check Crop',
                        color: Colors.green,
                        onTap: () {},
                      ),
                      QuickButton(
                        icon: Icons.smart_toy_outlined,
                        title: 'AI Advisor',
                        color: Colors.deepPurple,
                        onTap: () {},
                      ),
                      QuickButton(
                        icon: Icons.bar_chart,
                        title: 'Market',
                        color: Colors.green,
                        onTap: () {},
                      ),
                      QuickButton(
                        icon: Icons.people_outline,
                        title: 'Community',
                        color: Colors.orange,
                        onTap: () {},
                      ),
                    ],
                  ),

                  const SizedBox(height: 25),
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
// ACTION CARD
// ============================================================

class ActionCard extends StatelessWidget {
  final IconData icon;
  final Color color;
  final String title;
  final String subtitle;
  final String tag;

  const ActionCard({
    super.key,
    required this.icon,
    required this.color,
    required this.title,
    required this.subtitle,
    required this.tag,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(13),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(17),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 24,
            backgroundColor: color.withValues(alpha: 0.12),
            child: Icon(
              icon,
              color: color,
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Flexible(
                      child: Text(
                        title,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                    ),
                    const SizedBox(width: 5),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 6,
                        vertical: 3,
                      ),
                      decoration: BoxDecoration(
                        color: color.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        tag,
                        style: TextStyle(
                          color: color,
                          fontSize: 8,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  subtitle,
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
          const Icon(
            Icons.chevron_right,
            color: Colors.grey,
          ),
        ],
      ),
    );
  }
}

// ============================================================
// INFO CARD
// ============================================================

class InfoCard extends StatelessWidget {
  final String emoji;
  final String title;
  final String value;

  const InfoCard({
    super.key,
    required this.emoji,
    required this.title,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        height: 78,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(15),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              emoji,
              style: const TextStyle(fontSize: 19),
            ),
            Text(
              title,
              style: const TextStyle(
                fontSize: 9,
                color: Colors.grey,
              ),
            ),
            Text(
              value,
              style: const TextStyle(
                fontSize: 11,
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
// QUICK BUTTON
// ============================================================

class QuickButton extends StatelessWidget {
  final IconData icon;
  final String title;
  final Color color;
  final VoidCallback onTap;

  const QuickButton({
    super.key,
    required this.icon,
    required this.title,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          margin: const EdgeInsets.only(right: 7),
          padding: const EdgeInsets.symmetric(vertical: 15),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(
            children: [
              Icon(
                icon,
                color: color,
                size: 26,
              ),
              const SizedBox(height: 6),
              Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 9,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// ============================================================
// DISEASE
// ============================================================

class DiseasePage extends StatelessWidget {
  const DiseasePage({super.key});

  @override
  Widget build(BuildContext context) {
    return SimplePage(
      title: 'Disease Detection',
      subtitle: 'Detect crop diseases using AI.',
      children: [
        Container(
          height: 190,
          width: double.infinity,
          decoration: BoxDecoration(
            color: const Color(0xFFE6F3DC),
            borderRadius: BorderRadius.circular(24),
          ),
          child: const Icon(
            Icons.search,
            size: 90,
            color: Color(0xFF238636),
          ),
        ),
        const SizedBox(height: 20),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(30),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(24),
          ),
          child: Column(
            children: [
              const Icon(
                Icons.cloud_upload_outlined,
                size: 55,
                color: Colors.grey,
              ),
              const SizedBox(height: 15),
              const Text(
                'Upload Leaf Image',
                style: TextStyle(
                  fontSize: 19,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'Take a clear picture of your crop leaf.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 20),
              FilledButton.icon(
                onPressed: () {},
                icon: const Icon(Icons.photo_library),
                label: const Text('Choose from Gallery'),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

// ============================================================
// MARKET
// ============================================================

class MarketPage extends StatelessWidget {
  const MarketPage({super.key});

  @override
  Widget build(BuildContext context) {
    return SimplePage(
      title: 'Market',
      subtitle: 'Prices, trends and buyer discovery.',
      children: [
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: const Color(0xFFEAF6D9),
            borderRadius: BorderRadius.circular(24),
          ),
          child: const Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Tomato',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      '₹2,300 / q',
                      style: TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 6),
                    Text(
                      'Trend: Rising ↗',
                      style: TextStyle(
                        color: Colors.green,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              Text(
                '🍅',
                style: TextStyle(fontSize: 60),
              ),
            ],
          ),
        ),
        const SizedBox(height: 22),
        const PriceCard(
          crop: '🍅 Tomato',
          price: '₹2,300 / q',
          trend: 'Rising ↗',
        ),
        const PriceCard(
          crop: '🥔 Potato',
          price: '₹1,850 / q',
          trend: 'Stable —',
        ),
        const PriceCard(
          crop: '🧅 Onion',
          price: '₹2,100 / q',
          trend: 'Rising ↗',
        ),
        const SizedBox(height: 15),
        const ListCard(
          icon: Icons.groups_outlined,
          title: 'Nearby Buyers',
          subtitle: 'Find verified buyers near you',
        ),
      ],
    );
  }
}

class PriceCard extends StatelessWidget {
  final String crop;
  final String price;
  final String trend;

  const PriceCard({
    super.key,
    required this.crop,
    required this.price,
    required this.trend,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 9),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
      ),
      child: Row(
        children: [
          Text(
            crop,
            style: const TextStyle(
              fontWeight: FontWeight.bold,
            ),
          ),
          const Spacer(),
          Text(price),
          const SizedBox(width: 10),
          Text(
            trend,
            style: TextStyle(
              color: trend.startsWith('Rising')
                  ? Colors.green
                  : Colors.orange,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}

// ============================================================
// LOGISTICS
// ============================================================

class LogisticsPage extends StatelessWidget {
  const LogisticsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return SimplePage(
      title: 'Logistics',
      subtitle: 'Transport your produce safely.',
      children: [
        Container(
          height: 190,
          width: double.infinity,
          decoration: BoxDecoration(
            color: const Color(0xFFE1F0DD),
            borderRadius: BorderRadius.circular(24),
          ),
          child: const Icon(
            Icons.local_shipping,
            size: 90,
            color: Color(0xFF238636),
          ),
        ),
        const SizedBox(height: 20),
        const ListCard(
          icon: Icons.local_shipping_outlined,
          title: 'Available Transport',
          subtitle: 'Find nearby transport services',
        ),
        const ListCard(
          icon: Icons.storefront_outlined,
          title: 'Nearby Mandis',
          subtitle: 'Discover markets near you',
        ),
        const ListCard(
          icon: Icons.location_on_outlined,
          title: 'Track Transport',
          subtitle: 'Track your current shipment',
        ),
      ],
    );
  }
}

// ============================================================
// PROFILE
// ============================================================

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return SimplePage(
      title: 'Profile',
      subtitle: 'Manage your farmer and farm information.',
      children: [
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: const Color(0xFF238636),
            borderRadius: BorderRadius.circular(24),
          ),
          child: const Row(
            children: [
              CircleAvatar(
                radius: 38,
                backgroundColor: Colors.white,
                child: Icon(
                  Icons.person,
                  size: 45,
                  color: Color(0xFF238636),
                ),
              ),
              SizedBox(width: 15),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Farmer',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 5),
                  Text(
                    'Maharashtra, India',
                    style: TextStyle(
                      color: Colors.white70,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 20),
        const ListCard(
          icon: Icons.agriculture_outlined,
          title: 'Farm Information',
          subtitle: 'Manage your farm details',
        ),
        const ListCard(
          icon: Icons.eco_outlined,
          title: 'Crops',
          subtitle: 'Manage your crops and fields',
        ),
        const ListCard(
          icon: Icons.language,
          title: 'Language',
          subtitle: 'English',
        ),
        const ListCard(
          icon: Icons.notifications_outlined,
          title: 'Notifications',
          subtitle: 'Manage your notifications',
        ),
        const ListCard(
          icon: Icons.settings_outlined,
          title: 'Settings',
          subtitle: 'App settings and preferences',
        ),
      ],
    );
  }
}

// ============================================================
// LIST CARD
// ============================================================

class ListCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;

  const ListCard({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(17),
      ),
      child: Row(
        children: [
          Container(
            width: 45,
            height: 45,
            decoration: BoxDecoration(
              color: const Color(0xFFE5F3E4),
              borderRadius: BorderRadius.circular(13),
            ),
            child: Icon(
              icon,
              color: const Color(0xFF238636),
            ),
          ),
          const SizedBox(width: 13),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  subtitle,
                  style: const TextStyle(
                    color: Colors.grey,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
          const Icon(
            Icons.chevron_right,
            color: Colors.grey,
          ),
        ],
      ),
    );
  }
}

// ============================================================
// SIMPLE PAGE
// ============================================================

class SimplePage extends StatelessWidget {
  final String title;
  final String subtitle;
  final List<Widget> children;

  const SimplePage({
    super.key,
    required this.title,
    required this.subtitle,
    required this.children,
  });

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 10),
            Text(
              title,
              style: const TextStyle(
                fontSize: 29,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 5),
            Text(
              subtitle,
              style: const TextStyle(
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 5),
            ...children,
          ],
        ),
      ),
    );
  }
}