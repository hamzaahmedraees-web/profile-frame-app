[app]
title = Profile Frame Maker
package.name = profileframemaker
package.domain = com.myapp
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
source.include_patterns = assets/*
version = 1.0
requirements = python3,kivy==2.2.1,pillow,android
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.release_artifact = aab
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
