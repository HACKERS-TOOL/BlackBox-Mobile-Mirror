# PACKAGING — BlackBox Mobile Mirror (DILIP DC)

This document describes how to package the BlackBox Mobile Mirror into:
- .deb package (Debian/Ubuntu/Kali/MX)
- AppImage (all Linux distros)
- Tar.gz release (simple Linux package)
- Recommended GitHub release structure

---

# 1. Build a .deb Package (Debian/Ubuntu/Kali/MX)

## 1.1 Folder Structure

Create the following:

deb-build/
└── blackbox-mobile-mirror/
    ├── DEBIAN/
    │   └── control
    └── usr/
        └── local/
            └── share/
                └── blackbox-mobile-mirror/
                    ├── blackbox_mobile_mirror.py
                    ├── bbmm_cli.sh
                    ├── install.sh
                    ├── blackbox-mobile-mirror.desktop
                    └── README.md

---

## 1.2 control File

Place this in:
deb-build/blackbox-mobile-mirror/DEBIAN/control

Content:

Package: blackbox-mobile-mirror
Version: 1.0
Section: utils
Priority: optional
Architecture: all
Maintainer: DILIP DC
Description: Android screen mirroring tool using scrcpy and adb.
 A lightweight GUI + CLI tool to mirror and control Android devices on Linux.
 Built for Blackbox and low-resource Linux systems.
Depends: python3, python3-gi, adb, scrcpy

---

## 1.3 Build the .deb

Run:

dpkg-deb --build deb-build/blackbox-mobile-mirror

Output:

blackbox-mobile-mirror.deb

---

## 1.4 Install the .deb

sudo dpkg -i blackbox-mobile-mirror.deb
sudo apt --fix-broken install

---

# 2. Build an AppImage (Universal Linux Package)

## 2.1 Folder Structure

AppDir/
├── AppRun
├── blackbox-mobile-mirror.desktop
├── blackbox_mobile_mirror.py
└── icons/
    └── app.png

---

## 2.2 AppRun File

Create AppRun:

#!/bin/bash
HERE="$(dirname "$(readlink -f "$0")")"
python3 "$HERE/blackbox_mobile_mirror.py"

Make executable:

chmod +x AppRun

---

## 2.3 Build AppImage

wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

./appimagetool-x86_64.AppImage AppDir

Output:

BlackBox-Mobile-Mirror-x86_64.AppImage

---

# 3. Tar.gz Release

tar -czvf blackbox-mobile-mirror-v1.0.tar.gz \
    blackbox_mobile_mirror.py bbmm_cli.sh install.sh README.md

---

# 4. GitHub Project Structure

Recommended folder layout:

BlackBox-Mobile-Mirror/
│
├── blackbox_mobile_mirror.py
├── bbmm_cli.sh
├── install.sh
├── blackbox-mobile-mirror.desktop
├── README.md
└── PACKAGING.md

---

# 5. GitHub Release

Create Release: v1.0  
Upload assets:

- blackbox-mobile-mirror.deb
- BlackBox-Mobile-Mirror-x86_64.AppImage
- blackbox-mobile-mirror-v1.0.tar.gz

---

# 6. Recommended Extras

- Add icon (app.png) for desktop/AppImage
- Add MIT LICENSE
- Add screenshots of GUI
- Add GitHub Actions workflow for automatic builds

---

# End of PACKAGING.md
