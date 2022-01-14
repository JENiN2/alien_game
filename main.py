import pygame

from game import Game
from settings import Settings


if __name__ == '__main__':
    pygame.init()
    Game(settings=Settings()).run()
