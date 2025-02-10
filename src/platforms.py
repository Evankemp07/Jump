import pygame
import random
from settings import WIDTH, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_SPEED

class Platform:
    def __init__(self, x, y, force_static=False):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT

        if force_static:
            self.type = "static"
        else:
            self.type = random.choices(
                ["static", "moving", "disappearing"],
                weights=[75, 10, 15]
            )[0]

        self.speed = PLATFORM_SPEED if self.type == "moving" else 0
        self.direction = random.choice([-1, 1])

        self.stepped_on = False
        self.fading = False
        self.fade_alpha = 255
        self.is_gone = False

    def update(self):
        if self.type == "moving":
            self.x += self.speed * self.direction
            if self.x <= 0 or self.x + self.width >= WIDTH:
                self.direction *= -1

        if self.type == "disappearing":
            self.disappear()

        if self.fading:
            self.fade_alpha -= 5
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.is_gone = True

    def draw(self, screen):
        if self.type == "moving":
            color = (255, 165, 0, self.fade_alpha)
        elif self.type == "disappearing":
            color = (255, 0, 0, self.fade_alpha)
        else:
            color = (0, 255, 0, self.fade_alpha)

        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill(color)
        screen.blit(surface, (self.x, self.y))

    def disappear(self):
        if self.type == "disappearing" and self.stepped_on:
            if not self.fading:
                self.fading = True
        return self.is_gone
