import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

class BlueetoothConnectionScreen extends StatefulWidget {
  const BlueetoothConnectionScreen({super.key});

  @override
  State<BlueetoothConnectionScreen> createState() => _BlueetoothConnectionScreenState();
}

class _BlueetoothConnectionScreenState extends State<BlueetoothConnectionScreen> {

  final Guid serviceUuid = Guid('0000181d-0000-1000-8000-00805f9b34fb');
  final Guid characteristicUuid = Guid('00002a9d-0000-1000-8000-00805f9b34fb');

  

  @override
  Widget build(BuildContext context) {
    return const Placeholder();
  }
}