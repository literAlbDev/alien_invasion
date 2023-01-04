import pygame
from pygame.sprite import Sprite
from pygame import Surface

from settings import Settings

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self,
            settings : Settings,
            screen : Surface):
        """Initialize alien object"""
        super(Alien, self).__init__()
        self.settings = settings
        self.screen = screen

        self.image = pygame.image.load("images/alien.bmp").convert()
        self.image.set_colorkey((230,230,230))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


    def check_edges(self):
        """Check if the alien hits the right or left edge of the screen"""
        if   self.rect.right >= self.screen_rect.right: return True
        elif self.rect.left  <= self.screen_rect.left : return True
        else : return False


    def update(self):
        """Update alien position"""
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = int(self.x)


    def draw(self):
        """Draw alien to the screen"""
        self.screen.blit(self.image, self.rect)
    
