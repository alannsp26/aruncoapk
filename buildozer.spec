[app]
title = My ArUco Detector
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 1. THE CRITICAL FIX: Lock the target APK compilation down to stable Python 3.11 
# and let the build toolchain compile NumPy and OpenCV for it.
requirements = python3==3.11.9,kivy==2.3.0,numpy,opencv

# 2. Keep the modern master branch toolchain active
p4a.branch = master

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
android.ndk = 25c
android.api = 33
android.minapi = 24
