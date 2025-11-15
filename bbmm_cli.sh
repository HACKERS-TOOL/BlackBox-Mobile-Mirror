#!/bin/bash

echo "=============================================="
echo "   DILIP DC — BlackBox Mobile Mirror (CLI)"
echo "=============================================="
echo ""

if ! command -v adb &>/dev/null; then
    echo "ERROR: adb is not installed."
    exit 1
fi

if ! command -v scrcpy &>/dev/null; then
    echo "ERROR: scrcpy is not installed."
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
echo "2) Medium (720p, 2.5M)"
echo "3) High (1024p, 8M)"
read -p "Choose (1/2/3): " q

case $q in
    1) SIZE=480; BIT="1M" ;;
    3) SIZE=1024; BIT="8M" ;;
    *) SIZE=720; BIT="2.5M" ;;
esac

echo ""
read -p "Record session? (y/n): " rec

if [[ "$rec" == "y" ]]; then
    read -p "Filename (default: dilip_record.mp4): " f
    [ -z "$f" ] && f="dilip_record.mp4"
    RECORD="--record $f"
else
    RECORD=""
fi

echo ""
echo "Starting scrcpy..."
scrcpy --serial "$DEVICE" --max-size "$SIZE" --bit-rate "$BIT" --window-title "DILIP DC — Mobile Mirror (CLI)" $RECORD
