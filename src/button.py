import pygame
import settings
import sys


class Button():

    def __init__(self, screen, msg, pos=(settings.screen_width / 2, settings.screen_height / 2),
                 text_color=(255, 255, 255),
                 button_color=(0, 255, 0), width=200, height=50, font_size=48):
        """
        初始化按钮属性
        :param msg 为要按钮中的文字
        :param pos  按钮位置，二元组
        """
        # 设置按钮的尺寸和其它属性
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)
        self.msg = msg

        # 创建按钮的rect对象，并设置其位置为pos
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = pos

        # 按钮的标签只需创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮中居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Menu():
    def __init__(self, screen):
        """初始化初始菜单"""
        # 初始化开始菜单为一个空列表
        self.startMenu = {}

        # 下面设置开始菜单选项，为便于调试，start表示第一个button纵坐标，interval两个button之间相隔的距离
        start = 200
        interval = 60
        self.add_button(screen=screen, msg="start", pos=(500, start))
        self.add_button(screen=screen, msg="record", pos=(500, start + interval))
        self.add_button(screen=screen, msg="setting", pos=(500, start + interval * 2))
        self.add_button(screen=screen, msg="help", pos=(500, start + interval * 3))
        self.add_button(screen=screen, msg="exit", pos=(500, start + interval * 4))
        self.add_button(screen=screen, msg="pause", pos=(500, 300))
        self.add_button(screen=screen, msg="back", pos=(800, 500), button_color=(0, 200, 200), width=150)
        self.add_button(screen=screen, msg="music", pos=(550, 300))
        self.add_button(screen=screen, msg="quiet", pos=(550, 300))
        self.add_button(screen=screen, msg='background', pos=(550, 400))
        self.add_button(screen=screen, msg="bluesky", pos=(770, 370))
        self.add_button(screen=screen, msg="dusk", pos=(770, 430))
        self.add_button(screen=screen, msg='continue', pos=(800, 440), button_color=(0, 200, 200), width=150)

    def add_button(self, screen, msg, pos=(500, 300), button_color=(0, 255, 0), width=200, height=50):
        """添加msg信息的button"""
        button = Button(screen, msg, pos=pos, button_color=button_color, width=width, height=height)
        self.startMenu[button.msg] = button

    def draw(self, stats):
        """在屏幕上显示控件"""
        if stats.game_windows['start_menu']:
            if stats.game_windows['continue']:
                self.startMenu['back'].draw()
                self.startMenu['continue'].draw()
                self.startMenu['record'].draw()
                self.startMenu['setting'].draw()
                self.startMenu['help'].draw()
                self.startMenu['exit'].draw()
            elif not stats.game_windows['continue']:
                self.startMenu['start'].draw()
                self.startMenu['record'].draw()
                self.startMenu['setting'].draw()
                self.startMenu['help'].draw()
                self.startMenu['exit'].draw()
        elif stats.game_windows['game_pause']:
            self.startMenu['pause'].draw()
            self.startMenu['back'].draw()
        elif stats.game_windows['setting']:
            if stats.game_windows['quiet']:
                self.startMenu['music'].draw()
            elif not stats.game_windows['quiet']:
                self.startMenu['quiet'].draw()
            if stats.game_windows['setting_bg']:
                self.startMenu['bluesky'].draw()
                self.startMenu['dusk'].draw()
            self.startMenu['background'].draw()
            self.startMenu['back'].draw()
        elif stats.game_windows['game_over']:
            self.startMenu['back'].draw()
        elif stats.game_windows['record'] or stats.game_windows['help']:
            self.startMenu['back'].draw()
        elif stats.game_windows['good_job']:
            self.startMenu['back'].draw()
            self.startMenu['continue'].draw()

    def collide_mouse(self, mouse_x, mouse_y, stats):
        """开始菜单中有控件被点击，被点击则改状态"""
        # 先检测是否碰撞
        for button in self.startMenu.values():
            if button.rect.collidepoint(mouse_x, mouse_y):
                if stats.game_windows['start_menu']:
                    if stats.game_windows['continue']:
                        if button.msg == 'continue':
                            stats.game_windows['start_menu'] = False
                            stats.game_windows['continue'] = False
                            stats.game_windows['game_over'] = False
                            stats.game_windows['game_pause'] = False
                        elif button.msg == 'record':
                            stats.game_windows['start_menu'] = False
                            stats.game_windows['record'] = True
                        elif button.msg == 'setting':
                            stats.game_windows['start_menu'] = False
                            stats.game_windows['setting'] = True
                        elif button.msg == "help":
                            stats.game_windows['start_menu'] = False
                            stats.game_windows['help'] = True
                        elif button.msg == "exit":
                            with open("record.txt", 'a+') as fw:
                                fw.write(str(stats.high_score) + '\n')
                            sys.exit()
                    elif not stats.game_windows['continue']:
                        if button.msg == 'start':
                            stats.game_windows['start_game'] = True
                            stats.game_windows['start_menu'] = False
                            stats.game_windows['game_over'] = False
                            stats.game_windows['boss_appear'] = False
                            stats.game_windows['game_pause'] = False
                        elif button.msg == 'record':
                            stats.game_windows['start_menu'] = False
                            stats.game_windows['record'] = True
                        elif button.msg == 'setting':
                            stats.game_windows['start_menu'] = False
                            stats.game_windows['setting'] = True
                        elif button.msg == "help":
                            stats.game_windows['start_menu'] = False
                            stats.game_windows['help'] = True
                        elif button.msg == "exit":
                            with open("record.txt", 'a+') as fw:
                                fw.write(str(stats.high_score) + '\n')
                            sys.exit()
                elif stats.game_windows['game_pause']:
                    if button.msg == 'back':
                        stats.game_windows['start_menu'] = True
                        stats.game_windows['continue'] = True
                        stats.game_windows['game_pause'] = False
                    elif button.msg == 'pause':
                        stats.game_windows['game_pause'] = False
                elif stats.game_windows['setting']:
                    if button.msg == 'back':
                        stats.game_windows['setting'] = False
                        stats.game_windows['start_menu'] = True
                    elif button.msg == 'music':
                        stats.game_windows['quiet'] = not stats.game_windows['quiet']

                        # 设置是否播放音乐
                        if stats.game_windows['quiet']:
                            pygame.mixer.music.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(1)
                    elif button.msg == 'background':
                        stats.game_windows['setting_bg'] = not stats.game_windows['setting_bg']
                    elif button.msg == 'bluesky' and stats.game_windows['setting_bg']:
                        stats.game_windows['scene'] = 'bluesky'
                    elif button.msg == 'dusk' and stats.game_windows['setting_bg']:
                        stats.game_windows['scene'] = 'dusk'

                elif stats.game_windows['game_over']:
                    if button.msg == 'back':
                        stats.game_windows['start_menu'] = True
                        stats.game_windows['setting'] = False
                        stats.game_windows['record'] = False
                        stats.game_windows['help'] = False
                        stats.game_windows['game_over'] = False
                        stats.game_windows['game_active'] = False
                elif stats.game_windows['record'] or stats.game_windows['help']:
                    if button.msg == 'back':
                        stats.game_windows['start_menu'] = True
                        stats.game_windows['record'] = False
                        stats.game_windows['help'] = False
                elif stats.game_windows['good_job']:
                    if button.msg == 'continue':
                        stats.game_windows['good_job'] = False
                        stats.game_windows['start_menu'] = False
                        stats.game_windows['continue'] = False
                        stats.game_windows['game_over'] = False
                        stats.game_windows['game_pause'] = False
                        stats.game_windows['setting'] = False
                        stats.game_windows['record'] = False
                        stats.game_windows['help'] = False
                    elif button.msg == 'back':
                        stats.game_windows['good_job'] = False
                        stats.game_windows['start_menu'] = True
                        stats.game_windows['continue'] = True

