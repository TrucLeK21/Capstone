import 'package:flutter/material.dart';
import 'package:health_app/consts.dart';
import 'package:health_app/models/metrics.dart';
import 'package:health_app/models/user.dart';
import 'package:health_app/services/auth_services.dart';
import 'package:health_app/services/user_services.dart';
import 'package:health_app/widgets/custom_footer.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  final int index = 2;
  User? user;
  Metrics? lastestRecord;

  void initState() {
    super.initState();
    // Gọi hàm lấy thông tin người dùng khi trang được tải
    _loadUserProfile();
  }

  void _loadUserProfile() async {
    try {
      final profile = await userServices().profile();

      if (profile != null) {
        print(profile);
        setState(() {
          user = profile;
          lastestRecord = user?.getLatestRecord();
        });
      } else {
        print('Không thể tải thông tin người dùng');
      }
    } catch (e) {
      print('Lỗi khi tải thông tin người dùng: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: AppColors.superLightGray,
        title: const Text("Hồ sơ"),
        centerTitle: true,
      ),
      body: _buildUI(),
      bottomNavigationBar: CustomFooter(
        curIdx: index,
      ),
    );
  }

  Widget _buildUI() {
    return Container(
      padding: EdgeInsets.fromLTRB(0, 20, 0, 20),
      decoration: const BoxDecoration(
        color: AppColors.superLightGray,
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // Image.asset(
          //   'assets/img/user-icon.png',
          //   width: 150,
          //   height: 150,
          // ),
          Text(
            user?.fullName ?? "Tên người dùng",
            style: const TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          // const SizedBox(
          //   height: 50,
          // ),
          Container(
            color: Colors.white,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildProfileField("Tên", user?.fullName ?? "Họ và tên"),
                _buildProfileField("Giới tính", user?.gender ?? "other"),
                _buildProfileField(
                    "Ngày sinh",
                    user?.dateOfBirth != null
                        ? "${user!.dateOfBirth!.day.toString().padLeft(2, '0')}/${user!.dateOfBirth!.month.toString().padLeft(2, '0')}/${user!.dateOfBirth!.year}"
                        : ""),
                _buildProfileField(
                    "Chiều cao (cm)", lastestRecord?.height?.toString() ?? ""),
                _buildProfileField(
                    "Cân nặng (kg)", lastestRecord?.weight?.toString() ?? ""),
                const SizedBox(
                  height: 30,
                ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    fixedSize: const Size(250, 50),
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.black,
                    side: const BorderSide(
                      color: Colors.black,
                      width: 2,
                    ),
                  ),
                  onPressed: () {
                    Navigator.pushNamed(context, '/edit-profile');
                  },
                  child: const Text(
                    "Chỉnh sửa",
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  ),
                ),
                const SizedBox(
                  height: 50,
                ),
              ],
            ),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              fixedSize: const Size(250, 50),
              backgroundColor: Color(0xffdc3545),
            ),
            onPressed: () {
              AuthServices().logout();
              Navigator.pushReplacementNamed(context, '/login');
            },
            child: const Text(
              "Đăng xuất",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
                color: Colors.white,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProfileField(String label, String value) {
    return Container(
      padding: const EdgeInsets.all(10.0),
      height: 60,
      decoration: const BoxDecoration(
        border: Border(
          top: BorderSide(
            color: AppColors.lightGray,
            width: 1,
          ),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.w500,
            ),
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w500,
              color: AppColors.boldGray,
            ),
          ),
        ],
      ),
    );
  }
}
