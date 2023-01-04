import sys
from time import sleep

import pygame
from pygame import Surface
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard


class Game:
    """The main game class"""

    def __init__(self,
            settings : Settings,
            screen : Surface,
            ship : Ship,
            bullets : Group, 
            aliens : Group,
            stars : Group,
            play_button : Button,
            game_stats : GameStats,
            scoreboard : Scoreboard):
        """Initialize game's variables"""
        self.settings = settings
        self.screen = screen
        self.ship = ship
        self.bullets = bullets
        self.aliens = aliens
        self.stars = stars
        self.play_button = play_button
        self.game_stats = game_stats
        self.scoreboard = scoreboard

        self.alien_height = Alien(settings, screen).rect.height
        self.alien_width = Alien(settings, screen).rect.width

    #####GAME LOOP

    def game_loop(self):
        """The game loop that must be called to run the game"""
        #check multiple condition like wining and losing
        self.check_game_events()
        self.update_objects_positions()
        self.draw_objects()
        # Make the most recently drawn screen visible.
        pygame.display.flip()


    def check_game_events(self):
        """Check main game condistions like wining and losing"""
        self.check_input_events()
        self.check_bullet_hit_top()
        self.check_bullet_hit_alien()
        self.check_aliens_wins()


    def update_objects_positions(self):
        """Update objects positions"""
        if self.game_stats.game_active:
            self.ship.update()
            self.bullets.update()
            self.aliens.update()
            self.scoreboard.update()


    def draw_objects(self):
        """Draw objects to the screen using their new positions"""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.draw()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.scoreboard.show()
        if not self.game_stats.game_active:
            self.play_button.draw_button()
    
    #####CHECK INPUT EVENTS

    def check_input_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            #check mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x, mouse_y)  


    def check_keydown_events(self, event):
        """Respond to keydown events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullets()
        elif event.key == pygame.K_q:
            self.quit_game()
        elif event.key == pygame.K_p:
            if not self.game_stats.game_active: self.start_game()


    def fire_bullets(self):
        """Fire a bullet if limit not reached yet."""
        if self.game_stats.game_active:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self.settings, self.screen, self.ship)
                self.bullets.add(new_bullet)
                bullets_copy = self.bullets.copy()
                bullets_copy.remove(new_bullet)
                pygame.sprite.spritecollide(new_bullet, bullets_copy, True)


    def check_keyup_events(self, event):
        """Respond to keyup events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    
    def check_play_button(self, mouse_x, mouse_y):
        """Check if play button is clicked"""
        if self.play_button.rect.collidepoint(mouse_x, mouse_y):
            self.start_game()

    #####CHECK BULLETS

    def check_bullet_hit_top(self):
        """Response to bullets that hit the top of the screen"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 : self.bullets.remove(bullet)
    

    def check_bullet_hit_alien(self):
        """Response to when a bullet hits an alien"""
        #check if any bullet hit any alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            #give points for every alien hit
            for aliens in collisions.values():
                self.game_stats.score += self.settings.alien_points * len(aliens)
            #check highscore
            if self.game_stats.highscore < self.game_stats.score:
                self.game_stats.highscore = self.game_stats.score
            #if no aliens remaining start new level
            if len(self.aliens) == 0:
                self.levelup_game()

    #####CHECK ALIENS

    def check_aliens_wins(self):
        """Response to events of aliens wins the round"""
        #check if any alien hits the ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.game_over()
        # check if aany alien hits ground or right or left of the screen
        self.check_fleet_edges()


    def check_fleet_edges(self):
        """Response to the fleet hitting the right, left or top corner of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self.game_over()
                break
            if alien.check_edges():
                self.change_fleet_direction()
                break


    def change_fleet_direction(self):
        """Change the direction of all aliens of the fleet"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    #####MAIN GAME ACTIONS

    def quit_game(self):
        """Quit the game and save the latest game statistics"""
        self.game_stats.save_stats()
        pygame.quit()
        sys.exit()


    def start_game(self):
        """Activate the game status and start it"""
        self.game_stats.game_active = True
        pygame.mouse.set_visible(False)
        self.reset_game()


    def game_over(self):
        """Response to when the player loses a round to the aliens"""
        self.game_stats.ships_left -= 1
        if self.game_stats.ships_left == 0:
            pygame.mouse.set_visible(True)
            self.game_stats.reset_stats()
            self.settings.init_dynamic_settings()
        self.reset_game()

    
    def levelup_game(self):
        """Levelup the game"""
        self.settings.increase_speed()
        self.game_stats.level += 1
        self.reset_game()


    def reset_game(self):
        """Reset all objects of the game"""
        self.bullets.empty()
        self.aliens.empty()
        self.ship.center_ship()
        self.create_fleet()
        sleep(0.5)

    #####CREATE ALIEN FLEET

    def create_fleet(self):
        """Create a fleet"""
        rows_number = self.get_available_rows_number()
        for row_number in range(rows_number):
            self.create_row(row_number)


    def get_available_rows_number(self):
        """Get available rows number to place aliens"""
        available_screen_hight = self.settings.screen_height - (3 * self.alien_height) - self.ship.rect.height
        return int(available_screen_hight / (3 * self.alien_height))


    def create_row(self, row_number):
        """Create a row of aliens"""
        aliens_number = self.get_available_aliens_number()
        for alien_number in range(aliens_number):
            self.create_alien(alien_number, row_number)


    def get_available_aliens_number(self):
        """Get available places number in a row to place aliens"""
        available_screen_width = self.settings.screen_width - (2 * self.alien_width)
        return int(available_screen_width / (2 * self.alien_width))


    def create_alien(self, alien_number, row_number):
        """Create an alien and position him in right place in rows and columns"""
        alien = Alien(self.settings, self.screen)
        alien.rect.x = self.alien_width + 2 * self.alien_width * alien_number
        alien.rect.y = self.alien_height + 2 * self.alien_height * row_number
        self.aliens.add(alien)
        alien.x = alien.rect.x