import pygame
import os
import math
import random

from block import Block
from entity import Entity

#constants
WIDTH = 1600
HEIGHT = 900

SCALE = 4 #scale of textures

WORLD_WIDTH = 256
WORLD_HEIGHT = 256

G = 20 #gravity

#initializing pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft 2d")

clock = pygame.time.Clock()

#initialing textures
textures = {"blocks":{}, "entities":{}}
for blockName in os.listdir("data/textures/blocks/"):
	textures["blocks"].update({blockName[:-4]:pygame.transform.scale(pygame.image.load("data/textures/blocks/"+blockName), (16*SCALE, 16*SCALE))})
for entityName in os.listdir("data/textures/entities/"):
	imageRaw = pygame.image.load("data/textures/entities/"+entityName)
	textures["entities"].update({entityName[:-4]:pygame.transform.scale(imageRaw, (imageRaw.get_width()*SCALE, imageRaw.get_height()*SCALE))})

#generating map
gameMap = []
for y in range(WORLD_HEIGHT):
	gameMap.append([])
	for x in range(WORLD_WIDTH):
		gameMap[y].append(Block("air"))

for x in range(WORLD_WIDTH):
	gameMap[63][x] = Block("grass")
for x in range(WORLD_WIDTH):
	gameMap[62][x] = Block("dirt")
	gameMap[61][x] = Block("dirt")
	gameMap[60][x] = Block("dirt")
for x in range(WORLD_WIDTH):
	for y in range(0, 60):
		gameMap[y][x] = Block("stone")

#steve
entities = []
entities.append(Entity(random.randint(0, WORLD_WIDTH), 65, "steveRight"))

#camera
camX = 0
camY = 70

#keys pressed
k_a = False
k_d = False

curX, curY = 0, 0 #cursor

mouseX, mouseY = 0, 0 #mouse

