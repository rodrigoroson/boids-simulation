from world import World
from config import WIDTH, HEIGHT
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    world = World()
    world.populate(n_prey=60, n_pred=4)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000  # segundos por frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        world.update(dt)
        screen.fill((0, 0, 0))
        world.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()