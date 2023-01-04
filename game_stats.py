from settings import Settings

class GameStats():
    """Track statistics for Alien Invasion."""
    
    def __init__(self,
            settings : Settings):
        """Initialize game statistics."""
        self.settings = settings
        self.highscore = 0
        self.reset_stats()
        self.get_stats()
        for _ in range(self.level):
            self.settings.increase_speed()
    

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.game_active = False
        self.score = 0
        self.level = 0
    

    def save_stats(self):
        """Save game statistics in data file"""
        with open(".data.bin", "w") as file:
            file.writelines(
                str(self.highscore) + "\n" +
                str(self.score) + "\n" +
                str(self.level)
                )


    def get_stats(self):
        """Get the game statistics from data file"""
        try:
            with open(".data.bin", "r") as file:
                self.highscore = int(file.readline())
                self.score     = int(file.readline())
                self.level     = int(file.readline())
        except:
            print("no file game_stats.bin")