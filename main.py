
import pygame
from game import Game

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Achtung, die Kurve!")

# Create game instance
game = Game(width, height)

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state
    game.update(screen)

    # Draw everything
    screen.fill((0, 0, 0))  # Fill screen with black
    game.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

pygame.quit()
