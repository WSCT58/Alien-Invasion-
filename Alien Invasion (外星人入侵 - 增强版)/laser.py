import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    """表示贯穿全屏的激光束"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ship = ai_game.ship

        # 1. 创建激光的形状
        # 宽度 = 15像素（稍微宽一点），高度 = 屏幕高度
        self.width = 60
        self.height = self.settings.screen_height

        # 2. 创建矩形
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # 3. 设置位置：水平居中于飞船，底部对齐屏幕底部
        self.rect.centerx = self.ship.rect.centerx
        self.rect.bottom = self.ship.rect.bottom

        # 4. 颜色：青色/亮蓝色
        self.color = (0, 255, 255)

        # 5. 持续时间（帧数）
        # 假设 60帧/秒，设置 15 帧意味着激光显示 0.25秒
        self.timer = 15

    def update(self):
        """更新激光状态"""
        # 倒计时，时间到了就自我销毁
        self.timer -= 1
        if self.timer <= 0:
            self.kill()  # 从编组中移除自己

    def draw_laser(self):
        """在屏幕上绘制激光"""

        # =================================================
        # 【修改这里】不直接画 self.rect
        # =================================================

        # 1. 创建一个新的矩形，作为“视觉效果”
        # 宽度设为 40 ，高度不变
        visual_rect = pygame.Rect(0, 0, 40, self.height)

        # 2. 让这个视觉矩形的中心，对齐判定矩形的中心
        visual_rect.center = self.rect.center

        # 3. 只画这个细的矩形
        pygame.draw.rect(self.screen, self.color, visual_rect)
