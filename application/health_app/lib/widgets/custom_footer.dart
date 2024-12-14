import 'package:flutter/material.dart';
import 'package:health_app/consts.dart';

class CustomFooter extends StatelessWidget {
  final int curIdx;

  const CustomFooter({required this.curIdx});

  @override
  Widget build(BuildContext context) {
    void onItemTapped(index) {
      if (index != curIdx) {
        switch (index) {
          case 0:
            Navigator.pushNamedAndRemoveUntil(context, '/home', (route) => false);
            
            break;
          case 1:
            Navigator.pushNamedAndRemoveUntil(context, '/family', (route) => false);
            break;
          case 2:
            Navigator.pushNamedAndRemoveUntil(context, '/profile', (route) => false);
            break;

          default:
            break;
        }
      }
    }

    // TODO: implement build
    return Container(
      decoration: const BoxDecoration(
        border: Border(
          top: BorderSide(
            color: AppColors.lightGray,
          ),
        ),
      ),
      height: 80,
      child: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.house),
            label: 'Trang chủ',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: 'Gia đình',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Hồ sơ',
          ),
        ],
        iconSize: 40,
        selectedItemColor: AppColors.mainColor,
        unselectedItemColor: AppColors.boldGray,
        backgroundColor: AppColors.superLightGray,
        currentIndex: curIdx,
        onTap: onItemTapped,
      ),
    );
  }
}
