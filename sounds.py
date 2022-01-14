import pygame


class SoundFX:

    def __init__(self):
        self.music()
        self.ship = pygame.mixer.Sound("sounds/ship_moving.ogg")

        self.shoot = pygame.mixer.Sound("sounds/laser_shoot.wav")
        self.expl = pygame.mixer.Sound("sounds/explosion.wav")
        self.play = pygame.mixer.Sound("sounds/button_click.wav")

    def music(self):
        pygame.mixer.music.load("music/space_ambient.wav")
        pygame.mixer.music.play(-1)

    def shoot_fx(self):
        self.shoot.set_volume(0.2)
        self.shoot.play()

    def explosion(self):
        self.expl.set_volume(0.1)
        self.expl.play()

    def button_click(self):
        self.play.set_volume(0.3)
        self.play.play()

    def ship_moving(self):
        self.ship.set_volume(0.5)
        self.ship.play()

    def ship_stop(self):
        self.ship.stop()
