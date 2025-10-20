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

        icon_image = Gtk.Image.new_from_gicon(
            self._app.get_icon(),
            Gtk.IconSize.LARGE_TOOLBAR,
        )

        super().__init__(
            image=icon_image
        )

        self.connect("button-release-event", self.on_clicked)
        self.connect("drag-data-get", self.on_drag_data_get)
        self.connect("drag-data-received", self.on_drag_received)
        
        self.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK,
            targets=[Gtk.TargetEntry.new("text/plain", 0, 0)],
            actions=Gdk.DragAction.MOVE,
        )

        self.drag_dest_set(
            flags=Gtk.DestDefaults.ALL,
            targets=[Gtk.TargetEntry.new("text/plain", 0, 0)],
            actions=Gdk.DragAction.MOVE,
        )

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

    def on_drag_data_get(
            self,
            widget,
            context: Gdk.DragContext,
            selection_data: Gtk.SelectionData,
            info: int,
            time_: int):
        pass
            
    def on_drag_received(self, *args, **kwargs):
        print("received", args, kwargs)
    

class AppsDock(Box):
    def __init__(self, **kwargs):
        super().__init__(orientation="v", **kwargs)

        service = get_gnome_favs_apps_service()
        for a in service.apps:
            app_btn = AppButton(a)
            self.add(app_btn)
