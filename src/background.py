"""
迪润完成
可自行拆分为多个文件
"""

import pygame as pg
from pygame.sprite import Group
from pygame.sprite import Sprite


class Background():
    def __init__(self, sett, stats):

        self.stats = stats
        self.sett=sett
        self.type='bluesky'
        self.skys = []
        self.lands = []
        for i in range(2):
            self.skys.append(pg.image.load('../image/bg/sky' + str(i) + '.png'))
            self.lands.append(pg.image.load('../image/bg/land' + str(i) + '.png'))
        self.fullimage = self.skys[0]
        self.images = [0, 0]
        self.rects = [0, 0]
        self.images[0] = self.fullimage.subsurface(pg.Rect((0, 0), (1000, 600)))
        self.images[1] = self.lands[0]
        for i in range(2):
            self.rects[i] = self.images[i].get_rect()
        self.rects[1].bottom = sett.screen_height
        self.time = 0.0
        self.fullrect=self.fullimage.get_rect()
        self.T = (self.fullrect.width - 1000) * sett.bgmoveT

    def update(self, t_interval):
        if not self.stats.game_windows['game_pause']:
            self.time += t_interval * 1000
        if self.time > self.T:
            self.time = 0
        i = int(self.time // self.sett.bgmoveT)
        self.images[0] = self.fullimage.subsurface(pg.Rect((i, 0), (1000, 600)))

    def drawme(self, screen):
        for i in range(2):
            screen.blit(self.images[i], self.rects[i])


class Sound():
    def __init__(self):
        self.do_play = {'fire': False, 'missile': False, 'skill': False, 'hitted': False, 'burst': False,
                        'hijacked': False, 'upgrade': False, 'die': False}
        self.sound = {}
        self.init_sound()

    def init_sound(self):
        self.sound['fire'] = pg.mixer.Sound('../sound/hero_fire.wav')
        self.sound['missile'] = pg.mixer.Sound('../sound/missile.wav')
        self.sound['skill'] = pg.mixer.Sound('../sound/skill.wav')
        self.sound['hitted'] = pg.mixer.Sound('../sound/hitted.wav')
        self.sound['burst'] = pg.mixer.Sound('../sound/burst.wav')
        self.sound['hijacked'] = pg.mixer.Sound('../sound/hijacker.wav')
        self.sound['upgrade'] = pg.mixer.Sound('../sound/upgrade.wav')
        self.sound['die'] = pg.mixer.Sound('../sound/die.wav')

    def play_snd(self, stats):
        if not stats.game_windows['quiet']:
            for action, val in self.do_play.items():
                if val:
                    self.sound[action].play()
                    self.do_play[action] = False
