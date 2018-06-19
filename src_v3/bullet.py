import pygame as pg
from pygame.sprite import Sprite
import math


class Bullet(Sprite):
    """父类"""

    def __init__(self, sett, screen, shooter, speed, lethality, byhero, _type,lr=0):

        super().__init__()

        self.sett = sett

        self.screen = screen

        self.screen_rect = screen.get_rect()

        self.shooter = shooter  # 发射子弹的对象

        self.speed = speed

        self.lethality = lethality

        self.byhero = byhero  # 标记该子弹是不是hero发射的(True or False)

        # 导入子弹图像

        if _type == 0:
            if self.byhero: 
                graph = '../image/bullets/bullet00.png'
            else:
                graph='../image/bullets/bullet01.png'

        elif _type == 1:
            if self.byhero:
                graph='../image/bullets/bullet1'+str(lr)+'0.png'
            else:
                graph='../image/bullets/bullet1'+str(lr)+'1.png'

        if _type==0 or _type==1:
            self.image = pg.image.load(graph)
        else:
            self.images=[]
            self.image=pg.image.load('../image/bullets/bullet20'+('0'if self.byhero else '1')+'.png')
            self.images.append(self.image)
            self.image=pg.image.load('../image/bullets/bullet21'+('0'if self.byhero else '1')+'.png')
            self.images.append(self.image)

        self.rect = self.image.get_rect()

        # 根据shooter（同样有属性rect）位置初始化子弹位置
        self.rect.centerx = shooter.rect.centerx
        self.rect.centery = shooter.rect.centery

        # 用self.x, self.y存储用小数表示的子弹位置

        self.x = float(self.rect.centerx)

        self.y = float(self.rect.centery)


class Bullet0(Bullet):
    """普通子弹,直线飞行"""

    def __init__(self, sett, screen, shooter, dir, byhero, is_skill=False):

        """在发射点所处的位置创建一个子弹对象"""
        
        lethality=sett.lethality[3] if is_skill else sett.lethality[0]

        super().__init__(sett, screen, shooter, sett.bullet0_speed, lethality, byhero, 0)

        self.dir = dir  # 子弹方向

    def update(self, bullets, t_interval):

        # 更新子弹位置
        move_distance = t_interval*self.speed
        self.x += move_distance * math.cos(self.dir)
        self.y -= move_distance * math.sin(self.dir)
        if self.y < 0 or self.y > self.sett.screen_height or self.x<0 or self.x>self.sett.screen_width:
            if self.byhero:
                bullets[0].remove(self)
            else:
                bullets[3].remove(self)
            return
        self.rect.centerx = self.x
        self.rect.centery = self.y


class Bullet1(Bullet):
    """多核弹，直线飞到一定距离后分裂"""

    def __init__(self, sett, screen, shooter, dir, byhero):

        """在发射点所处的位置创建一个子弹对象"""

        if dir>-math.pi/2 and dir<math.pi/2:
            lr=1   #上下左右
        elif dir==-math.pi/2:
            lr=2
        elif dir==math.pi/2:
            lr=3
        else:
            lr=0
        super().__init__(sett, screen, shooter, sett.bullet1_speed, sett.lethality[1], byhero, 1,lr)

        self.sett = sett

        self.dir = dir

        # 更新次数
        self.dist_pass = 0

    def update(self, bullets, t_interval):

        # 更新子弹位置，分裂后生成几个Bullet0,

        # byhero==True,将bullet0存进bullets[0],在bullet[1]中删除该bullet1

        # byhero==False，将bullet0存进bullets[3],在bullet[4]中删除该bullet1
        move_distance=t_interval*self.speed
        self.x += move_distance * math.cos(self.dir)
        self.y -= move_distance * math.sin(self.dir)
        if self.y < 0 or self.y > self.sett.screen_height or self.x<0 or self.x>self.sett.screen_width:
            if self.byhero:
                bullets[1].remove(self)
            else:
                bullets[4].remove(self)
            return
        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.dist_pass += move_distance

        #400: 走过的距离
        if (self.dist_pass >= 250):
            # 五个方向
            new_bullet0 = Bullet0(self.sett, self.screen, self, -self.sett.degree_disper*2 + self.dir, self.byhero)
            new_bullet1 = Bullet0(self.sett, self.screen, self, -self.sett.degree_disper + self.dir, self.byhero)
            new_bullet2 = Bullet0(self.sett, self.screen, self, self.dir, self.byhero)
            new_bullet3 = Bullet0(self.sett, self.screen, self, self.sett.degree_disper + self.dir, self.byhero)
            new_bullet4 = Bullet0(self.sett, self.screen, self, self.sett.degree_disper*2 + self.dir, self.byhero)
     
            if self.byhero == True:
                bullets[0].add(new_bullet0)
                bullets[0].add(new_bullet1)
                bullets[0].add(new_bullet2)
                bullets[0].add(new_bullet3)
                bullets[0].add(new_bullet4)

                # bullets[1]删除这个子弹
                bullets[1].remove(self)
            else:
                bullets[3].add(new_bullet0)
                bullets[3].add(new_bullet1)
                bullets[3].add(new_bullet2)
                bullets[3].add(new_bullet3)
                bullets[3].add(new_bullet4)

                # bullets[4]删除这个子弹
                bullets[4].remove(self)


