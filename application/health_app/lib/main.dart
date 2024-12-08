import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:health_app/consts.dart';
import 'package:health_app/pages/ble_page.dart';
import 'package:health_app/pages/detail_page.dart';
import 'package:health_app/pages/edit_profile_page.dart';
import 'package:health_app/pages/family_page.dart';
import 'package:health_app/pages/home_page.dart';
import 'package:health_app/pages/login_page.dart';
import 'package:health_app/pages/profile_page.dart';
import 'package:health_app/pages/register_page.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Khóa hướng màn hình
  await SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return MaterialApp(
      title: 'Health App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        appBarTheme: const AppBarTheme(
          titleTextStyle: TextStyle(
            color: AppColors.mainColor,
            fontSize: 25,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      initialRoute: '/login',
      routes: {
        "/login": (context) => const LoginPage(),
        "/register": (context) => const RegisterPage(),
        "/home": (context) => const HomePage(),
        "/detail": (context) => const DetailPage(),
        "/family": (context) => const FamilyPage(),
        "/profile": (context) => const ProfilePage(),
        "/edit-profile": (context) => const EditProfilePage(),
        "/ble-screen": (context) => const BlueetoothConnectionScreen(),
      },
    );
  }
}
