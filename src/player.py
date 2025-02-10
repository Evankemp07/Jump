import pygame
from settings import PLAYER_COLOR, WIDTH, GRAVITY, JUMP_STRENGTH, PLAYER_SPEED

class Player:
    def __init__(self, start_platform):
        self.width = 30
        self.height = 30
        self.x = WIDTH // 2 - self.width // 2
        self.y = start_platform.y - self.height - 10
        self.vel_y = 0

    def update(self, platforms):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        for platform in platforms:
            if (
                self.vel_y > 0 and
                self.y + self.height >= platform.y and
                self.y + self.height - self.vel_y <= platform.y and
                self.x + self.width > platform.x and
                self.x < platform.x + platform.width
            ):
                self.vel_y = JUMP_STRENGTH
                self.y = platform.y - self.height

                if platform.type == "disappearing" and not platform.stepped_on:
                    platform.stepped_on = True

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += PLAYER_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, self.width, self.height))
