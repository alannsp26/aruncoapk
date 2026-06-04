[app]
title = My ArUco Detector
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Forcing the compilation framework to target Python 3.11 compatibility
python = 3.11
requirements = python3,kivy==2.3.0,numpy,opencv
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
