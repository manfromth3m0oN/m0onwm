# A basic python-xlib window manager

TODO:
* Document almost everything

## Keybinds

To edit the keybinds first add the key to the `grabbedKeys` list.
After which you need to define its functionality in the `kp()` function


## Mapping of windows for workspaces

When a window is created it needs to be mapped to be visible.

The current mapping implamentation is very limited as it maps a window as soon as the window is created.
For the window manager to respect workspaces, it must only map windows within the current workspace.

The first step is for when process is spawned, if it sends a map request, the request is to be sent to a method which determines which workspace it is to be placed into. This could allow for programs to be opened onto other workspaces from the current one.

Then by looping through the windows atributed to a certian workspace, once a workspace is opened, each window will be mapped with the `Window.map()` method

When leaving a workspace all open programs will be unmapped with `Window.unmap()`