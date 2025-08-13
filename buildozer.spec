
[app]
title = リアルお店屋さんごっこ
package.name = shopgame
package.domain = org.rio.omiseya
source.dir = .
source.include_exts = py,kv,json,mp3,ogg,png,jpg,ttf
version = 0.4.0
requirements = python3==3.12.6, kivy==2.3.1, kivymd, ffpyplayer, pillow, plyer, android, pyjnius
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
orientation = landscape
fullscreen = 0
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
