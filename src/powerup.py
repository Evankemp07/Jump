import pygame
from settings import PLATFORM_WIDTH

class PowerUp:
    def __init__(self, platform):
        self.platform = platform
        self.x = platform.x + platform.width // 2 - 10
        self.y = platform.y - 2
        self.width = 25
        self.height = 15
        self.active = True

    def update(self):
        self.x = self.platform.x + self.platform.width // 2 - 10
        self.y = self.platform.y - 20
    
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (0, 255, 255), (self.x, self.y, self.width, self.height), border_radius=10)

    def collect(self, player):
        if self.active and player.x < self.x + self.width and player.x + player.width > self.x:
            if player.y < self.y + self.height and player.y + player.height > self.y:
                self.active = False
                return True
        return False
