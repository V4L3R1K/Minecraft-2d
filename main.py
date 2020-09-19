import pygame
import os

from block import Block

#constants
WIDTH = 800
HEIGHT = 450

SCALE = 5 #scale of textures

#initializating pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft 2d")

clock = pygame.time.Clock()

#initialazing textures
textures = {"blocks":{}}
for blockName in os.listdir("data/textures/blocks/"):
	if blockName != "desktop.ini":
		textures["blocks"].update({blockName[:-4]:pygame.transform.scale(pygame.image.load("data/textures/blocks/"+blockName), (16*SCALE, 16*SCALE))})

#generating map
blocks = []
blocks.append(Block(1, 2, "grass"))

#main cycle
alive = True
while alive:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			alive = False



	screen.fill((63, 127, 191))

	#drawing blocks
	for block in blocks:
		screen.blit(textures["blocks"][block.name], (block.x*16*SCALE, block.y*16*SCALE))

	pygame.display.update()

	clock.tick()