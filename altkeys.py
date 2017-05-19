from evdev import InputDevice
from selectors import DefaultSelector, EVENT_READ

selector = DefaultSelector()

mouse = InputDevice('/dev/input/event0')
keybd = InputDevice('/dev/input/event1')

# This works because InputDevice has a `fileno()` method.
selector.register(mouse, EVENT_READ)
selector.register(keybd, EVENT_READ)

while True:
	for key, mask in selector.select():
		device = key.fileobj
		for event in device.read():
			print(event)
	print ("ping" )