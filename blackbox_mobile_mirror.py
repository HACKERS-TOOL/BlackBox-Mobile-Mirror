#!/usr/bin/env python3
"""
Black Box Mobile Mirror — Advanced GUI wrapper for scrcpy
Brand: DILIP DC

Fully fixed for:
- scrcpy 3.x (Snap version)
- Android 14/15 devices (Motorola G45)
- New scrcpy flags (--video-bit-rate)
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import subprocess
import threading
import shlex
import shutil
import os

APP_TITLE = "DILIP DC — Mobile Mirror"

class MobileMirrorApp(Gtk.Window):
    def __init__(self):
        super().__init__(title=APP_TITLE)
        self.set_border_width(8)
        self.set_default_size(650, 430)

        # Force snap scrcpy
        self.scrcpy_path = "/snap/bin/scrcpy"
        self.adb_path = shutil.which('adb')

        # Header
        hb = Gtk.HeaderBar(title=APP_TITLE)
        hb.set_show_close_button(True)
        self.set_titlebar(hb)

        self.status_label = Gtk.Label(label="Status: Idle")
        hb.pack_end(self.status_label)

        self.spinner = Gtk.Spinner()
        hb.pack_start(self.spinner)

        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(main)

        # Device selection
        row = Gtk.Box(spacing=6)
        main.pack_start(row, False, False, 0)

        self.device_combo = Gtk.ComboBoxText()
        row.pack_start(self.device_combo, True, True, 0)

        refresh_btn = Gtk.Button(label="Refresh")
        refresh_btn.connect("clicked", self.on_refresh)
        row.pack_start(refresh_btn, False, False, 0)

        wifi_btn = Gtk.Button(label="Wireless: Discover")
        wifi_btn.connect("clicked", self.on_wireless)
        row.pack_start(wifi_btn, False, False, 0)

        # Options
        grid = Gtk.Grid(column_spacing=6, row_spacing=6)
        main.pack_start(grid, False, False, 0)

        grid.attach(Gtk.Label(label="Preset:"), 0, 0, 1, 1)
        self.preset_combo = Gtk.ComboBoxText()
        self.preset_combo.append_text("Low (480p, 1M)")
        self.preset_combo.append_text("Medium (720p, 2M)")
        self.preset_combo.append_text("High (1080p, 8M)")
        self.preset_combo.set_active(1)
        grid.attach(self.preset_combo, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Max size (0=no limit):"), 0, 1, 1, 1)
        self.entry_max = Gtk.Entry()
        self.entry_max.set_text("0")
        grid.attach(self.entry_max, 1, 1, 1, 1)

        grid.attach(Gtk.Label(label="Video bitrate (e.g. 2M):"), 0, 2, 1, 1)
        self.entry_bitrate = Gtk.Entry()
        self.entry_bitrate.set_text("2M")
        grid.attach(self.entry_bitrate, 1, 2, 1, 1)

        self.record_check = Gtk.CheckButton(label="Record session")
        grid.attach(self.record_check, 0, 3, 2, 1)

        grid.attach(Gtk.Label(label="Record file:"), 0, 4, 1, 1)
        self.record_file = Gtk.Entry()
        self.record_file.set_text("dilip_record.mp4")
        grid.attach(self.record_file, 1, 4, 1, 1)

        # Buttons
        btn_row = Gtk.Box(spacing=6)
        main.pack_start(btn_row, False, False, 0)

        self.start_btn = Gtk.Button(label="Start Mirror")
        self.start_btn.connect("clicked", self.on_start)
        btn_row.pack_start(self.start_btn, True, True, 0)

        self.stop_btn = Gtk.Button(label="Stop")
        self.stop_btn.set_sensitive(False)
        self.stop_btn.connect("clicked", self.on_stop)
        btn_row.pack_start(self.stop_btn, True, True, 0)

        hint_btn = Gtk.Button(label="Install deps hint")
        hint_btn.connect("clicked", self.on_hint)
        btn_row.pack_start(hint_btn, True, True, 0)

        # Log output
        frame = Gtk.Frame(label="Output / Logs")
        main.pack_start(frame, True, True, 0)

        scroll = Gtk.ScrolledWindow()
        frame.add(scroll)

        self.log_view = Gtk.TextView()
        self.log_view.set_editable(False)
        scroll.add(self.log_view)
        self.log_buf = self.log_view.get_buffer()

        self.scrcpy_proc = None
        self.connect("delete-event", self.on_quit)

        GLib.idle_add(self.on_refresh, None)

    # Logging
    def log(self, text):
        end = self.log_buf.get_end_iter()
        self.log_buf.insert(end, text + "\n")

    def status(self, text, running=False):
        self.status_label.set_text(f"Status: {text}")
        if running:
            self.spinner.start()
        else:
            self.spinner.stop()

    # Refresh devices
    def on_refresh(self, _btn):
        self.device_combo.remove_all()
        if not self.adb_path:
            self.device_combo.append_text("adb not found")
            self.device_combo.set_active(0)
            return

        out = subprocess.check_output([self.adb_path, "devices"], text=True)
        found = False
        for line in out.splitlines():
            if "device" in line and not "List of devices" in line:
                serial = line.split("\t")[0]
                self.device_combo.append_text(serial)
                found = True

        if not found:
            self.device_combo.append_text("No devices")

        self.device_combo.set_active(0)
        self.log("Device list refreshed")

    def on_wireless(self, _):
        self.log("Wireless mode: run adb tcpip 5555 + adb connect <IP>")

    # Build scrcpy command
    def build_cmd(self):
        device = self.device_combo.get_active_text()
        if not device or "No devices" in device:
            return None

        cmd = [self.scrcpy_path, "--serial", device]

        preset = self.preset_combo.get_active_text()
        if "Low" in preset:
            max_size = "480"
            bitrate = "1M"
        elif "High" in preset:
            max_size = "1080"
            bitrate = "8M"
        else:
            max_size = "720"
            bitrate = "2M"

        if self.entry_max.get_text().strip() != "0":
            max_size = self.entry_max.get_text().strip()

        if self.entry_bitrate.get_text().strip():
            bitrate = self.entry_bitrate.get_text().strip()

        cmd += ["--max-size", max_size]
        cmd += ["--video-bit-rate", bitrate]
        cmd += ["--window-title", APP_TITLE]

        if self.record_check.get_active():
            fname = self.record_file.get_text().strip() or "dilip_record.mp4"
            cmd += ["--record", fname]

        return cmd

    # Start scrcpy
    def on_start(self, _):
        cmd = self.build_cmd()
        if not cmd:
            self.log("No device selected")
            return

        self.log("Starting scrcpy...")
        self.status("Starting...", True)

        def run():
            try:
                self.scrcpy_proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
            except Exception as e:
                self.log(f"Error: {e}")
                self.status("Error", False)
                return

            self.start_btn.set_sensitive(False)
            self.stop_btn.set_sensitive(True)
            self.status("Streaming", True)

            for line in self.scrcpy_proc.stdout:
                self.log(line.strip())

            self.status("Idle", False)
            self.start_btn.set_sensitive(True)
            self.stop_btn.set_sensitive(False)

        threading.Thread(target=run, daemon=True).start()

    # Stop scrcpy
    def on_stop(self, _):
        if self.scrcpy_proc:
            self.scrcpy_proc.terminate()
            self.log("Scrcpy stopped")
            self.status("Stopped", False)

    def on_hint(self, _):
        self.log("Install packages: sudo apt install adb python3-gi")

    def on_quit(self, *_):
        if self.scrcpy_proc:
            self.scrcpy_proc.terminate()
        Gtk.main_quit()


if __name__ == "__main__":
    win = MobileMirrorApp()
    win.show_all()
    Gtk.main()
