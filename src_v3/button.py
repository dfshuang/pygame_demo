import pygame
import settings
import sys
class Button():

    def __init__(self, screen, msg, pos=(settings.screen_width/2, settings.screen_height/2), text_color=(255, 255, 255),
                 button_color=(0, 255, 0), width=200, height=50, font_size=48):
        """
        初始化按钮属性
        :param msg 为要按钮中的文字
        :param pos  按钮位置，二元组
        """
        #设置按钮的尺寸和其它属性
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)
        self.msg = msg

        #创建按钮的rect对象，并设置其位置为pos
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = pos

        #按钮的标签只需创建一次
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
        self.startMenu = []

        #下面设置开始菜单选项，为便于调试，start表示第一个button纵坐标，interval两个button之间相隔的距离
        start = 200
        interval = 60
        self.add_button(screen=screen, msg="start", pos=(500, start))
        self.add_button(screen=screen, msg="record", pos=(500, start+interval))
        self.add_button(screen=screen, msg="setting", pos=(500, start+interval*2))
        self.add_button(screen=screen, msg="help", pos=(500, start+interval*3))
        self.add_button(screen=screen, msg="exit", pos=(500, start + interval * 4))
        self.add_button(screen=screen, msg="pause", pos=(500, 300))
        self.add_button(screen=screen, msg="quiet", pos=(700, 360))
        self.add_button(screen=screen, msg="back", pos=(800, 500))
        self.add_button(screen=screen, msg="music", pos=(700, 300))


    def add_button(self, screen, msg, pos):
        """添加msg信息的button"""
        self.startMenu.append(Button(screen, msg, pos=pos))

    def draw(self, stats):
        """在屏幕上显示控件"""
        if stats.isStartMenu is True:
            for i in range(5):
                self.startMenu[i].draw()
        elif stats.game_pause is True:
            self.startMenu[5].draw()
            self.startMenu[7].draw()
        elif stats.isSetting is True:
            self.startMenu[6].draw()
            self.startMenu[7].draw()
            self.startMenu[8].draw()
        elif stats.isRecord or stats.isHelp:
            self.startMenu[7].draw()


    def collide_mouse(self, mouse_x, mouse_y, stats):
        """开始菜单中有控件被点击，被点击则改状态"""
        #先检测是否碰撞
        for button in self.startMenu:
            if button.rect.collidepoint(mouse_x, mouse_y):
                if button.msg == "start":
                    if stats.isStartMenu:
                        stats.start_game = True
                        stats.isStartMenu = False
                elif button.msg == "record":
                    if stats.isStartMenu:
                        stats.isRecord = True
                        stats.isStartMenu = False
                elif button.msg == "setting":
                    if stats.isStartMenu:
                        stats.isSetting = True
                        stats.isStartMenu = False
                elif button.msg == "help":
                    if stats.isStartMenu:
                        stats.isHelp = True
                        stats.isStartMenu = False
                elif button.msg == "pause":
                    if stats.game_active:
                        stats.game_pause = not stats.game_pause
                elif button.msg == "back":
                    if stats.isRecord or stats.isHelp or stats.isSetting or stats.game_pause:
                        stats.isStartMenu = True
                        stats.isRecord = False
                        stats.isHelp = False
                        stats.isSetting = False
                        stats.game_pause = False
                        stats.game_active = False
                elif button.msg == "music":
                    if stats.isSetting:
                        stats.isQuiet = False
                elif button.msg == "quiet":
                    if stats.isSetting:
                        stats.isQuiet = True
                elif button.msg == "exit":
                    if stats.isStartMenu:
                        with open("record.txt", 'a+') as fw:
                            fw.write(str(stats.high_score) + '\n')
                        sys.exit()