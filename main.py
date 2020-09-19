import pygame

pygame.init()

w = 800
h = 450
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Minecraft 2d")

clock = pygame.time.Clock()

alive = True

while alive:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			alive = False



	screen.fill((31, 31, 31))



	pygame.display.update()

	clock.tick()