class Bullet2(Bullet):
    """导弹，能一直追踪hero，能被子弹击落"""

    def __init__(self, sett, screen, shooter, target, byhero,enemies=[], bullets=[]):

        super().__init__(sett, screen, shooter, sett.bullet2_speed, sett.lethality[2], byhero, 2)

        self.life = sett.bullet2_life  # 导弹生命值

        self.lr=1 #向左0，向右1

        if byhero==True:
            radar=Radar(self.rect)
            self.target=radar.detect(enemies,bullets)
        else:
            self.target=target


    def update(self, bullets, t_interval, enemies=[]):
        """每次更新位置都朝着target_pos方向即可"""
        
        if self.byhero:
            #判断目标是否还存活，如果不存活，再选一个目标
            if self.target not in enemies and self.target not in bullets[5]:
                radar=Radar(self.rect)
                self.target=radar.detect(enemies,bullets)

        # 目标位置        
        target_pos = (self.target.rect.centerx, self.target.rect.centery)

        # 自身位置
        self_pos = (self.rect.centerx, self.rect.centery)

        if self_pos[0]<target_pos[0]:
            if self.lr==0:
                self.lr=1
                self.image=self.images[1]
        elif self_pos[0]>target_pos[0]:
            if self.lr==1:
                self.lr=0
                self.image=self.images[0]

        # 目标与自身距离
        distance = ((target_pos[0] - self_pos[0]) ** 2 + (self_pos[1] - target_pos[1]) ** 2) ** 0.5
        
        move_distance = t_interval * self.speed
        
        # 比例，大家都懂
        if distance != 0:
            self.x += (target_pos[0] - self_pos[0]) * move_distance / distance
            self.y += (target_pos[1] - self_pos[1]) * move_distance / distance
        if self.y < 0 or self.y > self.sett.screen_height or self.x<0 or self.x>self.sett.screen_width:
            if self.byhero: 
                bullets[2].remove(self)
            else:
                bullets[5].remove(self)
            return

        self.rect.centerx = self.x
        self.rect.centery = self.y

class Radar(Sprite):
    '''
    雷达，检测距离最近的敌机或导弹
    '''
    def __init__(self,init_rect):
        super().__init__()   
        self.rect=pg.Rect(init_rect)
        self.centerx, self.centery=self.rect.centerx, self.rect.centery

    def detect(self,enemies,bullets):
        for i in range(6):
            #扩大探测范围
            self.rect.width+=200
            self.rect.height+=200
            self.rect.centerx, self.rect.centery=self.centerx, self.centery
     
            #检测探测范围内是否有敌机
            enemies_detected=pg.sprite.spritecollide(self, enemies,False)
            if enemies_detected:
                self.rect.size=(0,0)
                return enemies_detected[0]

            else:
                #如果探测范围内没用敌机，则检测是否有导弹
                bullet2s_detected=pg.sprite.spritecollide(self, bullets[5],False)
                if bullet2s_detected:
                    self.rect.size=(0,0)
                    return bullet2s_detected[0]

        #探测最大范围内没有敌机或导弹，返回一个默认target
        default_tar=DefaultObj()
        return default_tar

class DefaultObj():
    def __init__(self):
        self.rect=pg.Rect(1200,300,2,2)
