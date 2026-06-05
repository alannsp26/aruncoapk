[app]
title = My ArUco Detector
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Ensure requirements are compatible with Python 3.11
# Note: opencv in p4a often requires specific handling; 
# ensure you aren't pulling incompatible versions.
requirements = python3,kivy==2.3.0,numpy,opencv-python

# The stable branch is correct; keep it.
p4a.branch = release-2024.01.21

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.ico
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

# Android settings aligned with NDK r25b
android.ndk = 25b
android.sdk = 33
android.minapi = 24
android.ndk_path = /opt/android-ndk-r25b
# Ensure the SDK path is defined if not automatically found by buildozer
# android.sdk_path = /opt/android-sdk

# Optimization: Ensure buildozer uses the environment's python
# This helps the build process respect the 3.11 virtualenv we created
p4a.local_recipes =
