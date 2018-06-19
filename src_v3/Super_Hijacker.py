
import sys
import pygame as pg
from pygame.sprite import Group
from settings import Settings
import game_function as gf
from hero import Hero
from enemy import *
from bullet import *
from background import *
from button import *
from game_stats import GameStats
from scoreboard import Scoreboard

 
def run_game():
    pg.init()

    #bgm
    pg.mixer.init()
    pg.mixer.music.load('../sound/bgm.mp3')
    pg.mixer.music.play(-1)
    
    sett = Settings()
    screen = pg.display.set_mode((sett.screen_width, sett.screen_height))
    pg.display.set_caption("Super Hijacker")

    menu = Menu(screen)
    pause_button = Button(screen, 'Pause')
    stats = GameStats(sett)
    sb = Scoreboard(sett, screen, stats)

    #背景
    bg = Background(sett)
    sound = Sound()

    # 创建hero
    hero = Hero(screen, sett)

    # 创建存储敌机的编组
    enemies = Group()

    boss=Boss(sett,screen)
    #enemies.add(boss)
    #print(enemies)
    #存储爆炸
    bursts = Group()

    # 创建存储子弹的编组
    # bullets[0],bullets[1],bullets[2]分别为存储hero发射的普通子弹、多核弹、导弹的编组，
    # bullets[3],bullets[4],bullets[5]分别为存储enemies发射的普通子弹、多核弹、导弹的编组
    bullets = []
    for i in range(6):
        bullet = Group()
        bullets.append(bullet)

    t_interval = 0
    clock = pg.time.Clock()
    # 游戏主循环
    while True:
        t_interval = clock.tick()/1000  #距离上一帧的时间间隔(s)
        gf.night_or_day(t_interval, stats, sett)
        gf.handle_events(sett, screen, hero, enemies, boss, bullets, bursts, stats, sb, sound, menu)
        if stats.game_active is True and not stats.game_pause:
            bg.update()
            hero.update(bullets, bursts, t_interval, stats, sb, sett,screen, sound)
            gf.update_bullets(sett, bullets, hero, enemies, boss,bursts, screen, stats, t_interval, sb, sound)
            boss.update(bullets, hero, t_interval, sound)
            gf.update_enemies(enemies, hero, bullets, bursts, stats, t_interval, sb, sound)
            gf.update_bursts(bursts)
        gf.update_screen(sett, screen, bg, hero, enemies, boss, bullets, bursts, menu, stats, sb, sound)

run_game()
