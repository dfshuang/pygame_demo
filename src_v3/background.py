"""
迪润完成
可自行拆分为多个文件
"""

import pygame as pg
from pygame.sprite import Group
from pygame.sprite import Sprite


class Background():
    def __init__(self, sett):
        self.skys = []
        self.lands = []
        for i in range(2):
            self.skys.append(pg.image.load('../image/bg/sky' + str(i) + '.png'))
            self.lands.append(pg.image.load('../image/bg/land' + str(i) + '.png'))
        self.fullimage = self.skys[0]
        self.images = [0, 0]
        self.rects = [0, 0]
        self.images[0] = self.fullimage.subsurface(pg.Rect((0, 0), (1200, 800)))
        self.images[1] = self.lands[0]
        for i in range(2):
            self.rects[i] = self.images[i].get_rect()
        self.rects[1].bottom = sett.screen_height
        self.time = 0.0
        self.clock = pg.time.Clock()
        self.T = (4033 - 1200) * 30.0

    def update(self):
        self.time += self.clock.tick()
        if self.time > self.T:
            self.time = 0
        i = int(self.time // 30)
        self.images[0] = self.fullimage.subsurface(pg.Rect((i, 0), (1200, 800)))

    def drawme(self, screen):
        for i in range(2):
            screen.blit(self.images[i], self.rects[i])


class Sound():
    def __init__(self):
        self.do_play = {'fire': False, 'missile': False, 'burst': False, 'hijacked': False, 'upgrade': False,
                        'die': False}
        self.sound = {}
        self.init_sound()

    def init_sound(self):
        self.sound['fire'] = pg.mixer.Sound('../sound/hero_fire.wav')
        self.sound['missile'] = pg.mixer.Sound('../sound/missile.wav')
        self.sound['burst'] = pg.mixer.Sound('../sound/burst.wav')
        self.sound['hijacked'] = pg.mixer.Sound('../sound/hijacker.wav')
        self.sound['upgrade'] = pg.mixer.Sound('../sound/upgrade.wav')
        self.sound['die'] = pg.mixer.Sound('../sound/die.wav')

    def play_snd(self, sett):
        if not sett.quiet:
            for action, val in self.do_play.items():
                if val:
                    self.sound[action].play()
                    self.do_play[action] = False
