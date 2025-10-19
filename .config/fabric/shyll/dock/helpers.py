import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Gio, GioUnix, GLib


def get_favorite_apps():
    shell_settings = Gio.Settings.new("org.gnome.shell")
    for a in shell_settings["favorite-apps"]:
        try:
            yield GioUnix.DesktopAppInfo.new(a)
        except TypeError as e:
            pass