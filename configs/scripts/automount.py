#!/usr/bin/env python3
from gi.repository import Gio, GLib


def volume_added(_monitor, volume):
    if not volume.can_mount():
        return

    if volume.get_mount() is not None:
        return

    if not volume.should_automount():
        return

    print(f"Подключаю: {volume.get_name()}")

    def finished(vol, result):
        try:
            vol.mount_finish(result)
            mount = vol.get_mount()
            if mount:
                print(f"Подключено: {mount.get_root().get_path()}")
        except GLib.Error as error:
            print(f"Ошибка подключения {vol.get_name()}: {error.message}")

    volume.mount(
        Gio.MountMountFlags.NONE,
        None,
        None,
        finished,
    )


monitor = Gio.VolumeMonitor.get()
monitor.connect("volume-added", volume_added)

loop = GLib.MainLoop()
loop.run()
