[app]
title = ArUco Scanner
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 1. Keep these unpinned so the stable recipes can compile them cleanly from source
python = 3.11
requirements = python3,kivy==2.3.0,numpy,opencv

# 2. THE CRITICAL FIX: Force the stable toolchain branch
# This prevents the build from using experimental Python 3.14 target environments
p4a.branch = stable

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
