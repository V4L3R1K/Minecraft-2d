import pygame
import os
import math
import random
import json
import time

from block import Block
from entity import Entity
from item import Item
from inventorySlot import InventorySlot

def CalculateBreakTime(block, item):
	blockProperties = properties["blocks"][block]

	t = 1.5 * blockProperties["hardness"]
	
	if blockProperties["material"] == "hand":
		if item.endswith(blockProperties["tool"]):
			if item.startswith("wooden"):
				t /= 2
			elif item.startswith("stone"):
				t /= 4
			elif item.startswith("iron"):
				t /= 6
			elif item.startswith("diamond"):
				t /= 8
			elif item.startswith("golden"):
				t /= 12
			else:
				print("error: "+item+" does not exist")
		else:
			pass
	elif blockProperties["material"] == "wooden":
		if item.endswith(blockProperties["tool"]):
			if item.startswith("wooden"):
				t /= 2
			elif item.startswith("stone"):
				t /= 4
			elif item.startswith("iron"):
				t /= 6
			elif item.startswith("diamond"):
				t /= 8
			elif item.startswith("golden"):
				t /= 12
			else:
				print("error: "+item+" does not exist")
		else:
			t *= 10/3
	elif blockProperties["material"] == "stone":
		if item.endswith(blockProperties["tool"]):
			if item.startswith("stone"):
				t /= 4
			elif item.startswith("iron"):
				t /= 6
			elif item.startswith("diamond"):
				t /= 8
			elif item.startswith("golden"):
				t /= 12
			else:
				t *= 10/3
		else:
			t *= 10/3
	elif blockProperties["material"] == "iron":
		if item.endswith(blockProperties["tool"]):
			if item.startswith("iron"):
				t /= 6
			elif item.startswith("diamond"):
				t /= 8
			else:
				t *= 10/3
		else:
			t *= 10/3
	elif blockProperties["material"] == "diamond":
		if item.endswith(blockProperties["tool"]):
			if item.startswith("diamond"):
				t /= 8
			else:
				t *= 10/3
		else:
			t *= 10/3
	else:
		print("error: "+item+" does not exist")

	return t

def Give(inventorySlot):
	for slot in range(36):
		if inventory[slot].item.name == inventorySlot.item.name:
			if inventory[slot].amount+inventorySlot.amount <= properties["items"][inventorySlot.item.name]["stack"]:
				inventory[slot].amount += inventorySlot.amount
				return
			else:
				inventory[slot].amount = properties["items"][inventorySlot.item.name]["stack"]
				Give(InventorySlot(inventorySlot.item, properties["items"][inventorySlot.item.name]["stack"]-inventory[slot].amount-inventorySlot.amount))
				return
	for slot in range(36):
		if inventory[slot].item.name == "hand":
			if inventorySlot.amount <= properties["items"][inventorySlot.item.name]["stack"]:
				inventory[slot] = inventorySlot
			else:
				inventory[slot] = InventorySlot(inventorySlot.item, properties["items"][inventorySlot.item.name]["stack"])
				Give(InventorySlot(inventorySlot.item, properties["items"][inventorySlot.item.name]["stack"]-inventorySlot.amount))
			return
	Drop(inventorySlot)

def Drop(inventorySlot):
	print("Dropped "+str(inventorySlot.amount)+" "+inventorySlot.item.name)

#constants
WIDTH = 1600
HEIGHT = 900

SCALE = 4 #scale of textures
GUI_SCALE = 4 #scale of gui

#world generation settings
WORLD_WIDTH = 256
WORLD_HEIGHT = 256

random.seed(0) #world seed

HEIGHT_DEFAULT = 63
HEIGHT_DISPERSION = 4

GENERATION_STEP = 8

TREE_STEP_MIN = 8
TREE_STEP_MAX = 16

G = 20 #gravity

#initializing pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft 2d")

clock = pygame.time.Clock()

#initialing textures
textures = {"blocks":{}, "entities":{}, "items":{}, "gui":{}, "destroy_stages":{}}
for name in os.listdir("data/textures/blocks/"):
	textures["blocks"].update({name[:-4]:pygame.transform.scale(pygame.image.load("data/textures/blocks/"+name), (16*SCALE, 16*SCALE))})
	textures["items"].update({name[:-4]:pygame.transform.scale(pygame.image.load("data/textures/blocks/"+name), (16*GUI_SCALE, 16*GUI_SCALE))})
