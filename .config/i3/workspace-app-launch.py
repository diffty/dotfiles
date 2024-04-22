import os

from i3ipc import Connection


i3 = Connection()
focused = i3.get_tree().find_focused()

workspace_app = {
    1: "code",
    2: "firefox",
    3: "kitty",
    4: "cider",
    5: "obsidian",
    7: "kitty",
    8: "keepassxc",
}

if focused:
    exec_name = workspace_app.get(focused.workspace().num, None)
    if exec_name:
        os.system(exec_name)
