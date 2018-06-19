import pygame

class GameStats():
    """跟踪显示游戏的统计信息"""

    def __init__(self, g_settings):
        """初始化统计信息"""
        self.g_settings = g_settings
        self.time_ = 0
        self.night = False #是否为黑夜模式
        self.reset_stats()  #游戏开始，重置信息
        self.high_score = 0

        #控制游戏处于哪个页面
        self.game_active = False
        self.game_pause = False
        self.isStartMenu = True
        self.isRecord = False
        self.isSetting = False
        self.isHelp = False

        #判断游戏是否准备开始
        self.start_game = False

        #游戏是否处于静音状态
        self.isQuiet = False

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.hero_left = self.g_settings.hero_limit  #命的条数
        self.score = 0 #记录游戏得分
        self.level = 1 #记录游戏等级
        self.heroLife = 0
        self.planeLife = 0
        self.planeTimeLimit = 0
