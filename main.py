# Basic X imports
from Xlib import X, XK
from Xlib.display import Display

# Subprocess to actually run programs
import subprocess

# ptvsd for debugging
import ptvsd

# 5678 is the default attach port in the VS Code debug configurations
print("Waiting for debugger attach")
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()

display = Display() # init display
rootwindow = display.screen().root # init root window
rootwindow.change_attributes(event_mask = X.SubstructureRedirectMask) # Add a mask that im not quite sure the function of

# Global variables
mod = X.Mod4Mask # Mod is Win/Super key
workspaces = {} # A dictionary of workspaces
ws = '1' # default current workspace
prefssize = [] # the size of the focused window before fullscreening
grabwindow = None # Which window has been grabbed for moving
gap = 10 # Number of pixels for the gap
barHeight = 0 # Offset for if there were to be a bar (e.g. polybar)

# Get the keycode of a specific key
def getcode(key):
	codes= set(code for code, index in display.keysym_to_keycodes(key))
	return int(next(iter(codes)))

# Configure keybinds
def configk():
	# Each key in this list is a HK
	grabbedKeys = [XK.XK_Return, XK.XK_D, XK.XK_Tab,
					XK.XK_Q, XK.XK_H, XK.XK_J,
					XK.XK_K, XK.XK_L, XK.XK_1,
					XK.XK_2, XK.XK_3, XK.XK_4,
					XK.XK_5, XK.XK_P, XK.XK_U,
					XK.XK_O, XK.XK_I, XK.XK_F
				]
	for keyBinding in grabbedKeys:
		code = getcode(keyBinding)
		rootwindow.grab_key(code, mod, 1, X.GrabModeAsync, X.GrabModeAsync)

# Handle keypress events
def kp(event):
	print(event.window)
	if event.detail == getcode(XK.XK_Return): run('kitty')
	if event.detail == getcode(XK.XK_D): run('dmenu_run')
	if event.detail == getcode(XK.XK_Tab): switchfocus()
	if event.detail == getcode(XK.XK_Q): windowClose()
	if event.detail == getcode(XK.XK_H): movewinx(-10)
	if event.detail == getcode(XK.XK_L): movewinx(10)
	if event.detail == getcode(XK.XK_K): movewiny(10)
	if event.detail == getcode(XK.XK_J): movewiny(-10)
	if event.detail == getcode(XK.XK_1): showws('1')
	if event.detail == getcode(XK.XK_2): showws('2')
	if event.detail == getcode(XK.XK_3): showws('3')
	if event.detail == getcode(XK.XK_4): showws('4')
	if event.detail == getcode(XK.XK_5): showws('5')
	if event.detail == getcode(XK.XK_P): width(10)
	if event.detail == getcode(XK.XK_U): width(-10)
	if event.detail == getcode(XK.XK_O): height(10)
	if event.detail == getcode(XK.XK_I): height(-10)
	if event.detail == getcode(XK.XK_F): fullscreen()

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
		if len(workspaces[ws]) != 0:
			print('falling back to root window')
			display.set_input_focus(X.PointerRoot, X.RevertToParent, 0)
			focus.destroy()
			workspaces[ws].remove(focus)
		else:
			print('No window to be destoryed')

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
	print('Map Event: ')
	print(event.window)
	assigntows(event.window, ws)
	event.window.map()
	event.window.set_input_focus(X.RevertToParent, X.CurrentTime)
	#breakpoint()
	# print(len(workspaces[ws]))
	# desiredWidth = round((rootwindow.get_geometry().width - (2 * gap)) / len(workspaces[ws]))
	# desiredHeight = round((rootwindow.get_geometry().height - ((2 * gap) + barHeight)) / len(workspaces[ws]))
	# print('Desired width and height: ', desiredWidth, ' ', desiredHeight)
	# event.window.configure(stack_mode = X.Above, width=desiredWidth, height=desiredHeight, x=gap, y=gap + barHeight)
	tile()
	configuremouse(event.window)

# Tile all windows in current workspace
def tile():
	if len(workspaces[ws]) == 1:
		width = rootwindow.get_geometry().width - (2 * gap)
		height = rootwindow.get_geometry().height - ((2 * gap) + barHeight)
		workspaces[ws][0].configure(stack_mode = X.Above, width=width, height=height, x=gap, y=gap + barHeight)
	elif len(workspaces[ws]) > 1:
		print(workspaces[ws])
		if len(workspaces[ws]) == 2:
			# First window
			width = round((rootwindow.get_geometry().width / 2) - gap)
			height = (rootwindow.get_geometry().height) - (2 * gap)
			workspaces[ws][0].configure(stack_mode = X.Above, width=width, height=height, x=gap, y=gap + barHeight)
			# Second window
			width = round((rootwindow.get_geometry().width / 2) - gap)
			height = (rootwindow.get_geometry().height) - (2 * gap)
			x = (rootwindow.get_geometry().width / 2)
			y = rootwindow.get_geometry().height
			workspaces[ws][1].configure()

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

# make the currently focused window full screen
def fullscreen():
	global prefssize
	focus = display.get_input_focus().focus
	rootGeometry = rootwindow.get_geometry()
	focusGeometry = focus.get_geometry()
	if focusGeometry.width != rootGeometry.width and focusGeometry.height != rootGeometry.height:
		prefssize = [focusGeometry.x, focusGeometry.y, focusGeometry.width, focusGeometry.height]
		focus.configure(x = 0, y = 0, width = rootGeometry.width, height = rootGeometry.height)
		focus.change_attributes(win_gravity=X.NorthWestGravity, bit_gravity=X.StaticGravity)
	else:
		focus.configure(x=prefssize[0], y=prefssize[1], width=prefssize[2], height=prefssize[3])
	
def mousehandler(event):
	global grabwindow
	print('grabwindow: '+str(grabwindow))
	print('Event type: '+str(event.type)+' | Button press: '+str(event.detail))
	if event.detail == 0 and event.type == X.MotionNotify: # X.MotionNotify == 6
		if grabwindow != None:
			print('grabbing window: '+str(event.window))
			grabwindow = event.window
			windowGeometry = grabwindow.get_geometry()
			moveX = windowGeometry.x - event.root_x
			moveY = windowGeometry.y - event.root_y
			print('X: '+str(moveX)+' Y: '+str(moveY))
		else:
			# print('moving window: '+str(event.window))
			# grabwindow.configure(x=moveX+event.root_x, y=moveY+event.root_y)
			pass
	elif event.type == X.ButtonRelease:
		grabwindow = None
	elif event.detail == 2 and event.type == X.ButtonPress:
		event.window.set_input_focus(X.RevertToParent, X.CurrentTime)
		event.window.configure(stack_mode=X.Above)

def configuremouse(window):
	print('configuring mouse')
	window.grab_button(0, mod, True,
		X.Button1MotionMask | X.ButtonReleaseMask | X.ButtonPressMask,
		X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE, None)

def autostart():
	run('wal -R')
	run('xrdb /home/m0on/.Xresources')

# The main loop
def main():
	configk()
	genworkspaces('1234567890')
	autostart()
	while True:
		if True:
			event = display.next_event()
			print('Event: '+str(event.type))
			if event.type == X.KeyPress: kp(event)
			elif event.type == X.MapRequest: me(event)
			elif event.type == X.ButtonPress: mousehandler(event)
			elif event.type == X.ButtonRelease: mousehandler(event)
			elif event.type == X.MotionNotify: mousehandler(event) 

main()
