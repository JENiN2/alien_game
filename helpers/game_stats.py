import pathlib


class GameStats:
    HIGHSCORE_FILENAME = 'highscore_save.txt'
    """Отслеживание статистики для игры Alien Invasion."""
    def __init__(self, settings):
        """Инициализирует статистику."""
        self.score = 0
        self.level = 0
        self.ships_left = 0

        self.settings = settings
        self.reset_stats()
        # Игра Alien Invasion запускается в неактивном состоянии.
        self.game_active = False
        # Рекорд не должен сбрасываться.
        self.high_score = 0
        self.last_high_score = 0
        self.load_highscore()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 0

    def load_highscore(self):
        parent_dir = pathlib.Path(__file__).parent.parent
        score_file_path = parent_dir / self.HIGHSCORE_FILENAME
        if not score_file_path.exists():
            return
        try:
            with open(score_file_path.absolute(), 'rt') as f:
                self.high_score = int(f.read())
                self.last_high_score = self.high_score
        except:
            pass

    def write_highscore(self):
        if self.high_score > self.last_high_score:
            with open(self.HIGHSCORE_FILENAME, 'wt') as f:
                f.write(str(self.score))
