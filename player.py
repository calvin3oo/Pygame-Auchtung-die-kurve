import pygame
import random

# The player class draws the players, handles player to player collision, and handles player to powerup collision
class Player:
    def __init__(self, x, y, angle, color, left_key, right_key):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 3
        self.angle = angle
        self.angular_speed = 5
        self.path = []
        self.left_key = left_key
        self.right_key = right_key
        self.gap = False 
        self.gap_count = 0
        self.powered = False
        self.powered_count = 0

    def update(self, other_players_paths, powerups, game, screen):
        keys = pygame.key.get_pressed()

        # Adjust the angle based on left or right key press
        if keys[self.left_key]:
            self.angle -= self.angular_speed
        if keys[self.right_key]:
            self.angle += self.angular_speed

        # Update the player's position based on the current angle
        self.x += self.speed * pygame.math.Vector2(1, 0).rotate(self.angle).x
        self.y += self.speed * pygame.math.Vector2(1, 0).rotate(self.angle).y

        # prevent the player from going off-screen
        self.x = max(0, min(self.x, 800))
        self.y = max(0, min(self.y, 600))

        # Randomly set 'gap' to True with a certain probability
        if random.random() < 0.02 or self.gap: 
            self.gap = True
            self.gap_count += 1
            if(self.gap_count > 10):
                self.gap_count = 0
                self.gap = False
        else:
            self.gap = False
            
        # Check for collisions with other players' paths
        if not self.gap:
            for other_path in other_players_paths:
                for trail_point in other_path:
                    distance = pygame.math.Vector2(self.x - trail_point[0], self.y - trail_point[1]).length()
                    if distance < 2 and not trail_point[2]:
                        # Handle collision logic
                        print("Trail Collision!")
                        game.loser = self
                        game.draw_winner(screen, game.loser)

        # Check for collisions with the player's own trail
        if not self.gap:
            for i in range(len(self.path) - 1):  # Exclude the current position to avoid self-collision
                point1 = pygame.math.Vector2(self.path[i][0], self.path[i][1])
                point2 = pygame.math.Vector2(self.path[i + 1][0], self.path[i + 1][1])
                player_position = pygame.math.Vector2(self.x, self.y)

                # Check collision between line segment and player's position
                if self.point_to_line_distance(player_position, point1, point2) < 1 and not self.path[i][2]:
                    # Handle collision logic
                    print("Self-Trail Collision!")
                    game.loser = self
                    game.draw_winner(screen, game.loser)

        self.path.append((self.x, self.y, self.gap))

        for powerup in powerups:
            distance = pygame.math.Vector2(self.x - powerup.x, self.y - powerup.y).length()
            if distance < 10:  # Adjust the collision radius as needed
                # Handle powerup collision logic
                self.apply_powerup(powerup)
                self.powered = True
                powerups.remove(powerup)
                self.powered_count += 1
        if(self.powered):
            self.powered_count += 1
            if(self.powered_count > 100):
                self.powered = False
                self.powered_count = 0
                self.speed = 3
                self.speed = max(1.5, self.speed)

    def apply_powerup(self, powerup):
        if powerup.powerup_type == "slow_down":
            self.speed -= 1
            self.speed = max(1.5, self.speed)

    def point_to_line_distance(self, point, line_start, line_end):
        line = line_end - line_start
        point_to_line_start = point - line_start
        denom = line.dot(line)
        if denom == 0:
            return point_to_line_start.length()
        t = max(0, min(line.dot(point_to_line_start) / denom, 1))
        projection = line_start + t * line
        distance = pygame.math.Vector2(point - projection).length()
        return distance
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

        # Draw the player's path
        if len(self.path) > 1:
            for i in range(1, len(self.path)):
                point1 = (int(self.path[i - 1][0]), int(self.path[i - 1][1]))
                point2 = (int(self.path[i][0]), int(self.path[i][1]))

                # don't draw if there is a gap
                if not self.path[i][2]:
                    pygame.draw.line(screen, self.color, point1, point2, 2)
