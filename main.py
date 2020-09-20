import pygame
import os

from block import Block

#constants
WIDTH = 800
HEIGHT = 600

SCALE = 2 #scale of textures

#initializing pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft 2d")

clock = pygame.time.Clock()

#initialing textures
textures = {"blocks":{}}
for blockName in os.listdir("data/textures/blocks/"):
	textures["blocks"].update({blockName[:-4]:pygame.transform.scale(pygame.image.load("data/textures/blocks/"+blockName), (16*SCALE, 16*SCALE))})

#generating map
blocks = []
for x in range(256):
	blocks.append(Block(x, 63, "grass"))
for x in range(256):
	blocks.append(Block(x, 62, "dirt"))
	blocks.append(Block(x, 61, "dirt"))
	blocks.append(Block(x, 60, "dirt"))
for x in range(256):
	for y in range(0, 60):
		blocks.append(Block(x, y, "stone"))

#camera
camX = 0
camY = 70

#main cycle
alive = True
while alive:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			alive = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				camY += 1
			elif event.key == pygame.K_LSHIFT:
				camY -= 1
			elif event.key == pygame.K_a:
				camX -= 1
			elif event.key == pygame.K_d:
				camX += 1

	print(clock.get_fps())

	screen.fill((63, 127, 191))

	#drawing blocks
	for block in blocks:
		if (block.x-camX)*16*SCALE > -16*SCALE and (block.x-camX)*16*SCALE < WIDTH and (camY-block.y)*16*SCALE > -16*SCALE and (camY-block.y)*16*SCALE < HEIGHT:
			screen.blit(textures["blocks"][block.name], ((block.x-camX)*16*SCALE, (camY-block.y)*16*SCALE))

	pygame.display.update()

	clock.tick()