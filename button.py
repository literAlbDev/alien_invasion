import pygame
import pygame.font

from settings import Settings


class Button:
    """Class to create button"""

    def __init__(self,
            settings : Settings,
            screen : pygame.Surface,
            msg : str):
        """Initialize button object"""
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 350, 50
        self.color = (0, 255, 0)
        self.font_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    
    def prep_msg(self, msg):
        """Prepare button to diaplay %msg"""
        self.msg_image = self.font.render(msg, True, self.font_color, self.color,)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    

    def draw_button(self):
        """Draw the button to the screen"""
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)