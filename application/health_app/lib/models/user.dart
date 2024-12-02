import 'dart:convert';
import './metrics.dart';

class User {
  int id;
  String username;
  String password;
  String? fullName;
  DateTime? dateOfBirth;
  String? gender;
  int? group;
  List<Metrics>? records;

  User({
    required this.id,
    required this.username,
    required this.password,
    this.fullName,
    this.dateOfBirth,
    this.gender,
    this.group,
    this.records,
  });

  // Phương thức tạo đối tượng User từ JSON
  factory User.fromJson(Map<String, dynamic> json) {
    json.forEach((key, value) {
      print('Field: $key, Type: ${value.runtimeType}, Value: $value');
    });
    return User(
      id: json['id'] ?? 1, // Gán giá trị mặc định 0 nếu 'id' là null
      username:
          json['username'] ?? '', // Gán giá trị mặc định nếu 'username' là null
      password:
          json['password'] ?? '', // Gán giá trị mặc định nếu 'password' là null
      fullName: json['fullName'],
      dateOfBirth: json['dateOfBirth'] != null
          ? DateTime.parse(json['dateOfBirth'])
          : null,
      gender: json['gender'] ?? '',
      group: json['group'] ?? null,
      records: json['records'] != null
          ? List<Map<String, dynamic>>.from(json['records'])
              .map((x) => Metrics.fromJson(x))
              .toList()
          : [], // Trả về danh sách rỗng nếu không có 'records'
    );
  }

  // Phương thức chuyển đối tượng User thành JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'password': password,
      'fullName': fullName,
      'dateOfBirth': dateOfBirth?.toIso8601String(),
      'gender': gender,
      'group': group,
      'records': records?.map((x) => x.toJson()).toList(),
    };
  }

  User copyWith({
    int? id,
    String? username,
    String? password,
    String? fullName,
    DateTime? dateOfBirth,
    String? gender,
    int? group,
    List<Metrics>? records,
  }) =>
      User(
        id: id ?? this.id,
        username: username ?? this.username,
        password: password ?? this.password,
        fullName: fullName ?? this.fullName,
        dateOfBirth: dateOfBirth ?? this.dateOfBirth,
        gender: gender ?? this.gender,
        group: group ?? this.group,
        records: records ?? this.records,
      );

  // Lấy bản ghi mới nhất từ records
  Metrics? getLatestRecord() {
    if (records != null && records!.isNotEmpty) {
      records!.sort(
          (a, b) => b.date!.compareTo(a.date!)); // Sắp xếp theo ngày giảm dần
      return records!.first;
    }
    return null; // Trả về null nếu không có bản ghi
  }

  @override
  String toString() {
    return jsonEncode(toJson());
  }
}
