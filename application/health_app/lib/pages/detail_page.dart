import 'package:flutter/material.dart';
import 'package:health_app/consts.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:health_app/widgets/custom_footer.dart';

class DetailPage extends StatefulWidget {
  const DetailPage({super.key});

  @override
  State<DetailPage> createState() => _DetailPageState();
}
// test
class _DetailPageState extends State<DetailPage> {
  final int index = 0;
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        title: const Column(children: [
          Text("Chi tiết"),
          Text(
            "Lúc 15:30 29 tháng 10",
            style: TextStyle(
              fontSize: 18,
              color: Colors.black,
              fontWeight: FontWeight.w300,
            ),
          )
        ]),
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
      child: Column(
        children: [
          //Represent Data
          Container(
            width: double.infinity,
            height: 200,
            color: Colors.white,
            child: const Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  // crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Baseline(
                      baseline: 64,
                      baselineType: TextBaseline.alphabetic,
                      child: Text(
                        "62.3",
                        style: TextStyle(
                          fontSize: 64,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                    SizedBox(
                      width: 15,
                    ),
                    Baseline(
                      baseline: 48,
                      baselineType: TextBaseline.alphabetic,
                      child: Text(
                        "kg",
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.w400,
                          color: AppColors.boldGray,
                        ),
                      ),
                    )
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      "tiêu chuẩn",
                      style: TextStyle(
                        color: AppColors.appGreen,
                        fontSize: 24,
                      ),
                    )
                  ],
                )
              ],
            ),
          ),
          // Represent chart
          Container(
            width: double.infinity,
            height: 250,
            color: Colors.white,
            padding: const EdgeInsets.all(20),
            child: LineChart(
              LineChartData(
                  titlesData: FlTitlesData(
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(
                          showTitles: true,
                          reservedSize: 40,
                          getTitlesWidget: (value, meta) {
                            return Container(
                              margin: const EdgeInsets.fromLTRB(0, 0, 10, 10),
                              child: Text("$value"),
                            );
                          }),
                    ),
                    rightTitles: const AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: false,
                      ),
                    ),
                    topTitles: const AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: false,
                      ),
                    ),
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 30,
                        interval: 1,
                        getTitlesWidget: (value, meta) {
                          switch (value.toInt()) {
                            case 0:
                              return Container(
                                margin: const EdgeInsets.only(top: 15),
                                child: const Text(
                                  'January',
                                  style: TextStyle(fontSize: 12),
                                ),
                              );
                            case 1:
                              return Container(
                                margin: const EdgeInsets.only(top: 15),
                                child: const Text(
                                  'February',
                                  style: TextStyle(fontSize: 12),
                                ),
                              );
                            case 2:
                              return Container(
                                margin: const EdgeInsets.only(top: 15),
                                child: const Text(
                                  'March',
                                  style: TextStyle(fontSize: 12),
                                ),
                              );
                            case 3:
                              return Container(
                                margin: const EdgeInsets.only(top: 15),
                                child: const Text(
                                  'April',
                                  style: TextStyle(fontSize: 12),
                                ),
                              );
                            default:
                              return const Text('');
                          }
                        },
                      ),
                    ),
                  ),
                  borderData: FlBorderData(
                    show: false,
                  ),
                  gridData: const FlGridData(
                    show: false,
                  ),
                  lineBarsData: [
                    LineChartBarData(spots: [
                      const FlSpot(0, 60),
                      const FlSpot(1, 62),
                      const FlSpot(2, 63),
                      const FlSpot(3, 62.3),
                    ])
                  ]),
            ),
          ),
        ],
      ),
    );
  }
}
