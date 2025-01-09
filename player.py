import pygame
import time
import constants as const
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.original_image = pygame.image.load("assets/player/player.png").convert_alpha()

        self.surf = self.original_image

        original_width, original_height = self.surf.get_size()
        max_width = const.PLAYER_INIT
        aspect_ratio = original_height / original_width
        new_width = max_width
        new_height = int(new_width * aspect_ratio)

        self.surf = pygame.transform.scale(self.surf, (new_width, new_height))
        
        self.rect = self.surf.get_rect()

        # Player position in maze grid
        self.x = 1
        self.y = 1

        # Movement delay (seconds)
        self.move_delay = 0.05
        self.last_move_time = time.time()

        # Health
        self.health = const.PLAYER_MAX_HEALTH

        # Defense
        self.projectiles = pygame.sprite.Group()

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

    def move(self, pressed_keys, maze):
        current_time = time.time()
        if current_time - self.last_move_time < self.move_delay:
            return
        
        new_x, new_y = self.x, self.y

        if pressed_keys[pygame.K_UP]:
            new_x -= 1
        elif pressed_keys[pygame.K_DOWN]:
            new_x += 1
        elif pressed_keys[pygame.K_LEFT]:
            new_y -= 1
        elif pressed_keys[pygame.K_RIGHT]:
            new_y += 1

        # Check collision with walls
        if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != 1:
            self.x, self.y = new_x, new_y

        # Update the pixel position of the player
        self.rect.midleft = (self.y * const.TILE_SIZE, self.x * const.TILE_SIZE)
        self.last_move_time = current_time

    def move_on_combat(self, pressed_keys):
        current_time = time.time()
        speed = const.PLAYER_SPEED
        
        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(speed * -1, 0)
        if pressed_keys[pygame.K_RIGHT] and self.rect.right < const.WIDTH:
            self.rect.move_ip(speed, 0)
        if pressed_keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, speed * -1)
        if pressed_keys[pygame.K_DOWN] and self.rect.bottom < const.HEIGHT:
            self.rect.move_ip(0, speed)

        self.last_move_time = current_time

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100 

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery, True)
        self.projectiles.add(projectile)

    def changeSize(self, new_width):
        original_width, original_height = self.original_image.get_size()
        aspect_ratio = original_height / original_width
        new_height = int(new_width * aspect_ratio)

        self.surf = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.surf.get_rect(center=self.rect.center)
