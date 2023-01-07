from random import randint

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game import Game
from star import Star
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard

#Initialize pygame
pygame.init()
pygame.display.set_caption("Alien Invation")

#Initialize all objects of the game
settings = Settings()
screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))

ship = Ship(settings, screen)
bullets = Group()
aliens = Group()
    #Create random star pattern
stars = Group()
for i in range(randint(10,100)):
    star = Star(screen)
    star.rect.x = randint(0,settings.screen_width)
    star.rect.y = randint(0,settings.screen_height)
    stars.add(star)

play_button = Button(settings, screen, "Play (press p to start)")
game_stats = GameStats(settings)
scoreboard = Scoreboard(settings, screen, game_stats)
#Pass all game objects to game class to configure the game and make it ready to start
game = Game(settings, screen, ship, bullets, aliens, stars, play_button, game_stats, scoreboard)

while True:        
    game.game_loop()