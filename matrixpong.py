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

wheel = 0

lastr = 0
lastg = 0
lastb = 150


def rainbowCycle(wheelPos):
	global lastr
	global lastg
	global lastb

	wheelPos = 255 - wheelPos;

	if wheelPos < 85:
		lastr = 255 - wheelPos * 3
		lastg = 0
		lastb = wheelPos * 3
		clearDisplay( 255 - wheelPos * 3, 0, wheelPos * 3 )
		return

	if wheelPos < 170:
		
		wheelPos = wheelPos - 85
		lastr = 0
		lastg = wheelPos * 3
		lastb = 255 - wheelPos * 3
		clearDisplay( 0, wheelPos * 3, 255 - wheelPos * 3)
		return

	wheelPos = wheelPos - 170
	
	lastr = wheelPos * 3
	lastg = 255 - wheelPos * 3
	lastb = 0
	clearDisplay( wheelPos * 3, 255 - wheelPos * 3, 0)



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
	for x in range(0,42):
		for y in range(0,24):
			drawPixel(x,y, pr, pg, pb )
	

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

gameState = 0

winOn = 3

# 0 = not playing
# 1 = countdown
# 2 = playing
# 3 = goal

countdown = 3

while done == False:
	try:
		for event in device.read():
			if event.type == evdev.ecodes.EV_KEY:
				print event.code

				if gameState == 2:
					if event.code == 48 and paddle2Y > 3:
						paddle2Y = paddle2Y - 1
					if event.code == 30 and paddle2Y < 20:
						paddle2Y = paddle2Y + 1
					if event.code == 35 and paddle1Y > 3:
						paddle1Y = paddle1Y - 1
					if event.code == 33 and paddle1Y < 20:
						paddle1Y = paddle1Y + 1

				if gameState == 0:
					if event.code == 18 or event.code == 23:
						gameState = 1
						ballX = 24
						ballY = 12
						playerScore1 = 0
						playerScore2 = 0
						updateCounter = 0
						countdown = 3


	except IOError:
		a = 1

	clearDisplay(lastr, lastg, lastb)

	if gameState == 0:
		wheel = wheel + 1

		if wheel > 254:
			wheel = 1

		rainbowCycle(wheel)


	if gameState == 1:
		if countdown == 0:
			gameState = 2
			updateCounter = 0
		else:		

			drawNumber(countdown, 5, 5, 0, 150, 0)

			updateCounter = updateCounter + 1

			if updateCounter > 20:
				updateCounter = 0
				countdown = countdown - 1	
	

	if gameState == 2:
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

		if ballX == 1:
			ballX = 24
			ballY = 12
			player1Score = player1Score + 1
			gameState = 3
			countdown = 3
			continue

		if ballX == 41:
			ballX = 24
			ballY = 12
			player2Score = player2Score + 1
			gameState = 3
			countdown = 3
			continue
		

		updateCounter = updateCounter + 1;
	
		if updateCounter > 5:

			updateCounter = 0
			ballX = ballX + ballXDir
			ballY = ballY + ballYDir

			if ballX > 40:
				ballXDir = -1

			if ballX < 2:
				ballXDir = 1

			if ballY > 21:
				ballYDir = -1

			if ballY < 2:
				ballYDir = 1


        if gameState == 3:

		if player1Score > 2 or player2Score > 2:
			gameState = 4

                if countdown == 0:
                        gameState = 2
                        updateCounter = 0
                else:

                        drawNumber(countdown, 5, 5, 0, 150, 0)

                        updateCounter = updateCounter + 1

                        if updateCounter > 20:
                                updateCounter = 0
                                countdown = countdown - 1

	if gameState == 4:

                if countdown == 0:
                        gameState = 0
                        updateCounter = 0
			player1Score = 0
			player2Score = 0
                else:

                        #drawNumber(countdown, 5, 5, 0, 150, 0)
			drawScore(player2Score, player1Score)

                        updateCounter = updateCounter + 1

                        if updateCounter > 20:
                                updateCounter = 0
                                countdown = countdown - 1
		


	updateDisplay()

	clock.tick(30)

pygame.quit()
ser.close()
