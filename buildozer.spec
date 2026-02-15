[app]
title = Titanium Victory
package.name = titanium.victory.apk
package.domain = org.titanium.v47
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.47.0
# Removed pyserpent and redundant sdl2 dependencies
requirements = python3,kivy,android,pyjnius,openssl,requests
orientation = portrait
fullscreen = 1
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_FINE_LOCATION, CAMERA
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master