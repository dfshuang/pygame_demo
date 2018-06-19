import pygame

class GameStats():
    """跟踪显示游戏的统计信息"""

    def __init__(self, g_settings):
        """初始化统计信息"""
        self.g_settings = g_settings
        self.game_active = False
        self.game_pause = False
        self.time_=0
        self.night=False #是否为黑夜模式
        self.reset_stats()
        self.high_score = 0


    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.hero_left = self.g_settings.hero_limit  #命的条数
        self.score = 0 #记录游戏得分
        self.level = 1 #记录游戏等级