import pygame
from pygame.sprite import Sprite


class Boss(Sprite):
    """表示关卡 Boss 的类"""

    def __init__(self, ai_game):
        """初始化 Boss 并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # --- 加载 Boss 图像 ---
        try:
            # 1. 加载名为 boss.bmp 的图片 (或者 boss.png)
            # 确保你的 images 文件夹里有这张图
            self.image = pygame.image.load('images/boss.bmp')

            # 2. 调整大小：Boss 应该很大！
            # 这里我把它设定为 120x120 像素，你可以根据需要修改数字
            self.image = pygame.transform.scale(self.image, (120, 100))

        except FileNotFoundError:
            # 如果找不到图片，就画一个红色大方块作为备用
            print("警告：未找到 images/boss.bmp，使用方块代替。")
            self.image = pygame.Surface((120, 100))
            self.image.fill((200, 0, 0))

        self.rect = self.image.get_rect()

        # Boss 初始位置：屏幕上方中央
        self.rect.midtop = self.screen_rect.midtop
        self.rect.y += 60  # 稍微往下一点，留出顶部空隙

        # 存储 Boss 的准确位置
        self.x = float(self.rect.x)

        # --- Boss 属性设置 ---
        # 血量随等级提升：基础血量 50 + 等级 * 30
        self.max_health = 50 + (ai_game.stats.level * 30)
        self.current_health = self.max_health

        # 移动方向：1 为右，-1 为左
        self.direction = 1
        # 速度设定：比普通外星人稍微快一点
        self.speed = self.settings.alien_speed * 1.5

    def update(self):
        """自动移动 Boss"""
        self.x += (self.speed * self.direction)
        self.rect.x = self.x
        self.check_edges()

    def check_edges(self):
        """如果 Boss 撞到边缘，改变方向"""
        if self.rect.right >= self.screen_rect.right:
            self.direction = -1
        elif self.rect.left <= 0:
            self.direction = 1

    def hit(self, damage=1):
        """Boss 受到伤害"""
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0

    def draw_health_bar(self):
        """在 Boss 头部上方绘制血条"""
        # 血条尺寸
        bar_width = self.rect.width  # 血条宽度等于 Boss 宽度
        bar_height = 10

        # 计算绿色（剩余血量）的宽度
        if self.max_health > 0:
            health_ratio = self.current_health / self.max_health
        else:
            health_ratio = 0
        fill_width = int(bar_width * health_ratio)

        # 血条位置：在 Boss 头顶上方 20 像素处
        bar_x = self.rect.left
        bar_y = self.rect.top - 20

        # 血条背景（红色）
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        # 剩余血量（绿色）
        fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)

        pygame.draw.rect(self.screen, (255, 0, 0), bg_rect)  # 红底
        pygame.draw.rect(self.screen, (0, 255, 0), fill_rect)  # 绿条
        pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 1)  # 白色边框

    def blitme(self):
        """在指定位置绘制 Boss 和血条"""
        self.screen.blit(self.image, self.rect)
        self.draw_health_bar()