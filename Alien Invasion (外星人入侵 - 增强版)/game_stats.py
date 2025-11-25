import json  #导入 json 模块

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        #画界面标记
        self.game_over = False
        # Start Alien Invasion in an active state.
        self.game_active = False

        # High score should never be reset.
        # <--- 2. 这里原来是 self.high_score = 0，改成下面这样：
        self.high_score = self.get_saved_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def get_saved_high_score(self):
        """Gets high score from file, if it exists."""
        try:
            with open('high_score.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return 0  # 如果文件不存在（第一次玩），就返回 0