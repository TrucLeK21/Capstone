import 'package:flutter/material.dart';
import 'package:health_app/consts.dart';
import 'package:health_app/models/metrics.dart';
import 'package:health_app/models/user.dart';
import 'package:health_app/services/user_services.dart';
import 'package:health_app/widgets/custom_footer.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final int index = 0;
  User? user;
  Metrics? lastestRecord;

  @override
  void initState() {
    super.initState();
    // Gọi hàm lấy thông tin người dùng khi trang được tải
    _loadUserProfile();
  }

  // Hàm lấy thông tin người dùng
  void _loadUserProfile() async {
    try {
      final profile = await userServices().profile();

      if (profile != null) {
        setState(() {
          user = profile;
          lastestRecord = profile.getLatestRecord();
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
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        backgroundColor: AppColors.superLightGray,
        title: const Text(
          "Trang chủ",
        ),
        centerTitle: true,
      ),
      body: _buildUI(),
      bottomNavigationBar: CustomFooter(
        curIdx: index,
      ),
    );
  }

  Widget _buildUI() {
  return Stack(
    children: [
      // Nội dung chính
      Container(
        padding: const EdgeInsets.fromLTRB(15, 10, 15, 0),
        decoration: const BoxDecoration(
          color: AppColors.superLightGray,
        ),
        child: SingleChildScrollView(
          child: Column(
            children: [
              if (lastestRecord != null)
                ...lastestRecord!
                    .toJson()
                    .entries
                    .where((entry) =>
                        entry.key != "date") // Lọc ra các phần tử có key khác "date"
                    .map((entry) {
                  return _infoCard(
                      entry.key, entry.value); // Trả về card cho mỗi entry
                }).toList(),
            ],
          ),
        ),
      ),
      // Nút nổi
      Positioned(
        bottom: 20, // Khoảng cách từ cạnh dưới
        right: 20,  // Khoảng cách từ cạnh phải
        child: FloatingActionButton(
          onPressed: () {
            // Hành động khi nhấn nút
            print('Floating Action Button Pressed!');
          },
          child: const Icon(Icons.monitor_weight,size: 40,), // Biểu tượng trên nút
          backgroundColor: AppColors.mainColor, // Màu nền nút
          foregroundColor: Colors.white, // Màu biểu tượng
        ),
      ),
    ],
  );
}


  Widget _infoCard(String key, dynamic value) {
    return InkWell(
      onTap: () {
        Navigator.pushNamed(context, '/detail');
      },
      child: Container(
        width: double.infinity,
        height: 160,
        margin: const EdgeInsets.only(top: 10),
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(10),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.5), // Màu bóng với độ trong suốt
              spreadRadius: 5, // Độ lan của bóng
              blurRadius: 10, // Độ mờ của bóng
              offset: const Offset(4, 4), // Độ lệch của bóng (x, y)
            )
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Icon(
                      Icons.accessibility,
                      color: AppColors.mainColor,
                      size: 32,
                    ),
                    const SizedBox(width: 5),
                    Text(
                      key,
                      style: const TextStyle(
                        color: AppColors.mainColor,
                        fontWeight: FontWeight.bold,
                        fontSize: 22,
                      ),
                    ),
                  ],
                ),
                Row(
                  children: [
                    Text(
                      lastestRecord?.date != null
                          ? "${lastestRecord!.date!.day.toString().padLeft(2, '0')}/${lastestRecord!.date!.month.toString().padLeft(2, '0')}/${lastestRecord!.date!.year}"
                          : "",
                      style: const TextStyle(
                        color: AppColors.boldGray,
                        fontSize: 20,
                      ),
                    ),
                    const Icon(
                      Icons.arrow_forward_ios,
                      size: 20,
                      color: Colors.grey,
                    ),
                  ],
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  children: [
                    const Text(
                      "Tiêu chuẩn",
                      style: TextStyle(
                        color: AppColors.appGreen,
                        fontSize: 20,
                      ),
                    ),
                    Row(
                      children: [
                        Text(
                          value.toString(),
                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(
                          width: 15,
                        ),
                        const Text(
                          "kg",
                          style: TextStyle(
                            fontSize: 20,
                            color: AppColors.mediumGray,
                          ),
                        ),
                      ],
                    )
                  ],
                ),
                const Column(
                  children: [
                    Icon(
                      Icons.bar_chart,
                      size: 80,
                    )
                  ],
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
