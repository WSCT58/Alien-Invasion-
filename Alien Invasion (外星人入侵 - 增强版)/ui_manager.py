import pygame.font


class UIManager:
    """管理游戏的 UI 界面（开始屏幕、结束屏幕等）"""

    def __init__(self, ai_game):
        """初始化 UI 属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (255, 255, 255)  # 白色文字

        # 初始化字体
        self.title_font = pygame.font.SysFont(None, 100)  # 大标题字体
        self.info_font = pygame.font.SysFont(None, 50)  # 说明文字字体

    def show_start_screen(self):
        """绘制开始界面"""
        self._draw_text("ALIEN INVASION", self.title_font, -80)
        self._draw_text("Press Play to Start", self.info_font, 80)

    def show_game_over(self):
        """绘制结束界面"""
        # 1. "GAME OVER" 大标题 -> 往上挪 (y = -120)
        self._draw_text("GAME OVER", self.title_font, -120)

        # 2. 显示最终得分 -> 往上挪 (y = -60)
        score_str = f"Final Score: {round(self.stats.score, -1):,}"
        self._draw_text(score_str, self.info_font, -60)

        # (屏幕中间 y=0 的位置是留给 Play 按钮的)

        # 3. 【新增】提示按 Q 退出 -> 往下挪 (y = +80)
        self._draw_text("Press 'Q' to Quit", self.info_font, 80)

    def _draw_text(self, msg, font, offset_y):
        """辅助方法：渲染文字并居中"""
        msg_image = font.render(msg, True, self.text_color, self.settings.bg_color)
        msg_rect = msg_image.get_rect()
        msg_rect.center = self.screen_rect.center
        msg_rect.centery += offset_y
        self.screen.blit(msg_image, msg_rect)