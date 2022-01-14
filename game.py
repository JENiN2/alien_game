import sys

import pygame

from sprites import Bullet, Ship
from helpers.button import Button
from helpers.game_stats import GameStats
from helpers.scoreboard import Scoreboard
from sprite_groups import AlienFleet
from sounds import SoundFX
from sprites.explosion import Explosion


class Game:
    def __init__(self, settings):
        pygame.display.set_caption("Alien invasion")
        self.settings = settings
        self.screen = pygame.display.set_mode(
            (settings.screen_width, settings.screen_height)
        )
        self.background = pygame.image.load("images/purple_background2.jpg")
        self.ship = Ship(screen=self.screen, ai_settings=settings)
        self.play_button = Button(self.screen, 'Play')
        self.stats = GameStats(settings)
        self.scoreboard = Scoreboard(settings, self.screen, self.stats)
        self.ship = Ship(settings, self.screen)
        self.bullets = pygame.sprite.Group()

        self.aliens = AlienFleet(
            screen=self.screen, settings=settings, sprites=[], gameover_callback=self.check_gameover
        )

        self.sound = SoundFX()
        self.expl = Explosion(0, 0)

    def run(self):
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()

            # При каждом проходе цикла перерисовывается экран.
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.write_highscore()
                sys.exit()
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                self.check_key_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.check_clicked() and not self.stats.game_active:
                    self.sound.button_click()
                    self.initialize_game()
                elif self.stats.game_active and event.button == 1:
                    self.sound.shoot_fx()
                    self.fire_bullet()

    def check_key_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
                self.sound.ship_moving()
            elif event.key == pygame.K_d:
                self.ship.moving_right = True
                self.sound.ship_moving()
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
                self.sound.ship_moving()
            elif event.key == pygame.K_a:
                self.ship.moving_left = True
                self.sound.ship_moving()
            elif event.key == pygame.K_SPACE:
                self.sound.shoot_fx()
                self.fire_bullet()
            elif event.key == pygame.K_p:
                if self.stats.game_active is False:
                    self.sound.button_click()
                    self.initialize_game()
            elif event.key == pygame.K_ESCAPE:
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
            elif event.key == pygame.K_q:
                self.stats.write_highscore()
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
                self.sound.ship_stop()
            elif event.key == pygame.K_d:
                self.ship.moving_right = False
                self.sound.ship_stop()
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False
                self.sound.ship_stop()
            elif event.key == pygame.K_a:
                self.ship.moving_left = False
                self.sound.ship_stop()

    def fire_bullet(self):
        # Создание новой пули и включение ее в группу bullets.
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self.settings, self.screen, self.ship))

    def initialize_game(self):
        self.settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        self.stats.game_active = True
        self.stats.reset_stats()
        self.aliens.empty()
        self.bullets.empty()
        self.ship.center_ship()
        self.scoreboard.prep_score()
        self.scoreboard.prep_high_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()

    def check_gameover(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left.
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Очистка списков пришельцев и пуль.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self.aliens.create_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def update_screen(self):
        self.screen.blit(self.background, (0, 0))
        # self.screen.fill(self.settings.bg_color)
        # Все пули выводятся позади изображений корабля и пришельцовю
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # Отрисовка взрывов.
        self.expl.explosion_group.draw(self.screen)
        self.expl.explosion_group.update()

        # Вывод счета.
        self.scoreboard.show_score()

        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def update_bullets(self):
        """Обновляет позиции пуль и уничтожает старые пули."""
        # Обновление позиций пуль.
        self.bullets.update()
        # Удаление пуль, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self, ):
        """Обработка коллизий пуль с пришельцами."""
        # Удаление пуль и пришельцев, участвующих в коллизиях.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.sound.explosion()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    x = alien.rect.x
                    y = alien.rect.y
                    explosion = Explosion(x, y)
                    self.expl.explosion_group.add(explosion)
            self.scoreboard.prep_score()
            if self.stats.score > self.stats.high_score:
                self.stats.high_score = self.stats.score
                self.scoreboard.prep_high_score()
        if len(self.aliens) == 0:
            # Уничтожение существующих пуль, повышеник скорости.
            self.bullets.empty()
            self.settings.increase_speed()
            # Увеличение уровня
            self.stats.level += 1
            self.scoreboard.prep_level()
            # Создание нового флота
            self.aliens.create_fleet()

    def update_aliens(self):
        """Проверяет, достиг ли флот края экрана, после чего обновляет позиции всех пришельцев во флоте."""
        self.aliens.check_edges()
        self.aliens.update()
        # Проверка коллизий "пришелец-корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.check_gameover()
        # Проверка пришельцев, добравшихся до нижнего края экрана.
        self.aliens.check_bottom()
