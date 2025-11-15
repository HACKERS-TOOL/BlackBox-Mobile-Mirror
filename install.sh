#!/bin/bash

APP="blackbox_mobile_mirror.py"
DESKTOP="$HOME/.local/share/applications/blackbox-mobile-mirror.desktop"

echo "Installing DILIP DC — Mobile Mirror..."

if [ ! -f "$APP" ]; then
    echo "ERROR: $APP not found!"
    exit 1
fi

echo "Checking dependencies..."
MISSING=()

for pkg in adb scrcpy python3-gi; do
    if ! command -v $pkg &>/dev/null; then
        MISSING+=($pkg)
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "Missing packages: ${MISSING[@]}"
    read -p "Install now? (y/n): " a
    if [[ "$a" == "y" ]]; then
        sudo apt update
        sudo apt install -y adb scrcpy python3-gi gir1.2-gtk-3.0
    fi
fi

chmod +x "$APP"

mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP" <<EOF
[Desktop Entry]
Name=DILIP DC — Mobile Mirror
Exec=python3 $PWD/blackbox_mobile_mirror.py
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Utility;
EOF

echo "Installation complete."
echo "Run using: python3 $APP"
