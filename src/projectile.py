import pygame
import constants as const

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, isPlayer):
        super(Projectile, self).__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))

        pygame.draw.circle(
            self.image, 
            const.PURPLE if isPlayer else const.RED,
            (10,10),
            10
        )
        
        self.rect = self.image.get_rect(center=(x, y)) 

        if isPlayer:
            self.speed = 10 # Player shoot from left to right
        else:
            self.speed = -10 # Enemy shoot from right to left

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > const.WIDTH:
            self.kill() # Delete if overflow window
