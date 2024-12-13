import 'package:flutter/material.dart';
import 'package:health_app/consts.dart';
// import 'package:health_app/models/metrics.dart';
import 'package:health_app/models/user.dart';
// import 'package:health_app/pages/ble_page.dart';
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
  DateTime? latestDate;
  List<dynamic>? latestRecord;

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
      final res = await userServices().getLatestRecord();

      if (profile != null) {
        setState(() {
          user = profile;
        });
        if (res != null) {
          latestRecord = res;
          final dateRecord = latestRecord?.firstWhere(
              (record) => record['key'] == 'date',
              orElse: () => null);
          latestDate = dateRecord != null
              ? DateTime.tryParse(dateRecord['value'])
              : null;
        }
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
            child: ListView.builder(
              padding: const EdgeInsets.fromLTRB(0, 10, 0, 0),
              itemCount: latestRecord?.length ?? 0,
              itemBuilder: (context, index) {
                final record = latestRecord![index];
                if (record['key'] != 'date' && record['key'] != '_id' && record['key'] != 'age') {
                  return _infoCard(record['key'] ,record['name'], record['value'],
                      record['unit'] ?? '', latestDate);
                }
                return const SizedBox();
              },
            )),
        // Nút nổi
        Positioned(
          bottom: 20, // Khoảng cách từ cạnh dưới
          right: 20, // Khoảng cách từ cạnh phải
          child: FloatingActionButton(
            onPressed: () {
              // Hành động khi nhấn nút
              Navigator.pushNamed(context, "/ble-screen");
            },
            backgroundColor: AppColors.mainColor, // Màu nền nút
            foregroundColor: Colors.white, // Màu biểu tượng
            child: const Icon(
              Icons.monitor_weight,
              size: 40,
            ), // Biểu tượng trên nút
          ),
        ),
      ],
    );
  }

  Widget _infoCard(String key, String name, dynamic value, String? unit, DateTime? date) {
    return InkWell(
      onTap: () {
        Navigator.pushNamed(
          context,
          '/detail',
          arguments: {
            "metric": key,
          },
        );
      },
      child: Container(
        width: double.infinity,
        height: 165,
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
            FittedBox(
              child: Row(
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
                      SizedBox(
                        width: 130,
                        child: Text(
                          name,
                          style: const TextStyle(
                            color: AppColors.mainColor,
                            fontWeight: FontWeight.bold,
                            fontSize: 22,
                          ),
                          softWrap: true,
                        ),
                      ),
                    ],
                  ),
                  Row(
                    children: [
                      Text(
                        latestDate != null
                            ? "${latestDate!.day.toString().padLeft(2, '0')}/${latestDate!.month.toString().padLeft(2, '0')}/${latestDate!.year}"
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
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "Giá trị",
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
                        Text(
                          unit ?? "",
                          style: const TextStyle(
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
