[app]
title = My ArUco Detector
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Keep these unpinned here to bypass the git checkout pathspec bug.
# Python-for-android will handle compiling them as standard dependencies.
python = 3.11
requirements = python3,kivy==2.3.0,numpy,opencv-python-headless

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
