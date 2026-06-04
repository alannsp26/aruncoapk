[app]
title = My ArUco Detector
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 1. Standard requirements
python = 3.11
requirements = python3,kivy==2.3.0,numpy,opencv

# 2. THE CRITICAL FIX: Change 'stable' to 'master'
# This pulls the modern toolchain that supports AAB and modern Android NDKs
p4a.branch = master

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
# Modern p4a works best with modern NDKs
android.ndk = 25c
android.api = 33
android.minapi = 24
