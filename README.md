# A basic python-xlib window manager

TODO:
* Document almost everything

## Keybinds

To edit the keybinds first add the key to the `grabbedKeys` list.
After which you need to define its functionality in the `kp()` function

## Workspaces

To change the names of the workspaces the `genworkspaces()` call needs to be changed and some minor adjustments to accept words or short collections of chars to use as ws names

## Mapping of windows for workspaces

When a window is created it needs to be mapped to be visible.

The current mapping implamentation is very limited as it maps a window as soon as the window is created.
For the window manager to respect workspaces, it must only map windows within the current workspace.

The first step is for when process is spawned, if it sends a map request, the request is to be sent to a method which determines which workspace it is to be placed into. This could allow for programs to be opened onto other workspaces from the current one.

Then by looping through the windows atributed to a certian workspace, once a workspace is opened, each window will be mapped with the `Window.map()` method

When leaving a workspace all open programs will be unmapped with `Window.unmap()`

## Conceptualising how tiling should work

lets say we have 4 windows. we are aiming for a layout that looks like this:
```
+-------------------------------------------------------------------------------------------+
|---------------------------------------------+ +-------------------------------------------|
||                                            | |                                          ||
||                                            | |                                          ||
||                                            | |                  ____                    ||
||                                            | |                 |  _ \                   ||
||                                            | |                 | |_) |                  ||
||                                            | |                 |  _ <                   ||
||                                            | |                 | |_) |                  ||
||                                            | |                 |____/                   ||
||                                            | |                                          ||
||                    /\                      | |                                          ||
||                   /  \                     | |                                          ||
||                  / /\ \                    | +-------------------------------------------+
||                 / ____ \                   | +--------------------+  +-----------------+ |
||                /_/    \_\                  | |                    |  |                 | |
||                                            | |                    |  |                 | |
||                                            | |         _____      |  |     _____       | |
||                                            | |        / ____|     |  |    |  __ \      | |
||                                            | |       | |          |  |    | |  | |     | |
||                                            | |       | |          |  |    | |  | |     | |
||                                            | |       | |____      |  |    | |__| |     | |
||                                            | |        \_____|     |  |    |_____/      | |
||                                            | |                    |  |                 | |
||                                            | |                    |  |                 | |
||                                            | |                    |  |                 | |
|---------------------------------------------+ +--------------------+  +-----------------+ |
+-------------------------------------------------------------------------------------------+
```
So; A is half of the screen
    B is a quater of the screen
    C & D are an eight respectively

programatically this would mean:
* first we need to get the geometery of the root window with `root.get_geometry()`
* next we iterate through the list of windows in the workspace
    * in this system A always takes up 50% of the screen (if there are other windows open in the ws)
    so we take the root window size and divide it by 2 then make the windows x & y these values
    * now we have the other half of the screen left therefore all y values will be offset by the root width/2 
    now the overall screen space is half of what it was so we will treat root width and height as half of what their values are
    

full screen = 1280x720
half screen = 640x360
quater screen = 320x180


## Install

Requirements:
```
Xlib
```

To install clone the repo and put this in your `.xinitrc`
```
exec python /path/to/m0onwm/main.py
```