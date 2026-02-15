[app]
title = Titanium Robot
package.name = titanium.robot.auto
package.domain = org.titanium.dileep
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.48.2
requirements = python3,kivy==2.3.0,kivymd,android,pyjnius,plyer,openssl,requests,sqlite3,pillow
orientation = portrait
fullscreen = 1
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_FINE_LOCATION, CAMERA
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master