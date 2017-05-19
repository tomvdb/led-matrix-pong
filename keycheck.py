from evdev import InputDevice, categorize, ecodes, KeyEvent
from select import select

#gamepad = InputDevice('/dev/input/event0')
devices = map(InputDevice, ('/dev/input/event0', '/dev/input/event1'))
devices = {dev.fd: dev for dev in devices}


for dev in devices.values(): 
	print(dev)


while True:
	print "ping"
	r, w, x = select(devices, [], [], 0)
    	for fd in r:
           for event in devices[fd].read():
		print fd	
                print(event)
#unique code

#for event in gamepad.read_loop():

#	if event.code == 16:
#		print ("%" )
#		print(event.code)
#		print(event.value)

