import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.Surface((30, 30))
        self._image.fill(0, 0, 0)
        self._rect = self._image.get_rect()