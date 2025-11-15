#!/bin/bash

SCRCPY="/snap/bin/scrcpy"

echo "=============================================="
echo "   DILIP DC — BlackBox Mobile Mirror (CLI)"
echo "=============================================="
echo ""

if ! command -v adb &>/dev/null; then
    echo "ERROR: adb is not installed."
    exit 1
fi

if [ ! -x "$SCRCPY" ]; then
    echo "ERROR: scrcpy (snap) not found at $SCRCPY"
    echo "Install it using: sudo snap install scrcpy"
    exit 1
fi

echo "Detecting devices..."
DEVICES=$(adb devices | grep -w "device" | awk '{print $1}')

if [ -z "$DEVICES" ]; then
    echo "No devices found."
    exit 1
fi

echo ""
echo "Connected devices:"
i=1
declare -A LIST
for d in $DEVICES; do
    echo "$i) $d"
    LIST[$i]=$d
    ((i++))
done

echo ""
read -p "Choose device number: " num
DEVICE="${LIST[$num]}"

if [ -z "$DEVICE" ]; then
    echo "Invalid selection."
    exit 1
fi

echo ""
echo "Select quality preset:"
echo "1) Low (480p, 1M)"
echo "2) Medium (720p, 2M)"
echo "3) High (1080p, 8M)"
read -p "Choose (1/2/3): " q

case $q in
    1) SIZE=480; BIT="1M" ;;
    3) SIZE=1080; BIT="8M" ;;
    *) SIZE=720; BIT="2M" ;;
esac

echo ""
read -p "Record video? (y/n): " rec

if [[ "$rec" == "y" ]]; then
    read -p "Filename (default: dilip_record.mp4): " f
    [ -z "$f" ] && f="dilip_record.mp4"
    RECORD="--record $f"
else
    RECORD=""
fi

echo ""
echo "Starting scrcpy..."
$SCRCPY --serial "$DEVICE" --max-size "$SIZE" --video-bit-rate "$BIT" --window-title "DILIP DC — Mobile Mirror (CLI)" $RECORD
