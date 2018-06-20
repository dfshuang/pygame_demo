import pygame


class Burst(pygame.sprite.Sprite):
    def __init__(self, is_enemy, pos):
        super().__init__()

        self.images = [0, 0]
        for i in range(2):
            self.images[i] = pygame.image.load('../image/enemies/burst' + str(i) + '.png')
        if not is_enemy:
            self.images[0] = pygame.transform.scale(self.images[0], (50, 40))
            self.images[1] = pygame.transform.scale(self.images[1], (55, 44))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]
        self.time = 0.0

    def update(self, t_interval):
        self.time += t_interval * 1000
        if self.time > 800:
            self.image = self.images[1]
