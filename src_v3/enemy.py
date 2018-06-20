import pygame
from pygame.sprite import Sprite
import random
import bullet
import time
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
        if typex==3:
            self.image=pygame.image.load('../image/enemies/boss.png')
        else:
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
            elif self.typex==3:
                self.images[0]=pygame.image.load('../image/enemies/boss.png')

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
        if typex!=3:
            self.fire_T=self.settings.fire_T[self.bullet_type]
        
        self.moving_udlr = [False, False, False, False]
        self.inity=self.y #self.y的初始值
        self.face_right=False #向左向右

    def update(self, bullets, target_hero, t_interval,sound):
        """移动或发射子弹"""
        #移动, 修改x, y后写入rect中，bullet_type 为3时为boss
        if self.bullet_type!=3:
            t_change = t_interval * self.speed
            self.t+=t_change
            #移动
            if self.typex==0:    
                self.track(200,200)  
            elif self.typex==1:
                self.track(300,100)
            elif self.typex==2:
                self.track(150,200)

            #随机发射子弹，1/fire_T概率发射
            randnum = random.randint(1, self.fire_T)
            if randnum == 3:
                self.fire_bullet(bullets, self.screen, target_hero, sound, t_interval)

        #boss
        else:
            if not self.appeared:
                if time.clock() > self.appearTime:
                    self.appeared = True
            else:
                t_change = t_interval * self.speed
                self._t+=t_change
                if self._t>1000:
                    self._t=0
                self.track(200,150,t_change)
                if self._t>157:
                    if self.shooting==-1:
                        randnum=random.randint(1,120)
                        if randnum==10 or randnum==11:
                            self.shooting=0
                            self.clock0=pygame.time.Clock()
                        elif randnum==30 or randnum==31 or randnum==32:
                            self.shooting=1
                            self.clock0=pygame.time.Clock()
                        elif randnum==50:
                            self.shooting=2
                            self.clock0=pygame.time.Clock()
            
                self.fire_bullet(bullets, self.screen, self.shooting, target_hero)
            

    def fire_bullet(self, bullets, screen, target_hero,sound, t_interval):
        """
        发射子弹，根据传入的子弹类型发射对应子弹
        """
        #每t_interval发射一次，概率
        if random.randint(0, int(1/t_interval)) == 1:

            #方向随机，根据子弹类型发射相应的子弹
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
                sound.do_play['missile']=True

    def track(self,Rx,Ry,t_change=0):
        """移动在轨迹上，Rx为x轴方向的半径，Ry为y方向半径"""
        if self.bullet_type==3:
            if self._t<300:
                self.t+=t_change
                #print(self.t,'\n','\n')
        ctx=1250-self.t_turn+self.init_t-Rx
        tmpx=self.x
        if self.t<self.t_turn:
            self.x=1250-self.t+self.init_t
        else:
            self.x=ctx+Rx*math.cos(0.01*self.t-0.01*self.t_turn)
            self.y=self.inity+Ry*math.sin(0.01*self.t-0.01*self.t_turn)
        self.rect.centerx, self.rect.centery=self.x, self.y

        #改变image
        if self.bullet_type!=3:
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
        self.t_turn=900
        self.t = float(random.randint(0,self.t_turn-100)) #控制其位置的自变量：self.y=a(t),self.x=b(t)
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
        self.t = float(random.randint(0,self.t_turn-100)) #控制其位置的自变量：self.y=a(t),self.x=b(t)
        self.init_t=self.t
        Enemy.__init__(self, settings, screen, self.life, self.speed, self.time_limit, self.bullet_type)


class Missile_plane(Enemy):
    """使用bullet2"""
    def __init__(self, settings, screen):
        self.life = settings.missilePlaneLife  # 生命值
        self.speed = settings.missilePlaneSpeed
        self.time_limit = settings.missilePlaneTimeLimit  # hero可以驾驶的时限
        self.bullet_type = 2
        self.t_turn=900
        self.t = float(random.randint(0,self.t_turn-200)) #控制其位置的自变量：self.y=a(t),self.x=b(t)
        self.init_t=self.t
        Enemy.__init__(self, settings, screen, self.life, self.speed, self.time_limit, self.bullet_type)  

class Boss(Enemy):
    def __init__(self,settings,screen):
        self.appeared=False
        self.appearTime=300
        self.life = settings.bossLife  # 生命值
        self.speed = settings.bossSpeed
        self.bullet_type = 3
        
        Enemy.__init__(self, settings, screen, self.life, self.speed, 0, self.bullet_type) 
        #self.rect_draw=pygame.Rect(self.rect)
        #self.rect.width=89
        #self.rect.centerx+=57
        self.rect.centery=0.5 * settings.screen_height
        self.y=float(self.rect.centery)
        self.inity = self.y

        self.t_turn=500
        self._t=0 #控制其位置的自变量：self.y=a(t),self.x=b(t)
        self.t = 0 
        self.init_t=self._t


        self.time0=0.0
        self.clock0=0
        self.shoot_dir0=0
        self.shooting=-1


    def fire_bullet(self,bullets,screen,typex,target_hero=0):
        if typex==0:
            tmp=self.shoot_dir0
            self.shoot_dir0=(self.time0//200)*(math.pi*3/4)
            if self.shoot_dir0>tmp:
                if self.shoot_dir0>4*math.pi:
                    self.shooting=-1
                    self.time0=0.0
                    self.shoot_dir0=0.0
                    return    
                for i in range(10):
                    bulletx=bullet.Bullet0(self.settings, screen, self, self.shoot_dir0+i*(math.pi/20),False,1)
                    bullets[3].add(bulletx)
            self.time0+=self.clock0.tick()

        elif typex==1:
            tmp=self.shoot_dir0
            self.shoot_dir0=50*math.sin(0.2*self.time0//50)
            if self.shoot_dir0!=tmp:
                if self.time0>2400:
                    self.shooting=-1
                    self.time0=0.0
                    self.shoot_dir0=0.0
                    return    
                for i in range(4):
                    bulletx=bullet.Bullet1(self.settings, screen, self, i*(math.pi/2),False,self.shoot_dir0,True)
                    bullets[4].add(bulletx)
            self.time0+=self.clock0.tick()

        elif typex==2:
            tmp=self.shoot_dir0
            self.shoot_dir0=self.time0//400    
            if self.shoot_dir0!=tmp:
                if self.shoot_dir0>=5:
                    self.shooting=-1
                    self.time0=0.0
                    self.shoot_dir0=0.0
                    return
                bulletx=bullet.Bullet2(self.settings, screen, self, target_hero, False)
                bullets[5].add(bulletx)
            self.time0+=self.clock0.tick()
            
            





