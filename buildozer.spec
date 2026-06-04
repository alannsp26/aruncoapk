[app]
title = My ArUco Detector
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# THE CRITICAL FIX: Lock both the host and target pythons to 3.11.9
requirements = python3,kivy==2.3.0,numpy,opencv

p4a.branch = master

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
fullscreen = 0

[buildozer]
android.ndk = 25b
