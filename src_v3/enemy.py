import pygame
from pygame.sprite import Sprite
import random
import bullet
import math

class Enemy(Sprite):
    def __init__(self, settings, screen, life, speed, time_limit, typex):
        """
        :param settings:
        :param screen:
        :param life: 生命值，由子类而得
        :param speed: 速度
        :param time_limit: 存在时限
        :param type: 敌机种类，决定子弹和图片类型
        """
        super(Enemy, self).__init__()
        self.settings = settings
        self.typex = typex
        
        #存储敌机图片（向左向右）
        self.images=[0,0]
        if self.typex==0:
            for i in range (2):
                self.images[i]=pygame.image.load('../image/enemies/ordinplane'+str(i)+'.png')     
        elif self.typex==1:
            for i in range (2):
                self.images[i]=pygame.image.load('../image/enemies/multiplane'+str(i)+'.png')    
        elif self.typex==2:
            for i in range (2):
                self.images[i]=pygame.image.load('../image/enemies/missileplane'+str(i)+'.png')         
        for i in range(2): 
            self.images[i]=pygame.transform.scale(self.images[i],(80,45))       
        
        self.image=self.images[0]    

        self.screen = screen
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #设置初始位置
        self.rect.left = self.screen_rect.right
        self.rect.centery = random.randint(20, self.screen_rect.height-210)

        # 存储小数形式的位置
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.life = life  # 生命值
        self.speed = speed
        self.time_limit = time_limit  # hero可以驾驶的时限
        self.jackedTime = None  # 被劫机的时间

        self.fire_T=self.settings.fire_T[self.bullet_type]
        
        self.moving_udlr = [False, False, False, False]
        self.inity=self.y #self.y的初始值
        self.face_right=False #向左向右

    def update(self, bullets, target_hero, t_interval):
        """移动或发射子弹"""
        #移动, 修改x, y后写入rect中
        t_change = t_interval * self.speed
        self.t+=t_change
        #移动
        if self.typex==0:    
            self.track(200,200)  
        elif self.typex==1:
            self.track(300,100)
        elif self.typex==2:
<<<<<<< HEAD
            self.track(150,200)
=======
            self.track(100,200)
>>>>>>> 384da0097d8ae9040c39a62fa19ee5f5619ac425

        #随机发射子弹，1/fire_T概率发射
        randnum = random.randint(1, self.fire_T)
        if randnum == 3:
            self.fire_bullet(bullets, self.screen, target_hero)
        

    def fire_bullet(self, bullets, screen, target_hero):
        """
        发射子弹，根据传入的子弹类型发射对应子弹
        """
        direction = random.randint(0, 7) - 3
        if self.typex == 0:
            bulletx = bullet.Bullet0(self.settings, screen, self, math.pi * direction/4, False)
            bullets[3].add(bulletx)
        elif self.typex == 1:
            bulletx = bullet.Bullet1(self.settings, screen, self, math.pi * direction/4, False)
            bullets[4].add(bulletx)
        elif self.typex == 2:
            bulletx = bullet.Bullet2(self.settings, screen, self, target_hero, False)
            bullets[5].add(bulletx)

    def track(self,Rx,Ry):
        '''移动在轨迹上，Rx为x轴方向的半径，Ry为y方向半径'''
        ctx=1250-self.t_turn+self.init_t-Rx
        tmpx=self.x
        if self.t<self.t_turn:
            self.x=1250-self.t+self.init_t
        else:
            self.x=ctx+Rx*math.cos(0.01*self.t-0.01*self.t_turn)
            self.y=self.inity+Ry*math.sin(0.01*self.t-0.01*self.t_turn)
        self.rect.centerx, self.rect.centery=self.x, self.y

        #改变image
        if tmpx<self.x and not self.face_right:
            self.face_right=True
            self.image=self.images[1]
        elif tmpx>self.x and self.face_right:
            self.face_right=False
            self.image=self.images[0]


class Ordin_plane(Enemy):
    """使用bullet0"""
    def __init__(self, settings, screen):
        self.life = settings.ordinPlaneLife  # 生命值
        self.speed = settings.ordinPlaneSpeed
        self.time_limit = settings.ordinPlaneTimeLimit  # hero可以驾驶的时限
        self.bullet_type = 0
<<<<<<< HEAD
        self.t_turn=900
        self.t = float(random.randint(0,self.t_turn-100)) #控制其位置的自变量：self.y=a(t),self.x=b(t)
=======
        self.t_turn=950
        self.t = float(random.randint(0,self.t_turn)) #控制其位置的自变量：self.y=a(t),self.x=b(t)
>>>>>>> 384da0097d8ae9040c39a62fa19ee5f5619ac425
        self.init_t=self.t
        Enemy.__init__(self, settings, screen, self.life, self.speed, self.time_limit, self.bullet_type)


class Multi_plane(Enemy):
    """使用bullet1"""
    def __init__(self, settings, screen):
        self.life = settings.multiPlaneLife  # 生命值
        self.speed = settings.multiPlaneSpeed
        self.time_limit = settings.multiPlaneTimeLimit  # hero可以驾驶的时限
        self.bullet_type = 1
        self.t_turn=750
<<<<<<< HEAD
        self.t = float(random.randint(0,self.t_turn-100)) #控制其位置的自变量：self.y=a(t),self.x=b(t)
=======
        self.t = float(random.randint(0,self.t_turn)) #控制其位置的自变量：self.y=a(t),self.x=b(t)
>>>>>>> 384da0097d8ae9040c39a62fa19ee5f5619ac425
        self.init_t=self.t
        Enemy.__init__(self, settings, screen, self.life, self.speed, self.time_limit, self.bullet_type)


class Missile_plane(Enemy):
    """使用bullet2"""
    def __init__(self, settings, screen):
        self.life = settings.missilePlaneLife  # 生命值
        self.speed = settings.missilePlaneSpeed
        self.time_limit = settings.missilePlaneTimeLimit  # hero可以驾驶的时限
        self.bullet_type = 2
<<<<<<< HEAD
        self.t_turn=900
        self.t = float(random.randint(0,self.t_turn-200)) #控制其位置的自变量：self.y=a(t),self.x=b(t)
=======
        self.t_turn=1050
        self.t = float(random.randint(0,self.t_turn)) #控制其位置的自变量：self.y=a(t),self.x=b(t)
>>>>>>> 384da0097d8ae9040c39a62fa19ee5f5619ac425
        self.init_t=self.t
        Enemy.__init__(self, settings, screen, self.life, self.speed, self.time_limit, self.bullet_type)  
