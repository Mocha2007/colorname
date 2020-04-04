import pygame
from sys import exit
from random import randint, choice
from time import sleep

colorfile = "color2.txt"
refresh = pygame.display.flip

def rb() -> int:
	return randint(0, 255)

def rc() -> (int, int, int):
	rless = choice((0, 255)), rb(), rb()
	gless = rb(), choice((0, 255)), rb()
	bless = rb(), rb(), choice((0, 255))
	return choice((rless, gless, bless))

def dist(a: tuple, b: tuple) -> float:
	assert len(a) == len(b)
	return sum(map(lambda x: (x[0]-x[1])**2, zip(a, b)))**.5

def predict(c: (int, int, int)) -> str:
	assert c[0] in range(256)
	assert c[1] in range(256)
	assert c[2] in range(256)
	# find closest color
	closest = 999, "benis"
	for i in colordata:
		# print(i, colordata[i])
		distance = dist(c, i)
		if distance < closest[0]:
			closest = distance, colordata[i]
	return closest[1]

def drawmap():
	for r in range(0, 256, resolution):
		for g in range(0, 256, resolution):
			c = namedata[predict((r, g, 0))]
			# screen.set_at((r, g), c)
			pygame.draw.rect(screen, c, (r, g+256, resolution, resolution))
			c = namedata[predict((r, g, 255))]
			pygame.draw.rect(screen, c, (768-r, g+256, -resolution, resolution))
		refresh()
	for g in range(0, 256, resolution):
		for b in range(0, 256, resolution):
			c = namedata[predict((255, g, b))]
			pygame.draw.rect(screen, c, (b+256, g+256, resolution, resolution))
			c = namedata[predict((0, g, b))]
			pygame.draw.rect(screen, c, (1024-b, g+256, -resolution, resolution))
		refresh()
	for b in range(0, 256, resolution):
		for r in range(0, 256, resolution):
			c = namedata[predict((r, 0, b))]
			pygame.draw.rect(screen, c, (r, 256-b, resolution, -resolution))
			c = namedata[predict((r, 255, b))]
			pygame.draw.rect(screen, c, (r, b+512, resolution, resolution))
		refresh()

def drawmap2():
	for coords, colorname in colordata.items():
		r, g, b = coords
		c = namedata[colorname]
		if b == 0:
			pygame.draw.rect(screen, c, (r, g+256, resolution, resolution))
		elif b == 255:
			pygame.draw.rect(screen, c, (768-r, g+256, -resolution, resolution))
		elif r == 255:
			pygame.draw.rect(screen, c, (b+256, g+256, resolution, resolution))
		elif r == 0:
			pygame.draw.rect(screen, c, (1024-b, g+256, -resolution, resolution))
		elif g == 0:
			pygame.draw.rect(screen, c, (r, 256-b, resolution, -resolution))
		else:
			pygame.draw.rect(screen, c, (r, b+512, resolution, resolution))

pygame.init()

resolution = 2
size = 1024, 768
screen = pygame.display.set_mode(size)

# colors
try:
	colordata = eval(open(colorfile, "r+").read())
except (FileNotFoundError, SyntaxError):
	colordata = {}

keydata = {
	pygame.K_b: 'blue',
	pygame.K_c: 'cyan',
	pygame.K_e: 'grey',
	pygame.K_g: 'green',
	pygame.K_i: 'pink',
	pygame.K_k: 'black',
	pygame.K_n: 'brown',
	pygame.K_o: 'orange',
	pygame.K_p: 'purple',
	pygame.K_r: 'red',
	pygame.K_t: 'tan',
	pygame.K_w: 'white',
	pygame.K_y: 'yellow'
}

namedata = {
	'blue': (0, 0, 255),
	'green': (0, 192, 0),
	'grey': (128, 128, 128),
	'pink': (255, 160, 160),
	'black': (0, 0, 0),
	'brown': (128, 64, 0),
	'orange': (255, 128, 0),
	'purple': (192, 0, 192),
	'red': (255, 0, 0),
	'white': (255, 255, 255),
	'yellow': (192, 192, 0),
	'cyan': (0, 192, 192),
	'tan': (224, 192, 160),
	'benis': (0, 0, 0)
}

chosen = True
skip = False
i = 0
while 1:
	if chosen or skip:
		currentcolor = rc()
		print(currentcolor, '->', predict(currentcolor))
		screen.fill(currentcolor)
		if i % 10 == 0:
			drawmap()
		refresh()
		skip = False
	chosen = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_x:
				skip = True
				break
			elif event.key in keydata:
				chosen = keydata[event.key]
				break
	# update color.txt
	if chosen:
		colordata[currentcolor] = chosen
		open(colorfile, "w+").write(str(colordata))
	# reduce cpu consumption
	sleep(1/20)
	i += 1