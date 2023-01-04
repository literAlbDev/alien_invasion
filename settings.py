class Settings():
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's settings."""
        #Screen settings
        self.screen_width = 900
        self.screen_height = 950
        self.bg_color = (200, 200, 200)
        #Bullet settings
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        #Aliens settings
        self.fleet_drop_speed = 50
        #Game settings
        self.ship_limit = 3
        self.levelup_scale = 1.2
        self.score_scale = 1.5

        self.init_dynamic_settings()

    
    def init_dynamic_settings(self):
        """Initialize game's settings that changes with time"""
        #Ship settings
        self.ship_speed_factor = 1.5
        #Bullet settings
        self.bullet_speed_factor = 2
        self.bullet_width = 5
        #Aliens settings
        self.alien_speed_factor = 0.5
        self.fleet_direction = 1
        self.alien_points = 50
    

    def increase_speed(self):
        """Increase the challenge level of the game"""
        self.ship_speed_factor *= self.levelup_scale
        self.alien_speed_factor *= self.levelup_scale
        self.bullet_speed_factor *= self.levelup_scale
        self.bullet_width *= self.levelup_scale

        self.alien_points *= self.score_scale
        self.alien_points = int(round(self.alien_points, -1))