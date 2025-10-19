import fabric
from fabric import Application
from fabric.widgets.datetime import DateTime
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.hyprland.widgets import HyprlandWorkspaces, WorkspaceButton
from fabric.system_tray.widgets import SystemTray
from fabric.hyprland.service import Hyprland

from fabric.utils import FormattedString, get_relative_path, bulk_replace

from shyll.dock.widgets import AppsDock

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

try:
    gi.require_version("GtkLayerShell", "0.1")
    from gi.repository import GtkLayerShell
except:
    raise ImportError(
        "looks like we don't have gtk-layer-shell installed, make sure to install it first (as well as using wayland)"
    )


WORKSPACES = {
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    11: "",
    12: "",
    13: ""
}
WORKSPACES_PER_MONITOR = {
    0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    1: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
}

class StatusBar(Window):
    def __init__(self, **kwargs):
        super().__init__(
            layer="top",
            anchor="top left bottom",
            exclusivity="auto",
            all_visible=True,
            **kwargs
        )

        self.date_time = DateTime(
            formatters=(
                "%H\n%M",
                "%m\n%d\n%y"
            )
        )

        self.sys_tray = SystemTray(
            icon_size=16,
            orientation="v",
        )

        self.workspaces = HyprlandWorkspaces(
            name="workspaces",
            spaces=4,
            orientation="v",
            buttons_factory=lambda ws_id: WorkspaceButton(
                ws_id,
                label=str(WORKSPACES.get(ws_id, ws_id)),
            ) if ws_id in WORKSPACES_PER_MONITOR.get(self.monitor, []) else None
        )

        self.apps_dock = AppsDock()

        self.children = CenterBox(
            name="bar_inner",
            orientation="vertical",

            start_children=Box(
                name="start_container",
                orientation="v",
                children=[
                    self.workspaces,
                ],
            ),

            center_children=Box(
                name="center_container",
                orientation="v",
                children=[
                    self.apps_dock,
                ],
            ),

            end_children=Box(
                name="end_container",
                orientation="v",
                children=[
                    self.sys_tray,
                    self.date_time,
                ],
            )
        )

        return self.show_all()
    

if __name__ == "__main__":
    bars = []

    for i in range(Gdk.Screen.get_default().get_n_monitors()):
        bars.append(StatusBar(monitor=i))
        
    app = Application("shyll", *bars)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    app.run()