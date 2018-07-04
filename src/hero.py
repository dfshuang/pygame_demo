"""凯欢完成"""
import math
import pygame as pg
from bullet import *
import game_function as gf
from pygame.sprite import Sprite
import time


class Hero(Sprite):
    def __init__(self, screen, sett, stats):
        """初始化hero并设置其初始位置"""
        super(Hero, self).__init__()
        self.screen = screen
        self.sett = sett
        self.stats = stats
        # 加载hero图像并获取其外接矩形
        self.images = {}
        self.init_images()
        # self.image=pg.image.load('../image/hero/run_80.gif')
        self.image = self.images['stand'][2]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 初始位置（待改）
        self.rect.centerx = 0.5 * (self.screen_rect.centerx + self.screen_rect.left)
        self.rect.bottom = self.screen_rect.bottom
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.life = sett.hero_life
        self.speed = sett.hero_speed
        # hero占有的飞机或坦克,记得离开敌机时把它变为None
        self.plane = None

        # 射击方向（水平向右为0度，按d or c可以改变shoot_dir）
        self.shoot_dir = 0

        # 射击杀伤力
        self.lethality = 1

        # 开导弹机时要轰炸的目标
        self.missile_target = None

        # 向左还是向右
        self.face_right = True

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.jumporfall = False  # 跳跃或下落
        self.jumpfallspeed = 0  # 在空中的竖直速度
        self.jump_init_speed = sett.jump_init_speed  # 起跳时的竖直速度

        # 用于跑步动画
        self.clock = 0  # Clock对象
        self._t = 0  # 记录时间
        self.imgnum = 0  # image的序号

        # 用于技能
        self.cooling_time = sett.hero_skill_cooling_time  # 技能冷却时间
        self.cool_finished = True  # 冷却完成与否
        self.skilling = False  # 是否正在使用技能
        self.skill_time = 0.0  # 技能已经冷却的时间
        self.shoot_dir0 = 0.0  # 其中一个发射角度

    def init_images(self):
        self.images['run'] = []
        self.images['stand'] = []
        self.images['jump'] = [0, 0]

        # 初始化images['run']
        for i in range(10):
            self.images['run'].append([])
        for i in range(7, 10):
            for j in range(8):
                self.images['run'][i].append(pg.image.load('../image/hero/run_' + str(i) + str(j) + '.gif'))
        for i in range(2, 5):
            for j in range(8):
                self.images['run'][i].append(pg.transform.flip(self.images['run'][i + 5][j], True, False))
        for i in range(5, 7):
            n = 7 if i == 5 else 8
            for j in range(n):
                self.images['run'][i].append(pg.image.load('../image/hero/run_' + str(i) + str(j) + '.png'))
            if i == 5:
                self.images['run'][i].append(pg.image.load('../image/hero/run_' + str(i) + '7.gif'))

        for i in range(0, 2):
            for j in range(8):
                self.images['run'][i].append(pg.transform.flip(self.images['run'][i + 5][j], True, False))

        # images['stand']
        for i in range(10):
            self.images['stand'].append(pg.image.load('../image/hero/stand_' + str(i) + '.gif'))
            tmp = self.images['stand'][i]
            tmp_rect = tmp.get_rect()
            self.images['stand'][i] = pg.transform.scale(tmp, (int(tmp_rect.width * 1.3), int(tmp_rect.height * 1.3)))
        # images['jump']
        self.images['jump'][1] = pg.image.load('../image/hero/jump_1.gif')
        self.images['jump'][0] = pg.transform.flip(self.images['jump'][1], True, False)

    def drawme(self):
        """在指定位置绘制hero"""
        if self.plane:
            self.screen.blit(self.plane.image, self.plane.rect)
        else:
            self.screen.blit(self.image, self.rect)

    def update(self, bullets, bursts, t_interval, stats, sb, sett, screen, sound):
        """
        :param t_interval: 根据屏幕刷新时间改变移动距离
        :param stats: 当前统计信息
        :param sb: 积分榜
        """
        if self.skilling:
            self.super_skill(sett, screen, bullets, t_interval)
        elif not self.cool_finished:
            self.skill_cooling(t_interval)

        # 如果没驾驶飞机
        if not self.plane:
            move_distance = t_interval * self.speed

            if self.moving_right:
                if self.x < sett.screen_width:
                    self.x += move_distance
                    self.rect.centerx = self.x
                    # 实现跑动中的动态效果
                    self._t += self.clock.tick()
                    if self._t >= 800:
                        self._t = 0
                    tmp = int(self._t // 100)
                    if tmp != self.imgnum:
                        self.imgnum = tmp
                        self.image = self.images['run'][int(self.shoot_dir // (math.pi / 4) + 2)][self.imgnum]
                        tmprect = self.rect
                        self.rect = self.image.get_rect()
                        self.rect.centerx, self.rect.centery = tmprect.centerx, tmprect.centery

            if self.moving_left:
                if self.x > 0:
                    self.x -= move_distance
                    self.rect.centerx = self.x
                    # 实现跑动中的动态效果
                    self._t += self.clock.tick()
                    if self._t >= 800:
                        self._t = 0
                    tmp = int(self._t // 100)
                    if tmp != self.imgnum:
                        self.imgnum = tmp
                        if self.shoot_dir > 0:
                            index = int(11 - self.shoot_dir // (math.pi / 4))
                        else:
                            index = int(3 - self.shoot_dir // (math.pi / 4))

                        self.image = self.images['run'][index][self.imgnum]
                        tmprect = self.rect
                        self.rect = self.image.get_rect()
                        self.rect.centerx, self.rect.centery = tmprect.centerx, tmprect.centery

            if self.jumporfall:
                move_distance = t_interval * self.jumpfallspeed
                speed_change = t_interval * self.sett.acc
                self.y += move_distance
                self.jumpfallspeed += speed_change
                self.rect.centery = self.y
                # 碰到上界
                if self.rect.top < 0:
                    self.rect.top = 0
                    self.y = float(self.rect.centery)
                    self.jumpfallspeed = 0
                # 落地后停止下落
                elif self.rect.bottom >= self.sett.groundy:
                    self.rect.bottom = self.sett.groundy
                    self.jumporfall = False
                    # 改变姿势
                    if self.face_right:
                        if not (self.shoot_dir >= -math.pi / 2 and self.shoot_dir <= math.pi / 2):
                            self.shoot_dir = 0
                        self.image = self.images['stand'][int(self.shoot_dir // (math.pi / 4) + 2)]
                    else:
                        if self.shoot_dir > -math.pi / 2 and self.shoot_dir < math.pi / 2:
                            self.shoot_dir = math.pi
                        if self.shoot_dir < 0:
                            self.image = self.images['stand'][int(3 - self.shoot_dir // (math.pi / 4))]
                        else:
                            self.image = self.images['stand'][int(11 - self.shoot_dir // (math.pi / 4))]
        # 如果驾驶飞机
        else:
            # 判断是否超过驾驶时限, 运行时间 > 被劫机时间 + 可驾驶时间
            self.plane.jackedTime += t_interval
            planeTimeLeft = self.plane.time_limit - self.plane.jackedTime
            if planeTimeLeft <= 0:
                # 超时
                gf.start_burst(True, self, bursts, sound)
                self.plane = None
                self.life -= 1
                self.face_right = True
                self.shoot_dir = 0
                self.jumporfall = True
                self.jumpfallspeed = 0
            else:
                move_distance = t_interval * 3 * self.plane.speed
                if self.plane.moving_udlr[3]:
                    if self.plane.x < sett.screen_width:
                        self.plane.x += move_distance
                        self.plane.rect.centerx = self.plane.x

                if self.plane.moving_udlr[2]:
                    if self.plane.x > 0:
                        self.plane.x -= move_distance
                        self.plane.rect.centerx = self.plane.x
                if self.plane.moving_udlr[0]:
                    if self.plane.y > 0:
                        self.plane.y -= move_distance
                        self.plane.rect.centery = self.plane.y
                if self.plane.moving_udlr[1]:
                    if self.plane.y < self.screen_rect.height:
                        self.plane.y += move_distance
                        self.plane.rect.centery = self.plane.y

                # 让hero.rect的位置与hero.plane.rect的位置保持一致
                self.x, self.y = self.plane.x, self.plane.y
                self.rect.centerx, self.rect.centery = self.x, self.y

        # 刷新主角生命值和飞机生命值
        stats.heroLife = self.life
        if self.plane:
            stats.planeTimeLimit = planeTimeLeft
            stats.planeLife = self.plane.life
        else:
            stats.planeTimeLimit = 0
            stats.planeLife = 0

        # 判断是否生命值以为0，每次游戏可以复活2次，三次机会用完了就得重新开始
        if self.life <= 0:
            sound.do_play['die'] = True
            # stats.hero_left -= 1
            sb.pHeros = True
            if stats.hero_left <= 0:
                stats.game_windows['game_active'] = False
                stats.game_windows['game_over'] = True

                # 角色死后，记录分数信息
                with open("record.txt", 'a+') as fw:
                    fw.write(str(stats.high_score) + '\n')

            self.life = sett.hero_life

    def super_skill(self, sett, screen, bullets, t_interval):
        """技能"""
        tmp = self.shoot_dir0
        self.shoot_dir0 = (self.skill_time // 100) * (math.pi / 25)
        if self.shoot_dir0 > tmp:
            if self.shoot_dir0 > 2 * math.pi:
                self.skilling = False
                self.skill_time = 0.0
                self.shoot_dir0 = 0.0
                return
            for i in range(6):
                bullet = Bullet0(sett, screen, self, self.shoot_dir0 + i * (math.pi / 3), True, 3)
                bullets[0].add(bullet)

        self.skill_time += t_interval * 1000

    def skill_cooling(self, t_interval):
        """技能冷却"""
        self.skill_time += t_interval * 1000
        self.stats.hero_skill_cooling_time = self.sett.hero_skill_cooling_time - self.skill_time
        if self.skill_time > self.cooling_time:
            self.cool_finished = True
            self.skill_time = 0.0
            self.stats.hero_skill_cooling_time = 0
