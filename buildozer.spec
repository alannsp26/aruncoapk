[app]
# (str) Title of your application
title = ArUco Detector

# (str) Package name
package.name = arucodetector

# (str) Package domain (needed for android/ios packaging)
package.domain = org.alan

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# Remove numpy and opencv-python-headless from here
requirements = python3,kivy==2.3.0

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Permissions
android.permissions = CAMERA

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 24

# (int) Android NDK API to use
android.ndk_api = 24

# (str) Android NDK version to use
android.ndk = 25c

# (list) Android archs to build
android.archs = arm64-v8a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
