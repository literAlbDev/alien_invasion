import pygame
from pygame.sprite import Sprite
from pygame import Surface

from settings import Settings
from ship import Ship

class Bullet(Sprite):
    """The bullets class"""

    def __init__(self,
            settings : Settings,
            screen : Surface,
            ship : Ship):
        """Initialize the bullet object"""
        super(Bullet,self).__init__()

        self.settings = settings
        self.screen = screen
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)


    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed_factor
        # Update the rect position.
        self.rect.y = self.y

    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)