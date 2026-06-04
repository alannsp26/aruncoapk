[app]
title = My ArUco Detector
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# We list only pure-Python or compatible platform requirements here.
# Numpy and OpenCV will be handled by the CI/pip step.
requirements = python3,kivy==2.3.0

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[buildozer]
# Pin NDK to a stable version known to work with OpenCV/Numpy
android.ndk = 25c
android.api = 33
android.minapi = 24
