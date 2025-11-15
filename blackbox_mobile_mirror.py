#!/usr/bin/env python3
"""
Black Box Mobile Mirror — Advanced GUI wrapper for scrcpy
Branding/title: DILIP DC

Requirements:
 - Python 3.8+
 - adb
 - scrcpy
 - python3-gi (GTK3)

This script launches adb + scrcpy using a clean GTK3 interface.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import subprocess
import threading
import shlex
import shutil

APP_TITLE = "DILIP DC — Mobile Mirror"

class MobileMirrorApp(Gtk.Window):
    def __init__(self):
        super().__init__(title=APP_TITLE)
        self.set_border_width(8)
        self.set_default_size(640, 420)

        hb = Gtk.HeaderBar(title=APP_TITLE)
        hb.set_show_close_button(True)
        self.set_titlebar(hb)

        self.status_label = Gtk.Label(label="Status: Idle")
        hb.pack_end(self.status_label)

        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(main)

        row = Gtk.Box(spacing=6)
        main.pack_start(row, False, False, 0)

        self.device_combo = Gtk.ComboBoxText()
        row.pack_start(self.device_combo, True, True, 0)

        btn_refresh = Gtk.Button(label="Refresh")
        btn_refresh.connect('clicked', self.on_refresh)
        row.pack_start(btn_refresh, False, False, 0)

        btn_wireless = Gtk.Button(label="Wireless Discover")
        btn_wireless.connect('clicked', self.on_wireless)
        row.pack_start(btn_wireless, False, False, 0)

        grid = Gtk.Grid(column_spacing=6, row_spacing=6)
        main.pack_start(grid, False, False, 0)

        grid.attach(Gtk.Label(label="Preset:"), 0, 0, 1, 1)
        self.preset = Gtk.ComboBoxText()
        self.preset.append_text("Low (480p, 1M)")
        self.preset.append_text("Medium (720p, 2.5M)")
        self.preset.append_text("High (1024p, 8M)")
        self.preset.set_active(1)
        grid.attach(self.preset, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Max Size (0 = no limit):"), 0, 1, 1, 1)
        self.entry_max = Gtk.Entry()
        self.entry_max.set_text("0")
        grid.attach(self.entry_max, 1, 1, 1, 1)

        grid.attach(Gtk.Label(label="Bitrate (e.g. 2M):"), 0, 2, 1, 1)
        self.entry_bitrate = Gtk.Entry()
        self.entry_bitrate.set_text("2M")
        grid.attach(self.entry_bitrate, 1, 2, 1, 1)

        self.record_check = Gtk.CheckButton(label="Record session")
        grid.attach(self.record_check, 0, 3, 2, 1)

        grid.attach(Gtk.Label(label="Record filename:"), 0, 4, 1, 1)
        self.record_file = Gtk.Entry()
        self.record_file.set_text("dilip_record.mp4")
        grid.attach(self.record_file, 1, 4, 1, 1)

        buttons = Gtk.Box(spacing=6)
        main.pack_start(buttons, False, False, 0)

        self.start_btn = Gtk.Button(label="Start Mirror")
        self.start_btn.connect("clicked", self.start_mirror)
        buttons.pack_start(self.start_btn, True, True, 0)

        self.stop_btn = Gtk.Button(label="Stop")
        self.stop_btn.set_sensitive(False)
        self.stop_btn.connect("clicked", self.stop_mirror)
        buttons.pack_start(self.stop_btn, True, True, 0)

        frame = Gtk.Frame(label="Logs")
        main.pack_start(frame, True, True, 0)

        scroll = Gtk.ScrolledWindow()
        frame.add(scroll)

        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.buffer = self.text_view.get_buffer()
        scroll.add(self.text_view)

        self.spinner = Gtk.Spinner()
        hb.pack_start(self.spinner)

        self.scrcpy_proc = None
        self.adb = shutil.which("adb")
        self.scrcpy = shutil.which("scrcpy")

        self.connect("delete-event", Gtk.main_quit)
        GLib.idle_add(self.on_refresh, None)

    def log(self, m):
        end = self.buffer.get_end_iter()
        self.buffer.insert(end, m + "\n")

    def on_refresh(self, *_):
        self.device_combo.remove_all()
        if not self.adb:
            self.device_combo.append_text("adb not found")
            self.device_combo.set_active(0)
            return

        try:
            out = subprocess.check_output([self.adb, "devices"], text=True)
        except:
            self.device_combo.append_text("adb error")
            self.device_combo.set_active(0)
            return

        added = False
        for l in out.splitlines():
            if "\tdevice" in l:
                serial = l.split("\t")[0]
                self.device_combo.append_text(serial)
                added = True

        if not added:
            self.device_combo.append_text("No devices")
        self.device_combo.set_active(0)
        self.log("Devices refreshed.")

    def on_wireless(self, *_):
        self.log("Enable wireless: adb tcpip 5555, then adb connect <IP>")

    def build_cmd(self):
        d = self.device_combo.get_active_text()
        if not d or d.startswith("No"):
            return None

        p = self.preset.get_active_text()
        if "Low" in p:
            size, br = "480", "1M"
        elif "High" in p:
            size, br = "1024", "8M"
        else:
            size, br = "720", "2.5M"

        if self.entry_max.get_text().strip() not in ("", "0"):
            size = self.entry_max.get_text().strip()

        if self.entry_bitrate.get_text().strip():
            br = self.entry_bitrate.get_text().strip()

        cmd = [self.scrcpy, "--serial", d, "--max-size", size, "--bit-rate", br, "--window-title", APP_TITLE]

        if self.record_check.get_active():
            fname = self.record_file.get_text().strip() or "dilip_record.mp4"
            cmd += ["--record", fname]

        return cmd

    def start_mirror(self, *_):
        if not self.scrcpy:
            self.log("scrcpy missing")
            return

        cmd = self.build_cmd()
        if not cmd:
            self.log("No device selected")
            return

        self.log("Running: " + " ".join(cmd))
        self.spinner.start()
        self.start_btn.set_sensitive(False)
        self.stop_btn.set_sensitive(True)

        def worker():
            try:
                self.scrcpy_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in self.scrcpy_proc.stdout:
                    GLib.idle_add(self.log, line.rstrip())
            except Exception as e:
                GLib.idle_add(self.log, "Error: " + str(e))
            finally:
                GLib.idle_add(self.spinner.stop)
                GLib.idle_add(self.start_btn.set_sensitive, True)
                GLib.idle_add(self.stop_btn.set_sensitive, False)

        threading.Thread(target=worker, daemon=True).start()

    def stop_mirror(self, *_):
        if self.scrcpy_proc and self.scrcpy_proc.poll() is None:
            self.scrcpy_proc.terminate()
        self.log("Stopped.")
        self.spinner.stop()


if __name__ == "__main__":
    win = MobileMirrorApp()
    win.show_all()
    Gtk.main()