for name in os.listdir("data/textures/entities/"):
	imageRaw = pygame.image.load("data/textures/entities/"+name)
	textures["entities"].update({name[:-4]:pygame.transform.scale(imageRaw, (imageRaw.get_width()*SCALE, imageRaw.get_height()*SCALE))})
for name in os.listdir("data/textures/items/"):
	textures["items"].update({name[:-4]:pygame.transform.scale(pygame.image.load("data/textures/items/"+name), (16*GUI_SCALE, 16*GUI_SCALE))})
for name in os.listdir("data/textures/gui/"):
	imageRaw = pygame.image.load("data/textures/gui/"+name)
	textures["gui"].update({name[:-4]:pygame.transform.scale(imageRaw, (imageRaw.get_width()*GUI_SCALE, imageRaw.get_height()*GUI_SCALE))})
for name in os.listdir("data/textures/destroy_stages/"):
	textures["destroy_stages"].update({name[:-4]:pygame.transform.scale(pygame.image.load("data/textures/destroy_stages/"+name), (16*SCALE, 16*SCALE))})

#initializing properties
properties = {"blocks":{}, "items":{}}
for name in os.listdir("data/properties/blocks/"):
	file = open("data/properties/blocks/"+name, "r")
	properties["blocks"].update({name[:-5]:json.loads(file.read())})
	file.close()
for name in os.listdir("data/properties/items/"):
	file = open("data/properties/items/"+name, "r")
	properties["items"].update({name[:-5]:json.loads(file.read())})
	file.close()

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
			try:
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
			except:
				pass

#entities
entities = []
entities.append(Entity(0.5, 70, "steveRight")) #steve

#camera
camX = 0
camY = 0

#keys pressed
k_a = False
k_d = False

curX, curY = 0, 0 #cursor

mouseX, mouseY = 0, 0 #mouse

showDebug = False #F3 menu

#inventory
inventory = {}
for i in range(45):
	inventory[i] = InventorySlot(Item("hand"), 1)
inventoryHotbarSelected = 0
inventoryOpened = False

