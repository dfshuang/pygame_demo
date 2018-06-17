import sys
import pygame as pg
from bullet import *
import time
import enemy
from burst import *
import random
import math

def handle_events(sett, screen, hero, enemies, bullets,bursts, stats, sb):
    """
	处理键盘和鼠标事件
	"""

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        elif event.type == pg.KEYDOWN:
            handle_keydown(sett, screen, event, enemies, hero, bullets,bursts, stats, sb)

        elif event.type == pg.KEYUP:
            handle_keyup(event, hero)

        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            handle_mouse(mouse_x, mouse_y, hero, enemies)

def handle_keydown(sett, screen, event, enemies, hero, bullets,bursts, stats, sb):
    """
    q: 退出
    p: 暂停
    enter: start
    方向键上下左右: move,  down: climb
    d,c: change shoot direction
    space: fire_bullet
    g: 以跳跃方式离开飞机
    b: 以下落方式离开飞机
    """
    #退出游戏界面
    if event.key == pg.K_q:
        sys.exit()

    # 暂停游戏
    elif event.key == pg.K_p:
        stats.game_pause = not stats.game_pause

    # 开始游戏
    elif event.key == pg.K_RETURN:
        start_game(sett, screen, enemies, hero, bullets, stats, sb)

    # 没有开敌机
    elif not hero.plane:
        # 移动
        if event.key == pg.K_d:
            hero.moving_right = True
            hero.clock=pg.time.Clock()
            hero._t=0
            if not hero.face_right:
                hero.face_right = True
                degreepi = math.pi if hero.shoot_dir >= 0 else -math.pi
                hero.shoot_dir = degreepi - hero.shoot_dir
        elif event.key == pg.K_a:
            hero.moving_left = True
            hero.clock=pg.time.Clock()    
            hero._t=0
            if hero.face_right:
                hero.face_right = False
                degreepi = math.pi if hero.shoot_dir >= 0 else -math.pi
                hero.shoot_dir = degreepi - hero.shoot_dir
        elif event.key == pg.K_j:
            if not hero.jumporfall:
                hero.jumporfall = True
                hero.jumpfallspeed = hero.jump_init_speed
                #改变image和rect
                lr=1 if hero.face_right else 0
                hero.image=hero.images['jump'][lr]
                tmprect=hero.rect
                hero.rect=hero.image.get_rect()
                hero.rect.centerx, hero.rect.centery=tmprect.centerx, tmprect.centery
        
        
        # 瞄准，开火
        #向上调角度
        elif event.key == pg.K_i:
            if hero.face_right:
                if hero.shoot_dir < math.pi / 2:
                    hero.shoot_dir += sett.dir_factor

                    if not hero.moving_right and not hero.moving_left and not hero.jumporfall:
                        hero.image=hero.images['stand'][int(hero.shoot_dir//(math.pi/4)+2)]
                        tmprect=hero.rect                    
                        hero.rect=hero.image.get_rect()
                        hero.rect.centerx, hero.rect.centery=tmprect.centerx, tmprect.centery       
            else:
                if hero.shoot_dir > math.pi / 2 or hero.shoot_dir <= -math.pi / 2:
                    hero.shoot_dir -= sett.dir_factor
                    if hero.shoot_dir <= -math.pi:
                        hero.shoot_dir = math.pi
                    if not hero.moving_right and not hero.moving_left and not hero.jumporfall:
                        if hero.shoot_dir>0:
                            index=int(11-hero.shoot_dir//(math.pi/4))
                        else:
                            index=int(3-hero.shoot_dir//(math.pi/4))
                        hero.image=hero.images['stand'][index]
                        tmprect=hero.rect                    
                        hero.rect=hero.image.get_rect()
                        hero.rect.centerx, hero.rect.centery=tmprect.centerx, tmprect.centery

        #向下调角度
        elif event.key == pg.K_o:
            if hero.face_right:
                if hero.shoot_dir > -math.pi / 2:
                    hero.shoot_dir -= sett.dir_factor
                    if not hero.moving_right and not hero.moving_left and not hero.jumporfall:
                        hero.image=hero.images['stand'][int(hero.shoot_dir//(math.pi/4)+2)]
                        tmprect=hero.rect                    
                        hero.rect=hero.image.get_rect()
                        hero.rect.centerx, hero.rect.centery=tmprect.centerx, tmprect.centery  
            else:
                if hero.shoot_dir >= math.pi / 2 or hero.shoot_dir < -math.pi / 2:
                    hero.shoot_dir += sett.dir_factor
                    if hero.shoot_dir > math.pi:
                        hero.shoot_dir = -math.pi + sett.dir_factor
                    if not hero.moving_right and not hero.moving_left and not hero.jumporfall:
                        if hero.shoot_dir>0:
                            index=int(4-hero.shoot_dir//(math.pi/4)+7)
                        else:
                            index=int(-4-hero.shoot_dir//(math.pi/4)+7)
                        hero.image=hero.images['stand'][index]
                        tmprect=hero.rect                    
                        hero.rect=hero.image.get_rect()
                        hero.rect.centerx, hero.rect.centery=tmprect.centerx, tmprect.centery

        #开火
        elif event.key == pg.K_k:
            bullet0 = Bullet1(sett, screen, hero, hero.shoot_dir, True)
            bullets[1].add(bullet0)

        #技能
        elif event.key == pg.K_u:
            if hero.cool_finished:
                hero.cool_finished=False
                hero.skilling=True
                hero.skill_clock=pg.time.Clock()

    # 开敌机
    else:
        # 移动
        if event.key == pg.K_d:
            hero.plane.moving_udlr[3] = True           
            if not hero.face_right:
                hero.face_right = True
                hero.plane.image=hero.plane.images[1]
                degreepi = math.pi if hero.shoot_dir >= 0 else -math.pi
                hero.shoot_dir = degreepi - hero.shoot_dir
        elif event.key == pg.K_a:
            hero.plane.moving_udlr[2] = True       
            if hero.face_right:
                hero.face_right = False
                hero.plane.image=hero.plane.images[0]
                degreepi = math.pi if hero.shoot_dir >= 0 else -math.pi
                hero.shoot_dir = degreepi - hero.shoot_dir
        elif event.key == pg.K_w:
            hero.plane.moving_udlr[0] = True
        elif event.key == pg.K_s:
            hero.plane.moving_udlr[1] = True

        # 瞄准，开火
        elif event.key == pg.K_i:
            if hero.face_right:
                if hero.shoot_dir < math.pi / 2:
                    hero.shoot_dir += sett.dir_factor
            else:
                if hero.shoot_dir > math.pi / 2 or hero.shoot_dir <= -math.pi / 2:
                    hero.shoot_dir -= sett.dir_factor
                    if hero.shoot_dir <= -math.pi:
                        hero.shoot_dir = math.pi

        elif event.key == pg.K_o:
            if hero.face_right:
                if hero.shoot_dir > -math.pi / 2:
                    hero.shoot_dir -= sett.dir_factor
            else:
                if hero.shoot_dir >= math.pi / 2 or hero.shoot_dir < -math.pi / 2:
                    hero.shoot_dir += sett.dir_factor
                    if hero.shoot_dir > math.pi:
                        hero.shoot_dir = -math.pi + sett.dir_factor

        elif event.key == pg.K_k:
            # 开火,不同战机不同子弹
            if str(type(hero.plane)) == "<class 'enemy.Ordin_plane'>":
                #三连发                
                for i in range(3):
                    tmp=DefaultObj()
                    tmp.rect.centerx, tmp.rect.centery=hero.plane.rect.centerx-15*i, hero.plane.rect.centery
                    bullet0 = Bullet0(sett, screen, tmp, hero.shoot_dir, True)
                    bullets[0].add(bullet0)
                
            elif str(type(hero.plane)) == "<class 'enemy.Multi_plane'>":
                bullet1 = Bullet1(sett, screen, hero.plane, hero.shoot_dir, True)
                bullets[1].add(bullet1)
            elif str(type(hero.plane)) == "<class 'enemy.Missile_plane'>":
                bullet2 = Bullet2(sett, screen, hero.plane, 0, True, enemies, bullets)
                bullets[2].add(bullet2)

        elif event.key == pg.K_j:
            # 以跳跃方式离开敌机
            start_burst(True,hero,bursts)
            hero.plane = None
            hero.face_right = True
            hero.shoot_dir = 0
            hero.jumporfall = True
            hero.jumpfallspeed = hero.jump_init_speed
        elif event.key == pg.K_n:
            # 以下落方式离开敌机
            start_burst(True,hero,bursts)
            hero.plane = None
            hero.face_right = True
            hero.shoot_dir = 0
            hero.jumporfall = True
            hero.jumpfallspeed = 0
        elif event.key == pg.K_u:
            if hero.cool_finished:
                hero.cool_finished=False
                hero.skilling=True
                hero.skill_clock=pg.time.Clock()

def handle_keyup(event, hero):
    # 没有开敌机
    if not hero.plane:
        if event.key == pg.K_d:
            hero.moving_right = False
            if not (hero.shoot_dir>=-math.pi/2 and hero.shoot_dir<=math.pi/2):
                hero.shoot_dir=0
            hero.image=hero.images['stand'][int(hero.shoot_dir//(math.pi/4)+2)]
                    
        elif event.key == pg.K_a:
            hero.moving_left = False
            if hero.shoot_dir<0:
                if hero.shoot_dir>-math.pi/2 and hero.shoot_dir<math.pi/2:
                    hero.shoot_dir=-3*math.pi/4
                hero.image=hero.images['stand'][int(3-hero.shoot_dir//(math.pi/4))]
            else:
                if hero.shoot_dir>-math.pi/2 and hero.shoot_dir<math.pi/2:
                    hero.shoot_dir=math.pi
                hero.image=hero.images['stand'][int(11-hero.shoot_dir//(math.pi/4))]
        

    # 开敌机
    else:
        if event.key == pg.K_d:
            hero.plane.moving_udlr[3] = False
        elif event.key == pg.K_a:
            hero.plane.moving_udlr[2] = False
        elif event.key == pg.K_w:
            hero.plane.moving_udlr[0] = False
        elif event.key == pg.K_s:
            hero.plane.moving_udlr[1] = False

def handle_mouse(mouse_x, mouse_y, hero, enemies):
    if str(type(hero.plane)) == "<class '__main__.Missile_plane'>":
        # 如果鼠标点击某架敌机，则将其作为导弹target，并存入hero.missle_target
        pass

def start_game(sett, screen, enemys, hero, bullets, stats, sb):
    """开始游戏"""
    if not stats.game_active:
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 清空敌机列表和子弹列表
        enemys.empty()
        for bulletsx in bullets:
            bulletsx.empty()

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_planes()

def update_screen(sett, screen,bg, hero, enemies, bullets,bursts, play_button, pause_button, stats, sb):
    """
	更新屏幕
	"""
    #重绘屏幕背景颜色
    if stats.night:
        screen.fill(sett.bg_color)
    else:
        bg.drawme(screen)
    

    #重绘子弹
    for i in range(6):
        if bullets[i]:
            bullets[i].draw(screen)

    if not stats.night:
        #重绘敌机
        if enemies:
            enemies.draw(screen)

    #重绘主角
    hero.drawme()

    #重绘爆炸   
    bursts.draw(screen)

    #重绘积分牌
    sb.show_score()

    # 如果游戏处于非活动状态就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    #暂停按钮
    if stats.game_pause:
        pause_button.draw_button()

    pg.display.flip()

def update_enemies(enemies, hero, bullets,bursts, stats, t_interval, sb):
    """
	生成新enemy
	更新enemy的位置或发射子弹，判断enemy是否与hero碰撞,若是，将碰撞的enemy存到hero.plane，
	并把hero.plane.jackedTime记录为当前时间，并在enemies中remove掉这个enemy
	sb: 需要更新劫机剩余时间，劫的机的生命值
	"""
    enemies.update(bullets, hero, t_interval)

    if not hero.plane:
        jacked_enemies = pg.sprite.spritecollide(hero, enemies, False)
        if jacked_enemies:
            hero.plane = jacked_enemies[0]
            enemies.remove(jacked_enemies[0])           
            hero.plane.image=hero.plane.images[1] if hero.face_right else hero.plane.images[0]  
            hero.shoot_dir=0 if hero.face_right else math.pi
            for i in range(4):
                hero.plane.moving_udlr[i] = False
            hero.moving_up = False
            hero.moving_left = False
            hero.moving_right = False
            hero.jumporfall = False
           
            # 开始倒计时
            hero.plane.jackedTime = time.clock()
            sb.prep_planeTimeLimit(hero.plane.jackedTime)

    else:
        enemies_crash = pg.sprite.spritecollide(hero.plane, enemies, False)
        if enemies_crash:
            start_burst(True,hero,bursts)
            hero.plane = None
            hero.face_right = True
            hero.shoot_dir = 0
            hero.jumporfall = True
            hero.jumpfallspeed = 0
            hero.life -= 1
            for enemy_crash in enemies_crash:
                start_burst(True,enemy_crash,bursts)
                enemies.remove(enemy_crash)

def update_bursts(bursts):
    bursts.update()
    for burst in bursts.copy():
        if burst.time>1600:
            bursts.remove(burst)

def start_burst(isenemy, obj, bursts):
    burst = Burst(isenemy, (obj.rect.centerx, obj.rect.centery))
    bursts.add(burst)


def update_bullets(sett, bullets, hero, enemies, bursts, screen, stats, t_interval, sb):
    """
	更新子弹位置，判断子弹是否与hero或enemies碰撞,导弹与敌方炮弹是否碰撞
	"""
    #先更新子弹
    for i in range(6):
        if i == 2:
            bullets[i].update(bullets, t_interval, enemies)
        else:
            bullets[i].update(bullets, t_interval)

    # hero中弹
    hero_get_shot(bullets, hero,bursts, sb)

    # 敌机中弹，可能要更新最高分，当前分数，生成新的敌机
    enemy_get_shot(bullets, enemies,bursts, stats, sett, sb, screen)

    # 己方导弹中弹：
    hero_missile_get_shot(bullets,bursts)

    # 对方导弹中弹
    enemy_missile_get_shot(bullets,bursts)

def hero_get_shot(bullets, hero,bursts, sb):
    """
    :param bullets: 子弹列表，编组的列表
    :param hero: 英雄
    :param sb: 可能需要更新截的机的生命值
    """
    me = hero.plane if hero.plane else hero
    for i in range(3):
        bullet_hits = pg.sprite.spritecollide(me, bullets[i + 3], False)
        for bullet_hit in bullet_hits:
            if i==2:
                start_burst(False,bullet_hit,bursts)
            me.life -= bullet_hit.lethality
            if me.life <= 0:
                if str(type(me)) != "<class 'hero.Hero'>":
                    # 驾驶的敌机毁灭, 主角生命值减一
                    start_burst(True,hero,bursts)
                    hero.life -= 1
                    hero.plane = None
                    hero.face_right = True
                    hero.shoot_dir = 0
                    hero.jumporfall = True
                    hero.jumpfallspeed = 0
            bullets[i + 3].remove(bullet_hit)

def enemy_get_shot(bullets, enemies,bursts, stats, sett, sb, screen):
    """
    :param bullets: 子弹列表，编组的列表
    :param enemies: 敌机编组
    :param stats: 统计信息，记录游戏当前得分（经验），最高得分，英雄等级，英雄还剩多少条命
    :param sett: 游戏设置，记录游戏当前状态
    :param sb: 游戏积分榜，包括要显示的一些信息
    :param screen: 创建敌机用
    """
    for i in range(3):
        collisions0 = pg.sprite.groupcollide(bullets[i], enemies, True, False)
        if collisions0:
            for bullet_hit, enemy_hits in collisions0.items():
                if i == 2:
                    start_burst(False,bullet_hit, bursts)
                enemy_hits[0].life -= bullet_hit.lethality
                stats.score += bullet_hit.lethality
                if enemy_hits[0].life <= 0:
                    start_burst(True,enemy_hits[0], bursts)               
                    enemies.remove(enemy_hits[0])
                    stats.score += sett.enemy_points
    #更新当前分数
    sb.prep_score()
    if stats.score >= stats.level**2 * sett.enemy_points:
        stats.level += 1
        sb.prep_level()
    #更新最高分
    if stats.high_score < stats.score:
        stats.high_score = stats.score
        sb.prep_high_score()

    #如果敌机数目比2小，则创建敌机
    if len(enemies) <= 2:
        create_enemys(sett, screen, enemies)

def hero_missile_get_shot(bullets,bursts):
    """己方导弹中弹"""
    for i in range(3):
        collisions1 = pg.sprite.groupcollide(bullets[2], bullets[i + 3], False, False)
        if collisions1:
            for mymissile, enmbullets in collisions1.items():
                for enmbullet in enmbullets:
                    mymissile.life -= enmbullet.lethality
                    if mymissile.life <= 0:
                        start_burst(False, mymissile, bursts)
                        bullets[2].remove(mymissile)
                    if i == 2:
                        enmbullet.life -= mymissile.lethality
                        if enmbullet.life <= 0:
                            start_burst(False,enmbullet,bursts)
                            bullets[5].remove(enmbullet)
                    else:
                        bullets[i + 3].remove(enmbullet)

def enemy_missile_get_shot(bullets, bursts):
    """敌方导弹中弹"""
    for i in range(3):
        collisions2 = pg.sprite.groupcollide(bullets[5], bullets[i], False, False)
        if collisions2:
            for enmmissile, mybullets in collisions2.items():
                for mybullet in mybullets:
                    enmmissile.life -= mybullet.lethality
                    if enmmissile.life <= 0:
                        start_burst(False,enmmissile, bursts)
                        bullets[5].remove(enmmissile)
                    if i == 2:
                        mybullet.life -= enmmissile.lethality
                        if mybullet.life <= 0:
                            start_burst(False,mybullet,bursts)
                            bullets[2].remove(mybullet)
                    else:
                        bullets[i].remove(mybullet)

def create_enemys(settings, screen, enemys):
    """创建3个敌机，并添加进enemys内"""
    for i in range(3):
        # 选择创建敌机类型
        randnum = random.randint(1, 10)
        if randnum<= settings.separates[0]:  # 敌机0
            enemytemp = enemy.Ordin_plane(settings, screen)
            enemys.add(enemytemp)
        elif randnum > settings.separates[0] and randnum <= settings.separates[1]:  # 敌机1
            enemytemp = enemy.Multi_plane(settings, screen)
            enemys.add(enemytemp)
        else:  # 敌机2
            enemytemp = enemy.Missile_plane(settings, screen)
            enemys.add(enemytemp)

def night_or_day(t_interval, stats,sett):
    stats.time_+=t_interval
    if not stats.night and stats.time_>=90:
        stats.night=True
        sett.bg_color=(0,0,0)
        stats.time_=0
    elif stats.night and stats.time_>=30:
        stats.night=False
        sett.bg_color=(0,255,255)
        stats.time_=0