import pygame
from pygame.sprite import Sprite


class BossBullet(Sprite):
    """Boss 发射的子弹"""

    def __init__(self, ai_game, boss):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 在 (0,0) 处创建一个子弹矩形，然后设置正确位置
        self.rect = pygame.Rect(0, 0, 5, 15)  # 宽5，高15
        self.rect.midbottom = boss.rect.midbottom

        self.y = float(self.rect.y)
        self.speed = self.settings.bullet_speed * 0.6  # Boss子弹慢一点
        self.color = (255, 50, 50)  # 红色子弹

    def update(self):
        """向下移动子弹"""
        self.y += self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)