breakStart = 0
breakTime = 0

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

			elif event.key == pygame.K_F3:
				showDebug = not showDebug

			elif event.key == pygame.K_e:
				inventoryOpened = not inventoryOpened

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				k_a = False

			elif event.key == pygame.K_d:
				k_d = False
		
		elif event.type == pygame.MOUSEMOTION:
			mouseX, mouseY = event.pos

			if event.buttons[0]:
				if int((mouseX+camX*(16*SCALE))//(16*SCALE)) == curX and int((-mouseY+camY*(16*SCALE))//(16*SCALE)+1) == curY:
					pass
				else:
					gameMap[int(curY)][int(curX)].breakStage = -1
					if gameMap[int((-mouseY+camY*(16*SCALE))//(16*SCALE)+1)][int((mouseX+camX*(16*SCALE))//(16*SCALE))].name != "air":		
						breakStart = time.time()
						breakTime = CalculateBreakTime(gameMap[int((-mouseY+camY*(16*SCALE))//(16*SCALE)+1)][int((mouseX+camX*(16*SCALE))//(16*SCALE))].name, inventory[inventoryHotbarSelected].item.name)
						gameMap[int((-mouseY+camY*(16*SCALE))//(16*SCALE)+1)][int((mouseX+camX*(16*SCALE))//(16*SCALE))].breakStage += 0.001

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if gameMap[int(curY)][int(curX)].name != "air":
					if gameMap[int(curY)][int(curX)].breakStage == -1:
						breakStart = time.time()
						gameMap[int(curY)][int(curX)].breakStage += 0.001

					breakTime = CalculateBreakTime(gameMap[int(curY)][int(curX)].name, inventory[inventoryHotbarSelected].item.name)

			elif event.button == 3:
				try:
					#you cant place blocks inside youself
					if (curY != math.ceil(entities[0].y) or curX != math.floor(entities[0].x+8/16)) and (int(curY) != math.ceil(entities[0].y-1) or int(curX) != math.floor(entities[0].x+8/16)) and (int(curY) != math.floor(entities[0].y-1) or int(curX) != math.floor(entities[0].x+8/16)) and (curY != math.ceil(entities[0].y) or curX != math.floor(entities[0].x)) and (int(curY) != math.ceil(entities[0].y-1) or int(curX) != math.floor(entities[0].x)) and (int(curY) != math.floor(entities[0].y-1) or int(curX) != math.floor(entities[0].x)):
						#you cant place blocks outside the world
						if curY>=0 and curY<WORLD_HEIGHT and curX>=0 and curX<WORLD_WIDTH:
							#you can place blocks only in the air
							if gameMap[int(curY)][int(curX)].name == "air":
								if properties["items"][inventory[inventoryHotbarSelected].item.name]["type"] == "block":
									gameMap[int(curY)][int(curX)] = Block(inventory[inventoryHotbarSelected].item.name)
									inventory[inventoryHotbarSelected].amount-=1
									if inventory[inventoryHotbarSelected].amount == 0:
										inventory[inventoryHotbarSelected] = InventorySlot(Item("hand"), 1)
				except:
					pass

			elif event.button == 4:
				inventoryHotbarSelected-=1
			elif event.button == 5:
				inventoryHotbarSelected+=1

		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				gameMap[int(curY)][int(curX)].breakStage = -1

	if inventoryHotbarSelected < 0: inventoryHotbarSelected=8
	if inventoryHotbarSelected > 8: inventoryHotbarSelected=0

	if gameMap[int(curY)][int(curX)].breakStage != -1:
		gameMap[int(curY)][int(curX)].breakStage = (time.time()-breakStart)/breakTime*10
	if gameMap[int(curY)][int(curX)].breakStage >= 9:
		gameMap[int(curY)][int(curX)].breakStage = -1
		number = random.random()
		summa = 0
		for drop in properties["blocks"][gameMap[int(curY)][int(curX)].name]["drop"]:
			summa += drop["chance"]
			if number < summa:
				Give(InventorySlot(Item(drop["name"]), drop["amount"]))
				break
		gameMap[int(curY)][int(curX)].name = "air"

	entities[0].velocityX = 0

	if k_a:
		entities[0].name = "steveLeft"
		entities[0].velocityX -= 4
				
	if k_d:
		entities[0].name = "steveRight"
		entities[0].velocityX += 4

	#collision detection
	for entity in entities:
		#Y
		entity.accelerationY = -G
		entity.velocityY += entity.accelerationY*clock.get_time()/1000
		entity.y += entity.velocityY*clock.get_time()/1000

		if gameMap[math.floor(entity.y)-1][math.floor(entity.x)].name != "air" or gameMap[math.floor(entity.y)-1][math.ceil(entity.x-8/16)].name != "air": #bottom
			entity.velocityY = 0
			entity.y = math.ceil(entity.y)

		if gameMap[math.ceil(entity.y)][math.floor(entity.x)].name != "air" or gameMap[math.ceil(entity.y)][math.ceil(entity.x-8/16)].name != "air": #top
			entity.velocityY = 0
			entity.y = math.floor(entity.y)
		
		#X
		entity.velocityX += entity.accelerationX*clock.get_time()/1000
		entity.x += entity.velocityX*clock.get_time()/1000

		if gameMap[math.ceil(entity.y)][math.ceil(entity.x-8/16)].name != "air" or gameMap[math.floor(entity.y)][math.ceil(entity.x-8/16)].name != "air" or gameMap[math.floor(entity.y-15/16)][math.ceil(entity.x-8/16)].name != "air": #right
			entity.x = math.floor(entity.x)+8/16
		if gameMap[math.ceil(entity.y)][math.floor(entity.x)].name != "air" or gameMap[math.floor(entity.y)][math.floor(entity.x)].name != "air" or gameMap[math.floor(entity.y-15/16)][math.floor(entity.x)].name != "air": #left
			entity.x = math.ceil(entity.x)

		if entity.x < 0: entity.x = 0
		if entity.x > WORLD_WIDTH-textures["entities"][entity.name].get_width()/(SCALE*16): entity.x = WORLD_WIDTH-textures["entities"][entity.name].get_width()/(SCALE*16)

	camX = entities[0].x-WIDTH//(16*SCALE)/2
	camY = entities[0].y+HEIGHT//(16*SCALE)/2

	curX = (mouseX+camX*(16*SCALE))//(16*SCALE)
	curY = (-mouseY+camY*(16*SCALE))//(16*SCALE)+1

	#drawing
	screen.fill((63, 127, 191))

	#blocks
	for y in range(int(camY)-HEIGHT//(16*SCALE), int(camY)+2):
		for x in range(int(camX), 2+int(camX)+WIDTH//(16*SCALE)):
			if x>=0 and x<WORLD_WIDTH and y>=0 and y<WORLD_HEIGHT and gameMap[y][x].name != "air":
				screen.blit(textures["blocks"][gameMap[y][x].name], ((x-camX)*16*SCALE, (camY-y)*16*SCALE))
				
	#breaking
	if math.floor(gameMap[int(curY)][int(curX)].breakStage) > -1:
		screen.blit(textures["destroy_stages"][str(math.floor(gameMap[int(curY)][int(curX)].breakStage))], ((int(curX)-camX)*16*SCALE, (camY-int(curY))*16*SCALE))

	#entities
	for entity in entities:
		if (entity.x-camX)*16*SCALE > -16*SCALE*textures["entities"][entity.name].get_width() and (entity.x-camX)*16*SCALE < WIDTH and (camY-entity.y)*16*SCALE > -16*SCALE*textures["entities"][entity.name].get_height() and (camY-entity.y)*16*SCALE < HEIGHT:
			screen.blit(textures["entities"][entity.name], ((entity.x-camX)*16*SCALE, (camY-entity.y)*16*SCALE))

	#cursor
	pygame.draw.rect(screen, (191, 191, 191), ((curX-camX)*(16*SCALE), (camY-curY)*(16*SCALE), 16*SCALE, 16*SCALE), 1)

	#hotbar
	screen.blit(textures["gui"]["hotbar"], (WIDTH//2-91*GUI_SCALE, HEIGHT-22*GUI_SCALE))
	screen.blit(textures["gui"]["hotbar_selected"], (WIDTH//2-92*GUI_SCALE+inventoryHotbarSelected*20*GUI_SCALE, HEIGHT-23*GUI_SCALE))
	for slot in range(9):
		if inventory[slot].item.name != "hand":
			screen.blit(textures["items"][inventory[slot].item.name], (WIDTH//2-91*GUI_SCALE+3*GUI_SCALE+slot*20*GUI_SCALE, HEIGHT-19*GUI_SCALE))
			screen.blit(pygame.font.SysFont("consolas", 11).render(str(inventory[slot].amount), 1, (255, 255, 255)), (WIDTH//2-91*GUI_SCALE+3*GUI_SCALE+slot*20*GUI_SCALE, HEIGHT-19*GUI_SCALE))

	#inventory
	if inventoryOpened:
		screen.blit(textures["gui"]["inventory"], (WIDTH//2-88*GUI_SCALE, HEIGHT//2-83*GUI_SCALE))

	#debug (F3 menu)
	if showDebug:
		screen.blit(pygame.font.SysFont("consolas", 11).render("FPS: "+str(clock.get_fps()), 1, (255, 255, 255)), (0, 0))
		screen.blit(pygame.font.SysFont("consolas", 11).render("XY: "+str(round(entities[0].x, 5))+" / "+str(round(entities[0].y, 5)), 1, (255, 255, 255)), (0, 10))

	'''
	pygame.draw.rect(screen, (255, 0, 0), ((math.floor(entities[0].x)-camX)*(16*SCALE), (camY-math.ceil(entities[0].y))*(16*SCALE), 16*SCALE, 16*SCALE), 1)
	pygame.draw.rect(screen, (127, 0, 0), ((math.floor(entities[0].x)-camX)*(16*SCALE), (camY-math.floor(entities[0].y))*(16*SCALE), 16*SCALE, 16*SCALE), 1)
	pygame.draw.rect(screen, (63, 0, 0), ((math.floor(entities[0].x)-camX)*(16*SCALE), (camY-math.floor(entities[0].y)+1)*(16*SCALE), 16*SCALE, 16*SCALE), 1)
	pygame.draw.rect(screen, (0, 255, 0), ((math.ceil(entities[0].x-8/16)-camX)*(16*SCALE), (camY-math.ceil(entities[0].y))*(16*SCALE), 16*SCALE, 16*SCALE), 1)
	pygame.draw.rect(screen, (0, 127, 0), ((math.ceil(entities[0].x-8/16)-camX)*(16*SCALE), (camY-math.floor(entities[0].y))*(16*SCALE), 16*SCALE, 16*SCALE), 1)
	pygame.draw.rect(screen, (0, 63, 0), ((math.ceil(entities[0].x-8/16)-camX)*(16*SCALE), (camY-math.floor(entities[0].y)+1)*(16*SCALE), 16*SCALE, 16*SCALE), 1)
	'''

	pygame.display.flip()

	clock.tick()