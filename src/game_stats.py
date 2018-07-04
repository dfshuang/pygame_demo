import pygame


class GameStats:
    """跟踪显示游戏的统计信息"""

    def __init__(self, g_settings):
        """初始化统计信息"""
        self.g_settings = g_settings
        self.time_ = 0
        self.night = False  # 是否为黑夜模式
        self.reset_stats()  # 游戏开始，重置信息
        self.high_score = 0

        # 控制游戏处于哪个页面及状态
        self.game_windows = {
            'game_active': False,  # 判断游戏是否在进行，状态
            'game_pause': False,
            'start_game': False,  # 判断游戏是否准备开始，过程
            'start_menu': True,
            'record': False,
            'setting': False,
            'setting_bg': False,
            'help': False,
            'quiet': False,  # 游戏是否静音
            'continue': False,  # boss死后继续游戏
            'game_over': False,
            'boss_appear': False,
            'good_job': False,
            'show_danger': False,  #boss出现前5秒显示danger
            'scene': 'bluesky'  #表示游戏的背景，有bluesky 和 dusk 两种
        }

        self.preMessage = {'hl': 0, 'sc': 0, 'le': 0, 'hlife': 0, 'plife': 0, 'ptime': 0,
                           'bosslife': self.g_settings.bossLife}
        self.hero_skill_cooling_time = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.hero_left = self.g_settings.hero_limit  # 命的条数
        self.score = 0  # 记录游戏得分
        self.level = 1  # 记录游戏等级
        self.heroLife = self.g_settings.hero_life
        self.planeLife = 0
        self.planeTimeLimit = 0
        self.bossLife = self.g_settings.bossLife
