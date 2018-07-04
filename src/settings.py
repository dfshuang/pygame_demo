import pygame as pg
import math

screen_width = 1000
screen_height = 600


class Settings:
    """存储游戏中的所有设置,比如屏幕属性，速度，生命值"""

    def __init__(self):
        # 屏幕设置
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_color = (0, 255, 255)
        self.bgmoveT = 30.0

        # 子弹设置
        self.dir_factor = math.pi / 4  # 方向改变单位(即每按一下改变多少度数)
        self.degree_disper = math.pi / 5  # 散弹的分散程度
        self.bullet2_life = 3

        self.bullet0_speed = 150
        self.bullet1_speed = 150
        self.bullet2_speed = 100

        self.lethality = [1, 3, 2, 3]  # 子弹杀伤力

        # enemy设置
        self.separates = (5, 8)  # 调整enemies的数量比例
        self.enemy_num = 3
        self.ordinPlaneLife = 6
        self.multiPlaneLife = 6
        self.missilePlaneLife = 6
        self.bossLife = 100

        self.ordinPlaneSpeed = 120
        self.multiPlaneSpeed = 100
        self.missilePlaneSpeed = 100
        self.bossSpeed = 80

        self.fire_T = [10, 20, 30, 120]  # 发射子弹间隔时间

        self.ordinPlaneTimeLimit = 60
        self.multiPlaneTimeLimit = 45
        self.missilePlaneTimeLimit = 30

        self.boss_appear_interval = 30 # boss出现间隔时间，秒

        # hero设置
        self.hero_limit = 0
        self.hero_life = 10  # hero每条命的血量
        self.hero_speed = 300
        self.jump_init_speed = -1100  # 向上为负方向
        self.hero_skill_cooling_time = 20000   #技能冷却时间

        # other settings
        self.acc = 2700  # 重力加速度
        self.groundy = self.screen_height  # 地面的y坐标
        self.enemy_points = 10  # 积分
        self.background = 0  # 背景选择
        self.night_interval = 5   #黑夜出现时间
