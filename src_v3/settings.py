import pygame as pg
import math


class Settings():
    """存储游戏中的所有设置,比如屏幕属性，速度，生命值"""

    def __init__(self):
        
        # 屏幕设置
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (0, 255, 255)


        # 子弹设置
        self.dir_factor = math.pi / 4  # 方向改变单位(即每按一下改变多少度数)
        self.degree_disper = math.pi/5 #散弹的分散程度
        self.bullet2_life = 3
        
        self.bullet0_speed = 150
        self.bullet1_speed = 150
        self.bullet2_speed = 100

        self.lethality = [1, 3, 2, 3]  # 子弹杀伤力

       
        #enemy设置
        self.separates=(5,8) #调整enemies的数量比例
        
        self.ordinPlaneLife = 6
        self.multiPlaneLife = 6
        self.missilePlaneLife = 6
        
        self.ordinPlaneSpeed = 120
        self.multiPlaneSpeed = 100
        self.missilePlaneSpeed = 100
        
        self.fire_T= [7,20,50] #发射子弹周期

        self.ordinPlaneTimeLimit = 60
        self.multiPlaneTimeLimit = 45
        self.missilePlaneTimeLimit = 30


        # hero设置
        self.hero_limit = 2
        self.hero_life = 50 #hero每条命的血量
        self.hero_speed = 400
        self.jump_init_speed = -1300  # 向上为负方向


        # other settings
        self.acc = 2700  # 重力加速度
        self.groundy = self.screen_height  # 地面的y坐标
        self.enemy_points = 100 #积分
    

       
