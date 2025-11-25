import pygame


class SkillBar:
    """管理飞船技能充能条的类"""

    def __init__(self, ai_game):
        """初始化技能条属性"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # --- 技能参数 ---
        self.max_charge = 5  # 需要击杀 5 个敌人
        self.current_charge = 0  # 当前充能

        # --- 绘制参数 ---
        self.width = 200  # 条的总宽度
        self.height = 15  # 条的高度
        self.border_color = (255, 255, 255)  # 边框颜色（白色）
        self.bar_color = (0, 255, 0)  # 充能颜色（绿色）
        self.ready_color = (255, 215, 0)  # 满能量颜色（金色）
        self.bg_color = (100, 100, 100)  # 背景底色（深灰）

        # --- 位置设置 ---
        # 放在屏幕顶部居中，稍微靠下一点，避开分数
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = 50

    def charge(self):
        """增加充能"""
        if self.current_charge < self.max_charge:
            self.current_charge += 1

    def reset(self):
        """重置充能（使用技能后）"""
        self.current_charge = 0

    def is_ready(self):
        """检查技能是否就绪"""
        return self.current_charge >= self.max_charge

    def draw_bar(self):
        """在屏幕上绘制技能条"""
        # 1. 绘制背景（底条）
        pygame.draw.rect(self.screen, self.bg_color, self.rect)

        # 2. 计算当前充能的宽度
        fill_width = (self.current_charge / self.max_charge) * self.width
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.height)

        # 3. 决定颜色：如果满了用金色，没满用绿色
        if self.is_ready():
            color = self.ready_color
        else:
            color = self.bar_color

        # 4. 绘制充能条
        pygame.draw.rect(self.screen, color, fill_rect)

        # 5. 绘制外边框（让它更好看）
        pygame.draw.rect(self.screen, self.border_color, self.rect, 2)