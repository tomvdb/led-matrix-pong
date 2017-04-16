import serial
import pygame
import time
import evdev

numpixels = 42 * 24

ser = serial.Serial()
ser.baudrate = 19200
ser.port = '/dev/ttyACM0'
ser.open()

pygame.init()

clock = pygame.time.Clock()

device = evdev.InputDevice('/dev/input/event0')
print device



matrix = list()

for num in range(0, numpixels):
	matrix.append(0)
        matrix.append(0)
        matrix.append(0)


ballX = 0
ballY = 0
ballXDir = 1
ballYDir = 1

clock_font = [
  0x1F, 0x11, 0x1F,
  0x00, 0x00, 0x1F,
  0x1D, 0x15, 0x17,
  0x15, 0x15, 0x1F,
  0x07, 0x04, 0x1F,
  0x17, 0x15, 0x1D,
  0x1F, 0x15, 0x1D,
  0x01, 0x01, 0x1F,
  0x1F, 0x15, 0x1F,
  0x17, 0x15, 0x1F]

mask = bytearray([1,2,4,8,16,32,64,128])

def drawField():
	for i in range(0,42):
		drawPixel(i, 0, 150,150,150)
		drawPixel(i, 23, 150,150,150)

	for i in range(0,24,2):
		drawPixel(21, i, 150, 150, 150)

def drawNumber(number,offsetx,offsety,r,g,b):
    	for x in range(0,3):
        	for y in range(0,5):
            		if clock_font[3*number + x]&mask[y]:
                		drawPixel(offsetx+x,offsety+y,r,g,b)

def drawScore(p1, p2):
	drawNumber( p1, 17, 2, 150, 150, 150)
	drawNumber( p2, 23, 2, 150, 150, 150)

def clearDisplay( pr, pg, pb ):
#	for cnum in range(0, numpixels, 3):
#        	matrix[cnum] = pr
#	        matrix[cnum+1] = pg
#        	matrix[cnum+2] = pb

	for x in range(0,42):
		for y in range(0,24):
			drawPixel(x,y, pr, pg, pb )
#	print matrix	
	

def drawPixel( px, py, pr, pg, pb ):

	if py % 2 > 0:
		px = 41 - px

	val = 42 * py
	val = val + px
	val = val * 3

	matrix[val] = pr
	matrix[val + 1] = pg
	matrix[val + 2] = pb

def updateDisplay():
	values = bytearray(matrix)
	ser.write("\x01")
	ser.write(str(values))

done = False

updateCounter = 0
numberCount = 0

clearDisplay( 0, 150, 0 )

paddle1Y = 11
paddle2Y = 11

player1Score = 0
player2Score = 0

ballX = 24
ballY = 12

while done == False:
	try:
		for event in device.read():
			if event.type == evdev.ecodes.EV_KEY:
#				print event.code
				if event.code == 105 and paddle2Y > 3:
					paddle2Y = paddle2Y - 1
				if event.code == 106 and paddle2Y < 20:
					paddle2Y = paddle2Y + 1
				if event.code == 45 and paddle1Y > 3:
					paddle1Y = paddle1Y - 1
				if event.code == 44 and paddle1Y < 20:
					paddle1Y = paddle1Y + 1


	except IOError:
		a = 1

#	for event in pygame.event.get():
#		if event.type == pygame.QUIT:
#			done = True
#		if event.type == pygame.KEYDOWN:
#			print "key pressed"
#			if event.key == pygame.K_UP:
#				numberCount = numberCount + 1
#			if event.key == pygame.K_DOWN:
#				numberCount = numberCount - 1
					

	clearDisplay(0, 0, 150)

#	drawNumber(numberCount, 10, 10, 150, 0, 0 )

	drawPixel( 1, paddle1Y-1, 150, 150, 150 )
	drawPixel( 1, paddle1Y-2, 150, 150, 150 )
	drawPixel( 1, paddle1Y+1, 150, 150, 150 )
	drawPixel( 1, paddle1Y+2, 150, 150, 150 )
	drawPixel( 1, paddle1Y, 150, 150, 150 )

	drawPixel( 40, paddle2Y-1, 150, 150, 150 )
	drawPixel( 40, paddle2Y-2, 150, 150, 150 )
	drawPixel( 40, paddle2Y+1, 150, 150, 150 )
	drawPixel( 40, paddle2Y+2, 150, 150, 150 )
	drawPixel( 40, paddle2Y, 150, 150, 150 )


	drawField()
	drawScore( player2Score, player1Score )


	drawPixel( ballX, ballY, 0, 150, 150 )

	


	if ballX == 2 and ballY >= paddle1Y - 2 and ballY <= paddle1Y + 2:
		ballXDir = 1

	if ballX == 39 and ballY >= paddle2Y - 2 and ballY <= paddle2Y + 2:
		ballXDir = -1

	if ballX == 0:
		ballX = 24
		ballY = 12
		player1Score = player1Score + 1

	if ballX == 41:
		ballX = 24
		ballY = 12
		player2Score = player2Score + 1
		

	updateCounter = updateCounter + 1;
	
	if updateCounter > 5:

#	        ltime =  time.localtime()
#	        hour = ltime.tm_hour
#	        minute= ltime.tm_min
#	        second= ltime.tm_sec

#	        drawNumber(int(hour/10),2,1,0,150,0)
#	        drawNumber(int(hour%10),6,1,0,150,0)
#	        drawNumber(int(minute/10),2,8,0,150,0)
#	        drawNumber(int(minute%10),6,8,0,150,0)
#	        drawNumber(int(second/10),2,15,0,150,0)
#	        drawNumber(int(second%10),6,15,0,150,0)		

		updateCounter = 0
		ballX = ballX + ballXDir
		ballY = ballY + ballYDir

		if ballX > 40:
#			numberCount = numberCount + 1
			ballXDir = -1

		if ballX < 2:
#			numberCount = numberCount + 1
			ballXDir = 1

		if ballY > 21:
#			numberCount = numberCount + 1
			ballYDir = -1

		if ballY < 2:
#			numberCount = numberCount + 1
			ballYDir = 1


#		print "(" + str(ballX) + "," + str(ballY) + ")" + str(ballXDir) + "," + str(ballYDir)

	updateDisplay()

	clock.tick(30)

pygame.quit()
ser.close()
