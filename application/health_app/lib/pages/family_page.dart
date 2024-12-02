import 'package:flutter/material.dart';
import 'package:health_app/consts.dart';
import 'package:health_app/widgets/custom_footer.dart';

class FamilyPage extends StatefulWidget {
  const FamilyPage({super.key});

  @override
  State<FamilyPage> createState() => _FamilyPageState();
}

class _FamilyPageState extends State<FamilyPage> {
  final int index = 1;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        title: Text("Gia đình"),
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
      width: double.infinity,
      height: double.infinity,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              fixedSize: Size(250, 50),
              backgroundColor: AppColors.mainColor,
              foregroundColor: Colors.white,
            ),
            onPressed: () {},
            child: const Text(
              "Tạo",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
          ),
          const SizedBox(
            height: 20,
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              fixedSize: Size(250, 50),
              backgroundColor: Colors.white,
              foregroundColor: Colors.black,
              side: const BorderSide(
                color: Colors.black,
                width: 2,
              ),
            ),
            onPressed: () {},
            child: const Text(
              "Tham gia",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
          )
        ],
      ),
    );
  }
}
