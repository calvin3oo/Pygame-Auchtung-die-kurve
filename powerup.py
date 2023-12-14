import pygame

# draw the powerup. Other powerup logic is currently handled in the player class
class Powerup:
    def __init__(self, x, y, color, powerup_type):
        self.x = x
        self.y = y
        self.color = color
        self.powerup_type = powerup_type

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)
