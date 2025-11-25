import sys
from time import sleep
import json
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
#新增的库
from star import Star
from ui_manager import UIManager
from skill_bar import SkillBar
from laser import Laser
from sound_manager import SoundManager

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        #BGM设置
        self.sounds = SoundManager()
        self.sounds.play_bgm()  # 游戏启动就开始放歌

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # 实例化 UI 管理器
        self.ui = UIManager(self)

        self.ship = Ship(self)
        #实例化技能
        self.skill_bar = SkillBar(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        #技能
        self.lasers = pygame.sprite.Group()
        # --- 新增：创建星星编组 ---
        self.stars = pygame.sprite.Group()
        self._create_stars()  # 调用下面定义的方法

        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        self.game_over = False
        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                # 更新激光（处理倒计时和消失）
                self.lasers.update()

            self._update_screen()
            self.clock.tick(60)

    def _close_game(self):
        """Save high score and exit."""
        saved_high_score = self.stats.high_score

        # 将最高分写入文件
        with open('high_score.json', 'w') as f:
            json.dump(saved_high_score, f)

        sys.exit()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._close_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            #重置状态
            self.stats.game_over = False
            # Reset the game statistics.
            self.stats.reset_stats()
            # 新游戏开始时，把技能条归零
            self.skill_bar.reset()

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._close_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_UP:
            self._activate_skill()

    def _activate_skill(self):
        """释放大招：激光贯穿！"""
        if self.skill_bar.is_ready():
            # 1. 消耗能量
            self.skill_bar.reset()
            #BGM
            self.sounds.play_skill()
            # 2. 创建激光对象
            new_laser = Laser(self)
            self.lasers.add(new_laser)

            # 3. 【核心逻辑】检测激光击杀
            # groupcollide 参数说明：
            # group1 (lasers), group2 (aliens)
            # False: 激光碰撞后不消失（因为它要贯穿！）
            # True: 外星人碰撞后消失（被秒杀）
            collisions = pygame.sprite.groupcollide(
                self.lasers, self.aliens, False, True)

            # 4. 计分
            if collisions:
                #BGM
                self.sounds.play_explosion()
                for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                    # 注意：大招击杀的敌人通常不给技能条充能，防止无限大招
                    # 所以这里不需要调用 self.skill_bar.charge()

                self.sb.prep_score()
                self.sb.check_high_score()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sounds.play_shoot()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            self.sounds.play_explosion()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                #每击杀一个敌人，给技能条充能
                for _ in range(len(aliens)):
                    self.skill_bar.charge()

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_over = True
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_stars(self):
        """生成一片星空"""
        # 这里我们可以生成 50 到 100 颗星星
        for _ in range(100):
            star = Star(self)
            self.stars.add(star)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)

        '''for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()'''

        #只有游戏进行中才画飞船和外星人
        if self.game_active:
            self.ship.blitme()
            self.aliens.draw(self.screen)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # 绘制激光
            for laser in self.lasers.sprites():
                laser.draw_laser()
            self.sb.show_score()
            # 技能条
            self.skill_bar.draw_bar()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

            #使用 self.ui 来调用方法
            if self.stats.game_over:
                self.ui.show_game_over()
            else:
                self.ui.show_start_screen()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()