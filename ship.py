import pygame
from pygame.sprite import Sprite
from pygame import Surface

from settings import Settings

class Ship(Sprite):
    """A class to configure the ship"""

    def __init__(self,
            settings : Settings,
            screen : Surface):
        """Initialize ship object"""
        super(Ship, self).__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("images/ship.bmp").convert()
        self.image.set_colorkey((230,230,230))
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False

        self.speed = settings.ship_speed_factor
        self.center = float(self.rect.centerx)


    def update(self):
        """Update the ship's position"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.speed

        elif self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.speed
        
        self.rect.centerx = self.center


    def draw(self):
        """Draw the ship to the screen"""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """Update the ship's position to be in the center"""
        self.center = self.screen_rect.centerx
        self.update()
