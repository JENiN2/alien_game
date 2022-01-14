from typing import Union, Sequence, Tuple, Callable

from pygame.sprite import Group
from pygame import Surface

from sprites import Alien


class AlienFleet(Group):
    def __init__(
            self, screen: Surface, settings, sprites: Union[Alien, Sequence[Alien]], gameover_callback: Callable
    ):
        super().__init__(sprites)
        self.screen = screen
        self.settings = settings
        self.gameover_callback = gameover_callback

    def get_aliens_matrix_size(self) -> Tuple[int, int]:
        alien = Alien(self.settings, self.screen)
        ship_height = 200  # todo: fix this somehow
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        
        avalible_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = int(avalible_space_x / (2 * alien_width))

        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))

        return number_aliens_x, number_rows

    def create_fleet(self):
        number_aliens_x, number_rows = self.get_aliens_matrix_size()
        for row_numbers in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_numbers)

    def create_alien(self, alien_number, row_number):
        self.alien = Alien(self.settings, self.screen)
        alien_width = self.alien.rect.width
        self.alien.x = alien_width + 2 * alien_width * alien_number
        self.alien.rect.x = self.alien.x
        self.alien.rect.y = self.alien.rect.height + 2 * self.alien.rect.height * row_number

        self.add(self.alien)

    def check_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.sprites():
            if alien.check_edges():  # type: ignore
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем.
                self.ship_hit()

                break

    def ship_hit(self):
        self.gameover_callback()