#main cycle
alive = True
while alive:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			alive = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				#jump
				if entities[0].velocityY == 0:
					entities[0].velocityY = 7.5
					entities[0].accelerationY = -G
					entities[0].velocityY+=entity.accelerationY*clock.get_time()/1000
					entities[0].y+=entity.velocityY*clock.get_time()/1000

			elif event.key == pygame.K_a:
				k_a = True

			elif event.key == pygame.K_d:
				k_d = True

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				k_a = False

			elif event.key == pygame.K_d:
				k_d = False
		
		elif event.type == pygame.MOUSEMOTION:
			mouseX, mouseY = event.pos

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				try:
					gameMap[int(curY)][int(curX)] = Block("air")
				except:
					pass

			elif event.button == 3:
				try:
					#you cant place blocks inside youself
					if (curY != math.ceil(entities[0].y) or curX != math.floor(entities[0].x+8/16)) and (int(curY) != math.ceil(entities[0].y-1) or int(curX) != math.floor(entities[0].x+8/16)) and (int(curY) != math.floor(entities[0].y-1) or int(curX) != math.floor(entities[0].x+8/16)) and (curY != math.ceil(entities[0].y) or curX != math.floor(entities[0].x)) and (int(curY) != math.ceil(entities[0].y-1) or int(curX) != math.floor(entities[0].x)) and (int(curY) != math.floor(entities[0].y-1) or int(curX) != math.floor(entities[0].x)):
						gameMap[int(curY)][int(curX)] = Block("stone")
				except:
					print(1)

	entities[0].velocityX = 0

	if k_a:
		entities[0].name = "steveLeft"
		entities[0].velocityX -= 4
				
	if k_d:
		entities[0].name = "steveRight"
		entities[0].velocityX += 4

	#physics
	for entity in entities:
		#X
		try:
			if entity.name.endswith("Right"):
				if gameMap[math.ceil(entity.y)][math.floor(entity.x+8/16)].name != "air" or gameMap[math.ceil(entity.y-1)][math.floor(entity.x+8/16)].name != "air" or gameMap[math.floor(entity.y-1)][math.floor(entity.x+8/16)].name != "air":
					entity.accelerationX = 0
					entity.velocityX = 0
				else:
					entity.velocityX+=entity.accelerationX*clock.get_time()/1000
					entity.x+=entity.velocityX*clock.get_time()/1000

			elif entity.name.endswith("Left"):
				if gameMap[math.ceil(entity.y)][math.floor(entity.x)].name != "air" or gameMap[math.ceil(entity.y-1)][math.floor(entity.x)].name != "air" or gameMap[math.floor(entity.y-1)][math.floor(entity.x)].name != "air":
					entity.accelerationX = 0
					entity.velocityX = 0
				else:
					entity.velocityX+=entity.accelerationX*clock.get_time()/1000
					entity.x+=entity.velocityX*clock.get_time()/1000
		except:
			entity.velocityX+=entity.accelerationX*clock.get_time()/1000
			entity.x+=entity.velocityX*clock.get_time()/1000

		if entity.x < 0: entity.x = 0
		if entity.x > WORLD_WIDTH-textures["entities"][entity.name].get_width()/(SCALE*16)-1/16: entity.x = WORLD_WIDTH-textures["entities"][entity.name].get_width()/(SCALE*16)-1/16
		
		#Y
		try:
			if gameMap[math.ceil(entity.y-2)][math.floor(entity.x+1/16)].name != "air" or gameMap[math.ceil(entity.y-2)][math.floor(entity.x+7/16)].name != "air":
				entity.accelerationY = 0
				entity.velocityY = 0
				entity.y = math.ceil(entity.y)
			else:
				entity.accelerationY = -G
				entity.velocityY+=entity.accelerationY*clock.get_time()/1000
				entity.y+=entity.velocityY*clock.get_time()/1000

			if gameMap[math.ceil(entity.y)][math.floor(entity.x+1/16)].name != "air" or gameMap[math.ceil(entity.y)][math.floor(entity.x+7/16)].name != "air":
				entity.velocityY = 0
				entity.y = math.floor(entity.y)
		except:
			entity.accelerationY = -G
			entity.velocityY+=entity.accelerationY*clock.get_time()/1000
			entity.y+=entity.velocityY*clock.get_time()/1000

	camX = entities[0].x-WIDTH//(16*SCALE)/2
	camY = entities[0].y+HEIGHT//(16*SCALE)/2

	curX = (mouseX+camX*(16*SCALE))//(16*SCALE)
	curY = (-mouseY+camY*(16*SCALE))//(16*SCALE)+1

	#drawing
	screen.fill((63, 127, 191))

	#blocks
	for y in range(int(camY)-HEIGHT//(16*SCALE), int(camY)+1):
		for x in range(int(camX), 1+int(camX)+WIDTH//(16*SCALE)):
			if x>=0 and x<WORLD_WIDTH and y>=0 and y<WORLD_HEIGHT and gameMap[y][x].name != "air":
				screen.blit(textures["blocks"][gameMap[y][x].name], ((x-camX)*16*SCALE, (camY-y)*16*SCALE))

	#entities
	for entity in entities:
		if (entity.x-camX)*16*SCALE > -16*SCALE*textures["entities"][entity.name].get_width() and (entity.x-camX)*16*SCALE < WIDTH and (camY-entity.y)*16*SCALE > -16*SCALE*textures["entities"][entity.name].get_height() and (camY-entity.y)*16*SCALE < HEIGHT:
			screen.blit(textures["entities"][entity.name], ((entity.x-camX)*16*SCALE, (camY-entity.y)*16*SCALE))

	#cursor
	pygame.draw.rect(screen, (191, 191, 191), ((curX-camX)*(16*SCALE), (camY-curY)*(16*SCALE), 16*SCALE, 16*SCALE), 1)

	pygame.display.flip()

	clock.tick(60)