import gi
gi.require_version("Gtk", "3.0")

from typing import List
from fabric.core.service import Service, Signal, Property

from .helpers import get_favorite_apps

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Gio, GioUnix, GLib



class GnomeFavAppsService(Service):

    @Signal
    def changed(self) -> None:
        pass

    @Property(List[GioUnix.DesktopAppInfo], flags="read-write")
    def apps(self) -> List[GioUnix.DesktopAppInfo]:
        return self._apps

    @apps.setter
    def apps(self, value: List[GioUnix.DesktopAppInfo]):
        self._apps = value
        self.changed(value)

    def __init__(self):
        super().__init__()
        self._apps = list(get_favorite_apps())
