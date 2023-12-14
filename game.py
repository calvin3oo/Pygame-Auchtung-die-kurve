import sys
import pygame
import random
from player import Player
from powerup import Powerup

# The game class provides methods for the main game loop. It also keeps track of the players and un-taken powerups
class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = [Player(50, height // 2, 0, (255, 0, 0), pygame.K_q, pygame.K_w),
                        Player(width - 50, height // 2, 180, (0, 0, 255), pygame.K_LEFT, pygame.K_RIGHT)]
        self.powerups = []
        self.loser = None

    def update(self, screen):
        for player in self.players:
            player.update([p.path for p in self.players if p != player], self.powerups, self, screen)

            # Check for collisions with the screen boundaries
            if not (0 < player.x < self.width and 0 < player.y < self.height):
                print("Boundary Collision!")
                self.loser = player
                self.draw_winner(screen, self.loser)
        if(random.random() < 0.005):
            self.spawn_powerup()

    def spawn_powerup(self):
        x = random.randint(20, self.width - 20)
        y = random.randint(20, self.height - 20)
        color = (0, 255, 0)  # Green color for the powerups
        powerup_type = "slow_down"
        powerup = Powerup(x, y, color, powerup_type)
        self.powerups.append(powerup)
            

    def draw(self, screen):
        for player in self.players:
            player.draw(screen)
        for powerup in self.powerups:
            powerup.draw(screen)

        
    def draw_winner(self, screen, loser):
        font = pygame.font.Font(None, 36)
        winner_color = "Red" if self.players.index(loser) == 1 else "Blue"
        text = font.render(f"{winner_color} wins!", True, (255, 255, 255))
        screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000) # don't close the game right away
        pygame.quit()
        sys.exit()
