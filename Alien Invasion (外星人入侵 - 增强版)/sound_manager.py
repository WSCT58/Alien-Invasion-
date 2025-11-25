import pygame

class SoundManager:
    """专门负责管理游戏音频的类"""

    def __init__(self):
        """初始化混音器并加载所有声音"""
        # 确保 mixer 已经初始化
        pygame.mixer.init()

        # --- 1. 加载背景音乐 ---
        try:
            pygame.mixer.music.load('sounds/bgm.mp3')
            pygame.mixer.music.set_volume(0.5) # 设置 BGM 音量
        except FileNotFoundError:
            print("警告：找不到背景音乐文件 (sounds/bgm.mp3)")

        # --- 2. 加载音效 ---
        # 为了防止某个文件缺失导致游戏崩溃，我们用辅助方法加载
        self.shoot_sound = self._load_sound('sounds/shoot.wav', 0.4)
        self.skill_sound = self._load_sound('sounds/laser_skill.wav', 0.6)
        self.explosion_sound = self._load_sound('sounds/explosion.wav', 0.3)

    def _load_sound(self, path, volume):
        """辅助方法：安全加载音效"""
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except FileNotFoundError:
            print(f"警告：找不到音效文件 ({path})")
            return None

    # --- 3. 提供对外的播放接口 ---

    def play_bgm(self):
        """播放背景音乐（循环）"""
        try:
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def play_shoot(self):
        """播放普通射击音效"""
        if self.shoot_sound:
            self.shoot_sound.play()

    def play_skill(self):
        """播放技能音效"""
        if self.skill_sound:
            self.skill_sound.play()

    def play_explosion(self):
        """播放爆炸音效"""
        if self.explosion_sound:
            self.explosion_sound.play()