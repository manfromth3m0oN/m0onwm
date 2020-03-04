# Basic X imports
from Xlib import X, XK
from Xlib.display import Display

# Subprocess to actually run programs
import subprocess

display = Display() # init display
rootwindow = display.screen().root # init root window
rootwindow.change_attributes(event_mask = X.SubstructureRedirectMask) # Add a mask that im not quite sure the function of

mod = X.Mod4Mask # Mod is Win/Super key
workspaces = {}
ws = '1'
# Get the keycode of a specific key
def getcode(key):
    codes= set(code for code, index in display.keysym_to_keycodes(key))
    return int(next(iter(codes)))

# Configure keybinds
def configk():
    # Each key in this list is a HK
    grabbedKeys = [XK.XK_Return, XK.XK_D, XK.XK_Tab, XK.XK_Q, XK.XK_H, XK.XK_J, XK.XK_K, XK.XK_L, XK.XK_1, XK.XK_2, XK.XK_3, XK.XK_4, XK.XK_5, XK.XK_P, XK.XK_U, XK.XK_O, XK.XK_I]
    for keyBinding in grabbedKeys:
        code = getcode(keyBinding)
        rootwindow.grab_key(code, mod, 1, X.GrabModeAsync, X.GrabModeAsync)
        
# Handle keypress events
def kp(event):
    print(event.detail)
    if event.detail == getcode(XK.XK_Return): run('urxvt')
    if event.detail == getcode(XK.XK_D): run('rofi -show run')
    if event.detail == getcode(XK.XK_Tab): switchfocus()
    if event.detail == getcode(XK.XK_Q): windowClose()
    # if event.detail == getcode(XK.XK_H): movewinx(-10)
    # if event.detail == getcode(XK.XK_L): movewinx(10)
    # if event.detail == getcode(XK.XK_K): movewiny(10)
    # if event.detail == getcode(XK.XK_J): movewiny(-10)
    if event.detail == getcode(XK.XK_1): showws('1')
    if event.detail == getcode(XK.XK_2): showws('2')
    if event.detail == getcode(XK.XK_3): showws('3')
    if event.detail == getcode(XK.XK_4): showws('4')
    if event.detail == getcode(XK.XK_5): showws('5')
    # if event.detail == getcode(XK.XK_P): width(10)
    # if event.detail == getcode(XK.XK_U): width(-10)
    # if event.detail == getcode(XK.XK_O): height(10)
    # if event.detail == getcode(XK.XK_I): height(-10)

# Create the workspace dictionary
def genworkspaces(ws):
    for i in ws:
        workspaces.update({i: []})

# Change focus to the next window
def switchfocus():
    if len(workspaces[ws]) > 1:
        focus = display.get_input_focus().focus
        index = workspaces[ws].index(focus)
        target = index + 1
        if target >= len(workspaces[ws]): target = 0
        display.set_input_focus(workspaces[ws][target], X.RevertToParent, 0)
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
    if len(workspaces[ws]) >= 1:
        print('Falling back to previous window')
        index = workspaces[ws].index(focus)
        print(index)
        target = index - 1
        print(target)
        if target >= len(workspaces[ws]): target = 0
        display.set_input_focus(workspaces[ws][target], X.RevertToParent, 0)
        focus.destroy()
        workspaces[ws].remove(focus)
    else:
        print('falling back to root window')
        display.set_input_focus(X.PointerRoot, X.RevertToParent, 0)
        focus.destroy()
        workspaces[ws].remove(focus)

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
    print(event.window)
    assigntows(event.window, ws)
    event.window.map()
    event.window.set_input_focus(X.RevertToParent, X.CurrentTime)
    event.window.configure(stack_mode = X.Above)

# Assign a window to a workspace
def assigntows(window, workspace):
    if window not in workspaces[workspace]:
        workspaces[workspace].append(window)
    else:
        print('Window already in a workspace')

# map all windows in a workspace
def showws(wsto):
    global ws
    for window in workspaces[ws]:
        window.unmap()
    ws = wsto
    for window in workspaces[wsto]:
        root = rootwindow.get_geometry()
        print(root.width)
        print(root.height)
        window.configure(width = root.width, height = root.height)
        window.map()
        window.set_input_focus(X.RevertToParent, X.CurrentTime)

# Add or remove a variable number of pixels to a windows width
def width(pixels):
    focus = display.get_input_focus().focus
    windowGeometry = focus.get_geometry()
    focus.configure(width = windowGeometry.width + pixels)

# Add or remove a variable number of pixels to a windows width
def height(pixels):
    focus = display.get_input_focus().focus
    windowGeometry = focus.get_geometry()
    focus.configure(height = windowGeometry.height + pixels)

def autostart():
    run('wal -R')

# The main loop
def main():
    configk()
    genworkspaces('1234567890')
    autostart()
    while True:
        if True:
            print(workspaces)
            event = display.next_event()
            if event.type == X.KeyPress: kp(event)
            elif event.type == X.MapRequest: me(event)

main()