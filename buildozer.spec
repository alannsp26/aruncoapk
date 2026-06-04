[app]
title = My ArUco Detector
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 1. Target dependencies (let Buildozer cross-compile them)
requirements = python3,kivy==2.3.0,numpy,opencv

# 2. THE CRITICAL FIX: Lock to a known stable release branch
# This prevents the experimental Python 3.14 C-API header crash
p4a.branch = release-2024.01.21

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

# 3. Pin the NDK to 25b, which perfectly matches the stable p4a branch
android.ndk = 25b
android.api = 33
android.minapi = 24
