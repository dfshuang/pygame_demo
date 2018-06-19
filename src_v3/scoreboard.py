import pygame.font
from pygame.sprite import Group
from hero import Hero

class Scoreboard():
    """显示得分的类"""
    def __init__(self, g_settings, screen, stats):
        """初始化显示得分的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.g_settings = g_settings
        self.stats = stats

        #显示得分信息时使用的字体
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 30)

        #准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_planes()
        self.prep_herolife(g_settings.hero_life)
        self.prep_planeLife(0)
        self.prep_planeTimeLimit(0)    
        self.prep_helpMessage()

    def prep_high_score(self):
        """将最高得分转化为渲染的图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = 'highest score: ' + '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                            self.text_color, self.g_settings.bg_color)

        #将最高得分放在屏幕顶部中间
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top #留一点间隔

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = 'score: ' + '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.g_settings.bg_color)
        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level(self):
        self.level_image = self.font.render('level: ' + str(self.stats.level), True,
                                            self.text_color, self.g_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_planes(self):
        """显示余下多少艘飞船"""
        self.planes = Group()
        for plane_number in range(self.stats.hero_left):
            plane = Hero(self.screen, self.g_settings)
            plane.rect.x = 10 + plane_number * plane.rect.width
            plane.rect.y = 10
            self.planes.add(plane)

    def prep_herolife(self, hero_life):
        """将主角生命值转换为一幅渲染的图像"""
        plane = Hero(self.screen, self.g_settings)  #为获取plane图像高度
        hero_life_str = 'life: ' + '{:,}'.format(hero_life)
        self.hero_life_image = self.font.render(hero_life_str, True, self.text_color,
                                            self.g_settings.bg_color)
        # 将生命值放在屏幕左上角
        self.hero_life_rect = self.hero_life_image.get_rect()
        self.hero_life_rect.left = 20
        self.hero_life_rect.top = plane.rect.height + 10

    def prep_planeLife(self, planeLife):
        planeLife_str = 'planeLife: ' + '{:,}'.format(planeLife)
        self.planeLife_image = self.font.render(planeLife_str, True, self.text_color,
                                                     self.g_settings.bg_color)
        # 将生命值放在屏幕左上角
        self.planeLife_rect = self.planeLife_image.get_rect()
        self.planeLife_rect.left = 20
        self.planeLife_rect.top = self.hero_life_rect.bottom + 7

    def prep_planeTimeLimit(self, planeTimeLimit):
        planeTimeLimit_str = 'planeTimeLeft: ' + '{:,}'.format(int(planeTimeLimit))
        self.planeTimeLimit_image = self.font.render(planeTimeLimit_str, True, self.text_color,
                                                self.g_settings.bg_color)
        # 将生命值放在屏幕左上角
        self.planeTimeLimit_rect = self.planeTimeLimit_image.get_rect()
        self.planeTimeLimit_rect.left = 20
        self.planeTimeLimit_rect.top = self.planeLife_rect.bottom + 7

    def prep_helpMessage(self):
        fonttemp = pygame.font.SysFont(None, 30)
        helpMessage_str = 'q: exit, d,c: change shoot dir, space: fire bullet, g,b: leave plane'
        self.helpMessage_image = fonttemp.render(helpMessage_str, True, self.text_color,
                                                     self.g_settings.bg_color)
        # 将生命值放在屏幕左上角
        self.helpMessage_rect = self.helpMessage_image.get_rect()
        self.helpMessage_rect.centerx = self.screen_rect.centerx
        self.helpMessage_rect.top = 350

    def show_score(self):
        """在屏幕上显示得分"""
        #绘制各种实时信息
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.hero_life_image, self.hero_life_rect)
        self.screen.blit(self.planeTimeLimit_image, self.planeTimeLimit_rect)
        self.screen.blit(self.planeLife_image, self.planeLife_rect)
        if self.stats.game_pause:
            self.screen.blit(self.helpMessage_image, self.helpMessage_rect)
        #绘制飞机多少条命
        self.planes.draw(self.screen)


