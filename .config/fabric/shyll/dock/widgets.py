import os
from functools import partial

from .service import GnomeFavAppsService

from fabric.widgets.button import Button
from fabric.widgets.box import Box

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Gio, GioUnix, GLib

gnome_fav_apps_service: GnomeFavAppsService | None = None


def get_gnome_favs_apps_service():
    global gnome_fav_apps_service
    
    if not gnome_fav_apps_service:
        gnome_fav_apps_service = GnomeFavAppsService()
    
    return gnome_fav_apps_service


class AppButton(Button):
    def __init__(self, app: GioUnix.DesktopAppInfo):
        self._app: GioUnix.DesktopAppInfo = app

        super().__init__(
            image=Gtk.Image.new_from_gicon(
                self._app.get_icon(),
                Gtk.IconSize.BUTTON
            )
        )

        self.connect("button-press-event", self.on_clicked)
    
    def on_clicked(self, _, event):
        match event.button:
            case 1:
                self._app.launch()
            
            case 3:
                self.menu = Gtk.Menu.new()

                list_actions = self._app.list_actions()

                if list_actions:
                    for action_name in list_actions:
                        action_nice_name = self._app.get_action_name(action_name)
                        menu_item = Gtk.MenuItem.new_with_label(action_nice_name)
                        menu_item.connect(
                            "activate",
                            partial(self.on_action_clicked, action_name)
                        )
                        menu_item.show()
                        self.menu.append(menu_item)

                    self.menu.popup_at_pointer()

    def on_action_clicked(self, action_name: str, menu_item: Gio.MenuItem):
        self._app.launch_action(action_name, None)


class AppsDock(Box):
    def __init__(self):
        super().__init__(orientation="v")

        service = get_gnome_favs_apps_service()
        for a in service.apps:
            app_btn = AppButton(a)
            self.add(app_btn)
