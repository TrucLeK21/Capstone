import 'dart:convert';
import 'package:health_app/services/user_session.dart';
import 'package:health_app/services/http_services.dart';
import 'package:health_app/models/user.dart';

class userServices {
  Future<User?> profile() async {
    String? token = UserSession().token;
    Map<String, String> header = {};
    if (token != null) {
      header['Authorization'] = 'Bearer $token';
    }

    final res = await HttpServices().get('/users/profile', headers: header);
    if (res!.statusCode == 200) {
      Map<String, dynamic> data = jsonDecode(res.body);
      User user = User.fromJson(data);
      print(user);
      return user;
    } else {
      return null;
    }
  }

  Future<bool?> update(Map<String, dynamic> data) async {
    String? token = UserSession().token;
    Map<String, String> header = {};
    if (token != null) {
      header['Authorization'] = 'Bearer $token';
    }
    final res =
        await HttpServices().put('/users/update', data, headers: header);
    if (res!.statusCode == 200) {
      Map<String, dynamic> data = jsonDecode(res.body);
      print(data);
      return true;
    } else {
      return false;
    }
  }

  Future<List<dynamic>?> getLatestRecord() async {
    String? token = UserSession().token;
    Map<String, String> header = {};
    if (token != null) {
      header['Authorization'] = 'Bearer $token';
    }
    final res =
        await HttpServices().get('/users/latestRecord', headers: header);
    if (res!.statusCode == 200) {
      return jsonDecode(res.body);
    } else {
      return null;
    }
  }
}
