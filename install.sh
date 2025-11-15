#!/bin/bash

# ==========================================================
#  DILIP DC — Mobile Mirror Installer (FINAL STABLE VERSION)
#  Works on: Ubuntu, Debian, Kali, MX Linux, BlackBox Linux,
#  PopOS, Mint, Zorin, Elementary, Lubuntu, Xubuntu, etc.
# ==========================================================

set -e

APP_NAME="blackbox_mobile_mirror.py"
DESKTOP_FILE="$HOME/.local/share/applications/blackbox-mobile-mirror.desktop"
SCRCPY_PATH="/snap/bin/scrcpy"

echo "==============================================="
echo " Installing DILIP DC — Mobile Mirror"
echo "==============================================="

# --- Check if run as root (NOT allowed) ---
if [ "$EUID" = 0 ]; then
    echo "ERROR: Do NOT run this installer as root!"
    echo "Close and run: ./install.sh"
    exit 1
fi

# --- Check python app exists ---
if [ ! -f "$APP_NAME" ]; then
    echo "ERROR: $APP_NAME not found in this folder!"
    exit 1
fi

# --- Install basic packages ---
echo ""
echo "Checking required packages..."
sudo apt update
sudo apt install -y adb python3-gi gir1.2-gtk-3.0 xhost

# --- Install SNAP if missing ---
if ! command -v snap &>/dev/null; then
    echo ""
    echo "SNAP not found — installing snapd..."
    sudo apt install -y snapd
    sudo systemctl enable snapd
    sudo systemctl start snapd
fi

# --- Install latest SCRCPY using SNAP ---
echo ""
echo "Installing latest scrcpy (Snap version)..."
sudo snap install scrcpy

# --- Give snap scrcpy permission to access screen/USB ---
echo ""
echo "Granting scrcpy snap permissions..."
sudo snap connect scrcpy:raw-usb
sudo snap connect scrcpy:x11
sudo snap connect scrcpy:desktop
sudo snap connect scrcpy:wayland || true

# --- Allow X11 access (fixes display errors) ---
echo ""
echo "Fixing snap display permissions..."
xhost +si:localuser:$USER
xhost +local:root || true

# --- Make Python GUI executable ---
chmod +x "$APP_NAME"

# --- Install desktop launcher ---
echo ""
echo "Creating desktop launcher..."

mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=DILIP DC — Mobile Mirror
Comment=Mirror Android phone using scrcpy
Exec=python3 $PWD/$APP_NAME
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Utility;Application;
EOF

echo ""
echo "Refreshing applications menu..."
update-desktop-database ~/.local/share/applications || true

echo ""
echo "==============================================="
echo " INSTALLATION COMPLETE!"
echo "==============================================="
echo ""
echo "Run from menu: DILIP DC — Mobile Mirror"
echo "Or run manually: python3 $APP_NAME"
echo ""
echo "Enjoy!"
