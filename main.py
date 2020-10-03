import pygame
import os
import math
import random

from block import Block
from entity import Entity

#constants
WIDTH = 1600
HEIGHT = 900

SCALE = 3 #scale of textures

#world generation settings
WORLD_WIDTH = 256
WORLD_HEIGHT = 256

random.seed(0) #world seed

HEIGHT_DEFAULT = 63
HEIGHT_DISPERSION = 2

GENERATION_STEP = 4

TREE_STEP_MIN = 4
TREE_STEP_MAX = 8

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

lastEnd = HEIGHT_DEFAULT
for i in range(WORLD_WIDTH//GENERATION_STEP):
	thisEnd = random.randint(HEIGHT_DEFAULT-HEIGHT_DISPERSION, HEIGHT_DEFAULT+HEIGHT_DISPERSION)
	gameMap[lastEnd][i*GENERATION_STEP] = Block("grass")
	for x in range(1, GENERATION_STEP):
		gameMap[int(lastEnd-(lastEnd-thisEnd)/GENERATION_STEP*x)][i*GENERATION_STEP+x] = Block("grass")
	lastEnd = thisEnd

for y in range(WORLD_HEIGHT):
	for blockX in range(len(gameMap[y])):
		if gameMap[y][blockX].name == "grass":
			gameMap[y-1][blockX] = Block("dirt")
			gameMap[y-2][blockX] = Block("dirt")
			if random.randint(0,1) == 1:
				gameMap[y-3][blockX] = Block("dirt")
			else:
				gameMap[y-3][blockX] = Block("stone")
			for yStone in range(0, y-3):
				gameMap[yStone][blockX] = Block("stone")

#trees
yTrees = [random.randint(TREE_STEP_MIN, TREE_STEP_MAX)]
while yTrees[-1] < WORLD_WIDTH:
	yTrees.append(yTrees[-1]+random.randint(TREE_STEP_MIN, TREE_STEP_MAX))
yTrees.pop(-1)
for y in range(WORLD_HEIGHT):
	for blockX in yTrees:
		if gameMap[y][blockX].name == "grass":
			gameMap[y+1][blockX] = Block("oak_log")
			gameMap[y+2][blockX] = Block("oak_log")
			gameMap[y+3][blockX] = Block("oak_log")
			gameMap[y+4][blockX] = Block("oak_log")
			gameMap[y+5][blockX] = Block("oak_log")
			gameMap[y+3][blockX-2] = Block("oak_leaves")
			gameMap[y+3][blockX-1] = Block("oak_leaves")
			gameMap[y+3][blockX+2] = Block("oak_leaves")
			gameMap[y+3][blockX+1] = Block("oak_leaves")
			gameMap[y+4][blockX-2] = Block("oak_leaves")
			gameMap[y+4][blockX-1] = Block("oak_leaves")
			gameMap[y+4][blockX+2] = Block("oak_leaves")
			gameMap[y+4][blockX+1] = Block("oak_leaves")
			gameMap[y+5][blockX-1] = Block("oak_leaves")
			gameMap[y+5][blockX+1] = Block("oak_leaves")
			gameMap[y+6][blockX-1] = Block("oak_leaves")
			gameMap[y+6][blockX] = Block("oak_leaves")
			gameMap[y+6][blockX+1] = Block("oak_leaves")

#steve
entities = []
entities.append(Entity(0.5, 70, "steveRight"))

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
						#you cant place blocks outside the world
						if curY>=0 and curY<WORLD_HEIGHT and curX>=0 and curX<WORLD_WIDTH:
							#you can place blocks only in the air
							if gameMap[int(curY)][int(curX)].name == "air":
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
		for x in range(int(camX), 2+int(camX)+WIDTH//(16*SCALE)):
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

	print(entities[0].y)