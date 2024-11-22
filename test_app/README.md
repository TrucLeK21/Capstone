## Getting Started

### Add permissions for Android (No Location)

In the **android/app/src/main/AndroidManifest.xml** add:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

     <!-- Allow Bluetooth -->
     <uses-feature android:name="android.hardware.bluetooth_le" android:required="true" />

     <!-- New Bluetooth permissions in Android 12
     https://developer.android.com/about/versions/12/features/bluetooth-permissions -->
     <uses-permission android:name="android.permission.BLUETOOTH_SCAN" android:usesPermissionFlags="neverForLocation" />
     <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
 
     <!-- legacy for Android 11 or lower -->
     <uses-permission android:name="android.permission.BLUETOOTH" android:maxSdkVersion="30" />
     <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" android:maxSdkVersion="30" />
     <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" android:maxSdkVersion="30"/>
 
 
     <!-- legacy for Android 9 or lower -->
     <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" android:maxSdkVersion="28" />
```
Add dependencies

```yaml
dependencies:
  flutter:
    sdk: flutter


  # The following adds the Cupertino Icons font to your application.
  # Use with the CupertinoIcons class for iOS style icons.
  cupertino_icons: ^1.0.8
  get: ^4.6.5
  flutter_blue_plus: ^1.4.0
```
Add images to asset folder
**assets/**

