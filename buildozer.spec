[app]
title = Titanium V60
package.name = titanium.v60.lockdown
package.domain = org.titanium.v60
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.60.0
requirements = python3,kivy==2.3.0,kivymd,android,pyjnius,plyer,openssl,requests
orientation = portrait
fullscreen = 1
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master