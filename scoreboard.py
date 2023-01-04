import pygame
import pygame.font
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats

class Scoreboard:
    """Class for creating scoreboard"""

    def __init__(self,
            settings : Settings,
            screen : pygame.Surface,
            game_stats : GameStats):
        """Initialize scoreboard"""
        self.settings = settings
        self.game_stats = game_stats
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        self.text_color = (50,50,50)
        self.score_font = pygame.font.SysFont(None,48)
        self.highscore_font = pygame.font.SysFont(None,48)
        self.level_font = pygame.font.SysFont(None,48)
        self.update()
    

    def update(self):
        """Update scoreboard's values"""
        self.update_highscore()
        self.update_score()
        self.update_level()
        self.update_ships()


    def update_highscore(self):
        """Update scoreboard's highscore value"""
        self.highscore_image = self.highscore_font.render("{:,}".format(self.game_stats.highscore), True, self.text_color)
        self.highscore_rect = self.highscore_image.get_rect()
        self.highscore_rect.centerx = self.screen_rect.centerx
        self.highscore_rect.top = 20


    def update_score(self):
        """Update scoreboard's score value"""
        self.score_image = self.score_font.render("{:,}".format(self.game_stats.score), True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    

    def update_level(self):
        """Update scoreboard's level value"""
        self.level_image = self.level_font.render("level: " + str(self.game_stats.level), True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.screen_rect.right - 20
    

    def update_ships(self):
        """Update scoreboard's available ships value"""
        self.ships = Group()
        for ship_number in range(self.game_stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.top = 20
            ship.rect.left = ship_number * ship.rect.width
            self.ships.add(ship)
    
    
    def show(self):
        """Draw the scoreboard on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highscore_image, self.highscore_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)