# Basic X imports
from Xlib import X, XK
from Xlib.display import Display

# Subprocess to actually run programs
import subprocess

display = Display() # init display
rootwindow = display.screen().root # init root window
rootwindow.change_attributes(event_mask = X.SubstructureRedirectMask) # Add a mask that im not quite sure the function of

mod = X.Mod4Mask # Mod is Win/Super key
windowlist = []
workspaces = {}
# Get the keycode of a specific key
def getcode(key):
    codes= set(code for code, index in display.keysym_to_keycodes(key))
    return int(next(iter(codes)))

# Configure keybinds
def configk():
    grabbedKeys = [XK.XK_Return, XK.XK_D, XK.XK_Tab, XK.XK_Q, XK.XK_H, XK.XK_J, XK.XK_K, XK.XK_L] # Each key in this list is a HK
    for keyBinding in grabbedKeys:
        code = getcode(keyBinding)
        rootwindow.grab_key(code, mod, 1, X.GrabModeAsync, X.GrabModeAsync)
        
# Handle keypress events
def kp(event):
    if event.detail == getcode(XK.XK_Return): run('urxvt')
    if event.detail == getcode(XK.XK_D): run('rofi -show run')
    if event.detail == getcode(XK.XK_Tab): switchfocus()
    if event.detail == getcode(XK.XK_Q): windowClose()
    if event.detail == getcode(XK.XK_H): movewinx(-10)
    if event.detail == getcode(XK.XK_L): movewinx(10)
    if event.detail == getcode(XK.XK_K): movewiny(10)
    if event.detail == getcode(XK.XK_J): movewiny(-10)

# Create the workspace dictionary
def genworkspaces(ws):
    for i in ws:
        workspaces.update({i: []})

# Change focus to the next window
def switchfocus():
    if len(windowlist) > 1:
        focus = display.get_input_focus().focus
        index = windowlist.index(focus)
        target = index + 1
        if target >= len(windowlist): target = 0
        display.set_input_focus(windowlist[target], X.RevertToParent, 0)
        newfocus = display.get_input_focus().focus
        newfocus.configure(stack_mode=X.Above)
    else:
        print('No window to switch to')

# A wrapper for subprocess.Popen
def run(command):
    commandlist = command.split(' ')
    subprocess.Popen(commandlist)

# Close the currently focused window
def windowClose():
    focus = display.get_input_focus().focus
    focus.destroy()
    if len(windowlist) > 1:
        index = windowlist.index(focus)
        target = index - 1
        if target >= len(windowlist): target = 0
        windowlist.remove(focus)
        display.set_input_focus(windowlist[target], X.RevertToParent, 0)
    else:
        display.set_input_focus(X.PointerRoot, X.RevertToParent, 0)

# Move the window by a variable number of pixels in the x direction
def movewinx(pixels):
    focus = display.get_input_focus().focus
    windowGeometry = focus.get_geometry()
    focus.configure(x = windowGeometry.x + pixels)

# Move the curently focused window by a variable number of pixels in the y direction
def movewiny(pixels):
    focus = display.get_input_focus().focus
    windowGeometry = focus.get_geometry()
    focus.configure(y = windowGeometry.y + pixels)

# Handle map event
def me(event):
    event.window.map()
    event.window.set_input_focus(X.RevertToParent, X.CurrentTime)
    event.window.configure(stack_mode = X.Above)
    windowlist.append(event.window)

# Assign a window to a workspace
def assigntows(window, workspace):
    if window not in workspaces[workspace]:
        workspaces[workspace].append(window)
    else:
        print('Window already in a workspace')

# map all windows in a workspace
def showws(ws):
    for window in workspaces[ws]:
        window.map

# The main loop
def main():
    configk()
    genworkspaces('1234567890')
    subprocess.Popen(['wal', '-R'])
    subprocess.Popen(['xrdb', '~/.Xresources'])
    while True:
        if True:
            event = display.next_event()
            if event.type == X.KeyPress: kp(event)
            elif event.type == X.MapRequest: me(event)

main()