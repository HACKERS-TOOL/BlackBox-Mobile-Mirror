# Packaging Guide — DILIP DC Mobile Mirror

This document helps Linux maintainers package the application as:

- `.deb` package  
- AppImage  
- Snap (future)  
- Flatpak (future)  

The application runs using Python + GTK3 + snap scrcpy.

---

# 📦 1. Dependencies

### Runtime:

- python3  
- python3-gi  
- gir1.2-gtk-3.0  
- adb  
- snap (for scrcpy backend)  
- scrcpy (snap package)

### Installer will configure:

- snap scrcpy  
- snap permissions  
- xhost X11 access  
- desktop launcher  

---

# 🧱 2. Folder Structure for Packaging

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
