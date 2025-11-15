# BlackBox Mobile Mirror (DILIP DC)

A lightweight Android screen mirroring tool for Linux using adb + scrcpy.
Includes a full GTK3 GUI and a minimal CLI version.

## Features
- Mirror Android screen
- Keyboard + mouse control
- USB + Wireless ADB
- Low/Medium/High presets
- Recording support
- Clean GTK3 interface
- Ultra-light Bash CLI script

## Requirements
sudo apt install -y adb scrcpy python3-gi gir1.2-gtk-3.0

## Run GUI
python3 blackbox_mobile_mirror.py

## CLI Mode
chmod +x bbmm_cli.sh
./bbmm_cli.sh

## Install launcher
chmod +x install.sh
./install.sh

## For packagers
See PACKAGING.md

## License
MIT
