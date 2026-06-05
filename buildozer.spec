[app]
title = ArUco Scanner
package.name = arucoscanner
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 1. FIXED: Must be 'opencv' (the p4a recipe name), not 'opencv-python'
requirements = python3,kivy==2.3.0,numpy,opencv-python-headless

p4a.branch = release-2024.01.21

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

android.ndk = 25b
android.sdk = 33
android.minapi = 24
android.ndk_path = /opt/android-ndk-r25b
# android.sdk_path = /opt/android-sdk

p4a.local_recipes = 

# 2. FIXED: Directly solves the "java.lang.OutOfMemoryError" in Gradle
android.add_gradle_properties = org.gradle.jvmargs=-Xmx4g -XX:+UseG1GC
