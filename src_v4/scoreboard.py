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
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 30)

        #准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        #self.prep_planes()
        self.prep_herolife()
        self.prep_planeLife()
        self.prep_planeTimeLimit()
        self.prep_helpMessage()
        self.prep_boss_life()
        self.prep_gameover()
        self.prep_skill()
        self.prep_goodjob()

    def prep_boss_life(self):
        """显示boss血量"""
        boss_life_str = 'boss life: ' + '{:}'.format(int(self.stats.bossLife if self.stats.bossLife>0 else 0))
        self.boss_life_image = self.font.render(boss_life_str, True, self.text_color)
        # 将生命值放在屏幕左上角
        self.boss_life_rect = self.boss_life_image.get_rect()
        self.boss_life_rect.right = self.screen_rect.right - 20
        self.boss_life_rect.top = 70

    def prep_high_score(self):
        """将最高得分转化为渲染的图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = 'highest score: ' + '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        #将最高得分放在屏幕顶部中间
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top #留一点间隔

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = 'score: ' + '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level(self):
        self.level_image = self.font.render('level: ' + str(self.stats.level), True,
                                            self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    # def prep_planes(self):
    #     """显示余下多少艘飞船"""
    #     self.planes = Group()
    #     for plane_number in range(self.stats.hero_left):
    #         plane = Hero(self.screen, self.g_settings)
    #         plane.rect.x = 10 + plane_number * plane.rect.width
    #         plane.rect.y = 10
    #         self.planes.add(plane)

    def prep_herolife(self):
        """将主角生命值转换为一幅渲染的图像"""
        plane = Hero(self.screen, self.g_settings, self.stats)  #为获取plane图像高度
        hero_life_str = 'life: ' + '{:,}'.format(self.stats.heroLife)
        self.hero_life_image = self.font.render(hero_life_str, True, self.text_color)
        # 将生命值放在屏幕左上角
        self.hero_life_rect = self.hero_life_image.get_rect()
        self.hero_life_rect.left = 20
        self.hero_life_rect.top = plane.rect.height + 10

    def prep_planeLife(self):
        planeLife_str = 'planeLife: ' + '{:}'.format(self.stats.planeLife)
        self.planeLife_image = self.font.render(planeLife_str, True, self.text_color)
        # 将生命值放在屏幕左上角
        self.planeLife_rect = self.planeLife_image.get_rect()
        self.planeLife_rect.left = 20
        self.planeLife_rect.top = self.hero_life_rect.bottom + 7

    def prep_planeTimeLimit(self):
        planeTimeLimit_str = 'planeTimeLeft: ' + '{:3.2f}'.format(self.stats.planeTimeLimit)
        self.planeTimeLimit_image = self.font.render(planeTimeLimit_str, True, self.text_color)
        # 将生命值放在屏幕左上角
        self.planeTimeLimit_rect = self.planeTimeLimit_image.get_rect()
        self.planeTimeLimit_rect.left = 20
        self.planeTimeLimit_rect.top = self.planeLife_rect.bottom + 7

    def prep_helpMessage(self):
        fonttemp = pygame.font.SysFont(None, 30)
        helpMessage_str = ''
        self.helpMessage_image = fonttemp.render(helpMessage_str, True, self.text_color)

        # 将生命值放在屏幕左上角
        self.helpMessage_rect = self.helpMessage_image.get_rect()
        self.helpMessage_rect.centerx = self.screen_rect.centerx
        self.helpMessage_rect.top = 350

    def prep_record(self):
        """从文件中读取分数记录，显示前3"""
        with open("record.txt", "r") as fr:
            record = []
            for line in fr.readlines():
                record.append(int(round(float(line))))

            score_str = 'rank     score'
            score_image = self.font.render(score_str, True, self.text_color)
            # 将得分放在屏幕中间
            score_rect = score_image.get_rect()
            score_rect.left = 400
            score_rect.top = 150
            self.screen.blit(score_image, score_rect)

            record.sort(reverse=True)
            record_cnt = 1
            for r in record:
                score_str = '{:>4}'.format(record_cnt) + '         ' + '{:,}'.format(r)
                score_image = self.font.render(score_str, True, self.text_color)
                # 将得分放在屏幕中间
                score_rect = score_image.get_rect()
                score_rect.left = 400
                score_rect.top = 150 + record_cnt * 30
                self.screen.blit(score_image, score_rect)
                record_cnt += 1
                if record_cnt > 10:
                    break

    def prep_gameover(self):
        fonttemp = pygame.font.SysFont(None, 60)
        gameover_str = 'Game  Over !'
        self.gameover_image = fonttemp.render(gameover_str, True, (255,0,0))

        self.gameover_rect = self.gameover_image.get_rect()
        self.gameover_rect.centerx = self.screen_rect.centerx
        self.gameover_rect.centery = 300

    def prep_goodjob(self):
        fonttemp = pygame.font.SysFont(None, 60)
        goodjob_str = 'Good Job !!!'
        self.goodjob_image = fonttemp.render(goodjob_str, True, (0,255,0))

        self.goodjob_rect = self.goodjob_image.get_rect()
        self.goodjob_rect.centerx = self.screen_rect.centerx
        self.goodjob_rect.centery = 250

    def prep_skill(self):
        #加载技能图标
        hero_skill_image = pygame.image.load('../image/hero/skill_circle.png')
        # 将生命值放在屏幕左上角
        hero_skill_image_rect = hero_skill_image.get_rect()
        hero_skill_image_rect.left = 20
        hero_skill_image_rect.top = 10

        #渲染技能冷却时间
        skill_time_str = ' : ' + '{:3.2f}'.format(self.stats.hero_skill_cooling_time/1000)
        skill_time_image = self.font.render(skill_time_str, True, self.text_color)
        # 将生命值放在屏幕左上角
        skill_time_rect = skill_time_image.get_rect()
        skill_time_rect.left = 70
        skill_time_rect.top = 25

        self.screen.blit(hero_skill_image, hero_skill_image_rect)
        self.screen.blit(skill_time_image, skill_time_rect)

    def show_message(self):
        """在屏幕上显示得分"""
        #更新屏幕消息
        if self.stats.preMessage['sc'] != self.stats.score:
            self.prep_score()
            self.stats.preMessage['sc'] = self.stats.score
        if self.stats.preMessage['hc'] != self.stats.high_score:
            self.prep_high_score()
            self.stats.preMessage['hc'] = self.stats.high_score
        if self.stats.preMessage['le'] != self.stats.level:
            self.prep_level()
            self.stats.preMessage['le'] = self.stats.level
        # if self.stats.preMessage['hl'] != self.stats.hero_left:
        #     self.prep_planes()
        #     self.stats.preMessage['hl'] = self.stats.hero_left
        if self.stats.preMessage['hlife'] != self.stats.heroLife:
            self.prep_herolife()
            self.stats.preMessage['hlife'] = self.stats.heroLife
        if self.stats.preMessage['plife'] != self.stats.planeLife:
            self.prep_planeLife()
            self.stats.preMessage['plife'] = self.stats.planeLife
        if self.stats.preMessage['ptime'] != self.stats.planeTimeLimit:
            self.prep_planeTimeLimit()
            self.stats.preMessage['ptime'] = self.stats.planeTimeLimit
        if self.stats.game_windows['boss_appear'] and self.stats.preMessage['bosslife'] != self.stats.bossLife:
            self.prep_boss_life()
            self.stats.preMessage['bosslife'] = self.stats.bossLife

        #绘制各种实时信息
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.hero_life_image, self.hero_life_rect)
        self.screen.blit(self.planeTimeLimit_image, self.planeTimeLimit_rect)
        self.screen.blit(self.planeLife_image, self.planeLife_rect)
        if self.stats.game_windows['boss_appear']:
            self.screen.blit(self.boss_life_image, self.boss_life_rect)
        if self.stats.game_windows['help']:
            self.screen.blit(self.helpMessage_image, self.helpMessage_rect)
        if self.stats.game_windows['record']:
            self.prep_record()
        if self.stats.game_windows['game_over']:
            self.screen.blit(self.gameover_image, self.gameover_rect)
        if self.stats.game_windows['continue'] and not self.stats.game_windows['game_pause']:
            self.screen.blit(self.goodjob_image, self.goodjob_rect)
        #绘制飞机多少条命
        #self.planes.draw(self.screen)

        self.prep_skill()

