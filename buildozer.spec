[app]
title = My ArUco Detector
package.name = arucodetector
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 1. Core requirements for the vision processing app
requirements = python3,kivy==2.3.0,numpy,opencv

# Note: p4a.branch is intentionally removed here to enforce the stable toolchain

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

# 2. Android API targets
android.api = 33
android.minapi = 24

# Note: android.ndk is intentionally omitted so the stable toolchain auto-downloads its preferred NDK
