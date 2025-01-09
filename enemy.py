import pygame
import random
import time
import constants as const
from projectile import Projectile

class Enemy(pygame.sprite.Sprite):
    def __init__(self, maze):
        super(Enemy, self).__init__()
        enemy_levels = [
            (pygame.image.load("assets/enemies/Enemy_1.png").convert_alpha(), 75, 3),
            (pygame.image.load("assets/enemies/Enemy_2.png").convert_alpha(), 40, 1),
            (pygame.image.load("assets/enemies/Enemy_3.png").convert_alpha(), 100, 5),
        ]

        self.enemy_selected = random.choice(enemy_levels)

        self.surf = self.enemy_selected[0]

        original_width, original_height = self.surf.get_size()
        max_width = 20
        aspect_ratio = original_height / original_width
        new_width = max_width
        new_height = int(new_width * aspect_ratio)

        self.surf = pygame.transform.scale(self.surf, (new_width, new_height))
        self.rect = self.surf.get_rect()

        # Random position
        self.x, self.y = self.get_random_position(maze)

        # Move to valid position on maze
        self.rect.x = self.x * const.TILE_SIZE
        self.rect.y = self.y * const.TILE_SIZE

        # Health
        self.health = self.enemy_selected[1]

        # Defense
        self.projectiles = pygame.sprite.Group()
        self.damage = self.enemy_selected[2]

        # Speed
        self.speed = 2
        self.move_delay = 0.05
        self.last_move_time = time.time()

    def get_random_position(self, maze):
        while True:
            x = random.randint(1, maze.COLS - 1)
            y = random.randint(1, maze.ROWS - 1)
            if maze.maze[y][x] == 0:  # Path, not a wall
                return x, y

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery, False)
        self.projectiles.add(projectile)

    def changeSize(self, new_width):
        original_width, original_height = self.enemy_selected[0].get_size()
        aspect_ratio = original_height / original_width
        new_height = int(new_width * aspect_ratio)

        self.surf = pygame.transform.scale(self.enemy_selected[0], (new_width, new_height))
        self.rect = self.surf.get_rect(center=self.rect.center)
