import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    """表示一颗星星的类"""

    def __init__(self, ai_game):
        """初始化星星并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 1. 创建星星的图形（这里我们做一个 2x2 像素的小矩形）
        self.image = pygame.Surface((2, 2))
        self.image.fill((200, 200, 200)) # 稍微暗一点的白色，避免太刺眼

        # 2. 获取矩形属性
        self.rect = self.image.get_rect()

        # 3. 随机设置位置
        self.rect.x = randint(0, self.settings.screen_width)
        self.rect.y = randint(0, self.settings.screen_height)