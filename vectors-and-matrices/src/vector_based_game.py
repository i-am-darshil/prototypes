import pygame
import numpy as np

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

position = np.array([100.0, 100.0])
velocity = np.array([4.0, -2.0])
acceleration = np.array([0.0, 0.2])
radius = 20

while True:
  screen.fill((0, 0, 0))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

  pygame.draw.circle(screen, (0, 255, 0), position.astype(int), radius)

  velocity += acceleration
  position += velocity

  # position[0] -> X position & position[1] -> Y position
  # velocity[0] -> X velocity & velocity[1] -> Y velocity
  if position[0] <= 0 or position[0] >= WIDTH:
    velocity[0] *= -0.95
  
  if position[1] >= HEIGHT:
    velocity[1] *= -0.95

  pygame.display.flip()

  clock.tick(60)


    
