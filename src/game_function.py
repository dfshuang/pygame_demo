import sys
import pygame as pg
from bullet import *
import time
import enemy
from burst import *
import random
import math


def handle_events(sett, screen,bg, hero, enemies, boss, bullets, bursts, stats, sb, sound, menu):
    """处理键盘和鼠标事件"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            with open("record.txt", 'a+') as fw:
                fw.write(str(stats.high_score) + '\n')
            sys.exit()

        elif event.type == pg.KEYDOWN:
            handle_keydown(sett, screen, event, enemies, boss, hero, bullets, bursts, stats, sb, sound)

        elif event.type == pg.KEYUP:
            handle_keyup(event, hero)

        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            handle_mouse(sett, mouse_x, mouse_y, menu, stats, enemies, boss, bullets,bg)


def handle_keydown(sett, screen, event, enemies, boss, hero, bullets, bursts, stats, sb, sound):
    # 退出游戏界面
    if event.key == pg.K_q:
        # 记录最高分
        with open("record.txt", 'a+') as fw:
            fw.write(str(stats.high_score) + '\n')
        sys.exit()

    # 暂停游戏
    elif event.key == pg.K_p:
        stats.game_windows['game_pause'] = not stats.game_windows['game_pause']

    # 开始游戏
    elif event.key == pg.K_RETURN:
        if stats.game_windows['start_menu'] and not stats.game_windows['game_active']:
            stats.game_windows['start_game'] = True
            stats.game_windows['start_menu'] = False
            game_play(stats, sett, enemies, boss, bullets)
        elif stats.game_windows['continue']:
            stats.game_windows['good_job'] = False
            stats.game_windows['start_menu'] = False
            stats.game_windows['continue'] = False
            stats.game_windows['game_over'] = False
            stats.game_windows['game_pause'] = False
            stats.game_windows['setting'] = False
            stats.game_windows['record'] = False
            stats.game_windows['help'] = False

    # 没有开敌机
    elif not hero.plane:
        # 移动
        if event.key == pg.K_d:
            hero.moving_left = False
            hero.moving_right = True
            hero.clock = pg.time.Clock()
            hero._t = 0
            if not hero.face_right:
                hero.face_right = True
                degreepi = math.pi if hero.shoot_dir >= 0 else -math.pi
                hero.shoot_dir = degreepi - hero.shoot_dir
        elif event.key == pg.K_a:
            hero.moving_right = False
            hero.moving_left = True
            hero.clock = pg.time.Clock()
            hero._t = 0
            if hero.face_right:
                hero.face_right = False
                degreepi = math.pi if hero.shoot_dir >= 0 else -math.pi
                hero.shoot_dir = degreepi - hero.shoot_dir
        elif event.key == pg.K_k:
            if not hero.jumporfall:
                hero.jumporfall = True
                hero.jumpfallspeed = hero.jump_init_speed
                # 改变image和rect
                lr = 1 if hero.face_right else 0
                hero.image = hero.images['jump'][lr]
                tmprect = hero.rect
                hero.rect = hero.image.get_rect()
                hero.rect.centerx, hero.rect.centery = tmprect.centerx, tmprect.centery


        # 瞄准，开火
        # 向上调角度
        elif event.key == pg.K_i:
            if hero.face_right:
                if hero.shoot_dir < math.pi / 2:
                    hero.shoot_dir += sett.dir_factor

                    if not hero.moving_right and not hero.moving_left and not hero.jumporfall:
                        hero.image = hero.images['stand'][int(hero.shoot_dir // (math.pi / 4) + 2)]
                        tmprect = hero.rect
                        hero.rect = hero.image.get_rect()
                        hero.rect.centerx, hero.rect.centery = tmprect.centerx, tmprect.centery
            else:
                if hero.shoot_dir > math.pi / 2 or hero.shoot_dir <= -math.pi / 2:
                    hero.shoot_dir -= sett.dir_factor
                    if hero.shoot_dir <= -math.pi:
                        hero.shoot_dir = math.pi
                    if not hero.moving_right and not hero.moving_left and not hero.jumporfall:
                        if hero.shoot_dir > 0:
                            index = int(11 - hero.shoot_dir // (math.pi / 4))
                        else:
                            index = int(3 - hero.shoot_dir // (math.pi / 4))
                        hero.image = hero.images['stand'][index]
                        tmprect = hero.rect
                        hero.rect = hero.image.get_rect()
                        hero.rect.centerx, hero.rect.centery = tmprect.centerx, tmprect.centery

        # 向下调角度
        elif event.key == pg.K_o:
            if hero.face_right:
                if hero.shoot_dir > -math.pi / 2:
                    hero.shoot_dir -= sett.dir_factor
                    if not hero.moving_right and not hero.moving_left and not hero.jumporfall:
                        hero.image = hero.images['stand'][int(hero.shoot_dir // (math.pi / 4) + 2)]
                        tmprect = hero.rect
                        hero.rect = hero.image.get_rect()
                        hero.rect.centerx, hero.rect.centery = tmprect.centerx, tmprect.centery
            else:
                if hero.shoot_dir >= math.pi / 2 or hero.shoot_dir < -math.pi / 2:
                    hero.shoot_dir += sett.dir_factor
                    if hero.shoot_dir > math.pi:
                        hero.shoot_dir = -math.pi + sett.dir_factor
                    if not hero.moving_right and not hero.moving_left and not hero.jumporfall:
                        if hero.shoot_dir > 0:
                            index = int(4 - hero.shoot_dir // (math.pi / 4) + 7)
                        else:
                            index = int(-4 - hero.shoot_dir // (math.pi / 4) + 7)
                        hero.image = hero.images['stand'][index]
                        tmprect = hero.rect
                        hero.rect = hero.image.get_rect()
                        hero.rect.centerx, hero.rect.centery = tmprect.centerx, tmprect.centery

        # 开火
        elif event.key == pg.K_j:
            bullet0 = Bullet0(sett, screen, hero, hero.shoot_dir, True, hero.lethality)
            bullets[0].add(bullet0)
            sound.do_play['fire'] = True

        # 技能
        elif event.key == pg.K_u:
            if hero.cool_finished:
                sound.do_play['skill'] = True
                hero.cool_finished = False
                hero.skilling = True

    # 开敌机
    else:
        # 移动
        if event.key == pg.K_d:
            hero.plane.moving_udlr[2] = False
            hero.plane.moving_udlr[3] = True
            if not hero.face_right:
                hero.face_right = True
                hero.plane.image = hero.plane.images[1]
                degreepi = math.pi if hero.shoot_dir >= 0 else -math.pi
                hero.shoot_dir = degreepi - hero.shoot_dir
        elif event.key == pg.K_a:
            hero.plane.moving_udlr[3] = False
            hero.plane.moving_udlr[2] = True
            if hero.face_right:
                hero.face_right = False
                hero.plane.image = hero.plane.images[0]
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

        elif event.key == pg.K_j:
            # 开火,不同战机不同子弹
            if str(type(hero.plane)) == "<class 'enemy.Ordin_plane'>":
                # 三连发
                for i in range(3):
                    tmp = DefaultObj()
                    tmp.rect.centerx, tmp.rect.centery = hero.plane.rect.centerx - 18 * i, hero.plane.rect.centery
                    bullet0 = Bullet0(sett, screen, tmp, hero.shoot_dir, True)
                    bullets[0].add(bullet0)
                sound.do_play['fire'] = True
            elif str(type(hero.plane)) == "<class 'enemy.Multi_plane'>":
                bullet1 = Bullet1(sett, screen, hero.plane, hero.shoot_dir, True)
                bullets[1].add(bullet1)
                sound.do_play['fire'] = True
            elif str(type(hero.plane)) == "<class 'enemy.Missile_plane'>":
                bullet2 = Bullet2(sett, screen, hero.plane, 0, True, enemies, bullets, boss)
                bullets[2].add(bullet2)
                sound.do_play['missile'] = True

        elif event.key == pg.K_k:
            # 以跳跃方式离开敌机
            start_burst(True, hero, bursts, sound)
            hero.plane = None
            hero.face_right = True
            hero.shoot_dir = 0
            hero.jumporfall = True
            hero.jumpfallspeed = hero.jump_init_speed
        elif event.key == pg.K_l:
            # 以下落方式离开敌机
            start_burst(True, hero, bursts, sound)
            hero.plane = None
            hero.face_right = True
            hero.shoot_dir = 0
            hero.jumporfall = True
            hero.jumpfallspeed = 0
        elif event.key == pg.K_u:
            if hero.cool_finished:
                sound.do_play['skill'] = True
                hero.cool_finished = False
                hero.skilling = True


def handle_keyup(event, hero):
    # 没有开敌机
    if not hero.plane:
        if event.key == pg.K_d:
            if hero.moving_right:
                hero.moving_right = False
                hero.image = hero.images['stand'][int(hero.shoot_dir // (math.pi / 4) + 2)]

        elif event.key == pg.K_a:
            if hero.moving_left:
                hero.moving_left = False
                if hero.shoot_dir < 0:
                    hero.image = hero.images['stand'][int(3 - hero.shoot_dir // (math.pi / 4))]
                else:
                    hero.image = hero.images['stand'][int(11 - hero.shoot_dir // (math.pi / 4))]


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


def handle_mouse(sett, mouse_x, mouse_y, menu, stats, enemies, boss, bullets,bg):
    """处理鼠标事件，刚开始的开始菜单"""
    menu.collide_mouse(mouse_x, mouse_y, stats)

    game_play(stats, sett, enemies, boss, bullets)

    if stats.game_windows['game_pause'] or not stats.game_windows['game_active'] \
            or stats.game_windows['game_over'] or stats.game_windows['continue']:
        if bg.type!=stats.game_windows['scene']:
            bg.type=stats.game_windows['scene']
            if bg.type=='bluesky':
                bg.fullimage=bg.skys[0]
                bg.images[1]=bg.lands[0]
            else:
                bg.fullimage=bg.skys[1]
                bg.images[1]=bg.lands[1]
            bg.images[0]=bg.fullimage.subsurface(pg.Rect((0,0),(1000,600)))
            bg.rects[1]=bg.images[1].get_rect()
            bg.rects[1].bottom=sett.screen_height
            bg.T=(bg.fullimage.get_rect().width-1000) * sett.bgmoveT


def game_play(stats, sett, enemies, boss, bullets):
    """开始游戏"""
    # 点击开始游戏
    if stats.game_windows['start_game']:
        stats.time_ = 0
        boss.appeared = False
        boss.time0 = 0.0
        boss.rect.left, boss.rect.centery = sett.screen_width, 0.5 * sett.screen_height
        boss._t = 0
        boss.t = 0
        boss.life = sett.bossLife
        # 重置游戏统计信息
        stats.reset_stats()

        # 清空敌机列表和子弹列表
        enemies.empty()
        for bulletsx in bullets:
            bulletsx.empty()

        stats.game_windows['game_active'] = True
        stats.game_windows['start_game'] = False


def update_screen(sett, screen, bg, hero, enemies, boss, bullets, bursts, menu, stats, sb, sound):
    """更新屏幕"""
    sound.play_snd(stats)
    # 重绘屏幕背景颜色
    if stats.night:
        screen.fill((0, 0, 0))
    else:
        bg.drawme(screen)

    # 重绘子弹
    for i in range(6):
        if bullets[i]:
            bullets[i].draw(screen)

    if not stats.night:
        # 绘制Boss
        if boss.appeared:
            screen.blit(boss.image, boss.rect)
        # 重绘敌机
        if enemies:
            enemies.draw(screen)

    # 重绘主角
    hero.drawme()

    # 重绘爆炸
    bursts.draw(screen)

    # 重绘游戏显示信息
    sb.show_message()

    # 是否显示鼠标,游戏暂停或未进入游戏
    if not stats.game_windows['game_active'] or stats.game_windows['game_pause'] or \
            stats.game_windows['game_over'] or stats.game_windows['continue']:
        pg.mouse.set_visible(True)
    else:
        pg.mouse.set_visible(False)

    # 重绘控件
    menu.draw(stats)

    pg.display.flip()


def update_enemies(enemies, boss, hero, bullets, bursts, stats, t_interval, sb, sound):
    """
	生成新enemy
	更新enemy的位置或发射子弹，判断enemy是否与hero碰撞,若是，将碰撞的enemy存到hero.plane，
	并把hero.plane.jackedTime记录为当前时间，并在enemies中remove掉这个enemy
	sb: 需要更新劫机剩余时间，劫的机的生命值
	"""
    enemies.update(bullets, hero, t_interval, sound)

    if not hero.plane:
        jacked_enemies = pg.sprite.spritecollide(hero, enemies, False)
        if jacked_enemies:
            sound.do_play['hijacked'] = True
            hero.plane = jacked_enemies[0]
            enemies.remove(jacked_enemies[0])
            hero.plane.image = hero.plane.images[1] if hero.face_right else hero.plane.images[0]
            hero.shoot_dir = 0 if hero.face_right else math.pi
            for i in range(4):
                hero.plane.moving_udlr[i] = False
            hero.moving_up = False
            hero.moving_left = False
            hero.moving_right = False
            hero.jumporfall = False

            # 开始倒计时
            hero.plane.jackedTime = 0
            stats.planeTimeLimit = hero.plane.time_limit

    else:
        enemies_crash = pg.sprite.spritecollide(hero.plane, enemies, False)
        if enemies_crash:
            start_burst(True, hero, bursts, sound)
            hero.plane = None
            hero.face_right = True
            hero.shoot_dir = 0
            hero.jumporfall = True
            hero.jumpfallspeed = 0
            hero.life -= 1
            for enemy_crash in enemies_crash:
                start_burst(True, enemy_crash, bursts, sound)
                enemies.remove(enemy_crash)
        elif boss.appeared:
            boss_t = [boss]
            bosses_crash = pg.sprite.spritecollide(hero.plane, boss_t, False)
            if bosses_crash:
                start_burst(True, hero, bursts, sound)
                hero.plane = None
                hero.face_right = True
                hero.shoot_dir = 0
                hero.jumporfall = True
                hero.jumpfallspeed = 0
                hero.life -= 3


def update_bursts(bursts, t_interval):
    bursts.update(t_interval)
    for burst in bursts.copy():
        if burst.time > 1600:
            bursts.remove(burst)


def start_burst(isenemy, obj, bursts, sound):
    burst = Burst(isenemy, (obj.rect.centerx, obj.rect.centery))
    bursts.add(burst)
    sound.do_play['burst'] = True


def update_bullets(sett, bullets, hero, enemies, boss, bursts, screen, stats, t_interval, sb, sound):
    """
	更新子弹位置，判断子弹是否与hero或enemies碰撞,导弹与敌方炮弹是否碰撞
	"""
    # 先更新子弹
    for i in range(6):
        if i == 2:
            bullets[i].update(bullets, t_interval, enemies, boss)
        else:
            bullets[i].update(bullets, t_interval)

    # hero中弹
    hero_get_shot(bullets, hero, bursts, sb, sound)

    # 敌机中弹，可能要更新最高分，当前分数，生成新的敌机
    enemy_get_shot(hero, bullets, enemies, boss, bursts, stats, sett, sb, screen, sound)

    # 己方导弹中弹：
    hero_missile_get_shot(bullets, bursts, sound)

    # 对方导弹中弹
    enemy_missile_get_shot(bullets, bursts, sound)


def hero_get_shot(bullets, hero, bursts, sb, sound):
    """
    :param bullets: 子弹列表，编组的列表
    :param hero: 英雄
    :param sb: 可能需要更新截的机的生命值
    """
    me = hero.plane if hero.plane else hero
    for i in range(3):
        bullet_hits = pg.sprite.spritecollide(me, bullets[i + 3], False)
        for bullet_hit in bullet_hits:
            if i == 2:
                # start_burst(False,bullet_hit,bursts,sound)
                sound.do_play['hitted'] = True
            me.life -= bullet_hit.lethality
            if me.life <= 0:
                if str(type(me)) != "<class 'hero.Hero'>":
                    # 驾驶的敌机毁灭, 主角生命值减一
                    start_burst(True, hero, bursts, sound)
                    hero.life -= 1
                    hero.plane = None
                    hero.face_right = True
                    hero.shoot_dir = 0
                    hero.jumporfall = True
                    hero.jumpfallspeed = 0
            bullets[i + 3].remove(bullet_hit)


def enemy_get_shot(hero, bullets, enemies, boss, bursts, stats, sett, sb, screen, sound):
    """
    :param bullets: 子弹列表，编组的列表
    :param enemies: 敌机编组
    :param stats: 统计信息，记录游戏当前得分（经验），最高得分，英雄等级，英雄还剩多少条命
    :param sett: 游戏设置，记录游戏当前状态
    :param sb: 游戏积分榜，包括要显示的一些信息
    :param screen: 创建敌机用
    """
    if boss.appeared:
        for i in range(3):
            bullet_hits = pg.sprite.spritecollide(boss, bullets[i], False)
            for bullet_hit in bullet_hits:
                if i == 2:
                    start_burst(False, bullet_hit, bursts, sound)
                    sound.do_play['burst'] = True
                boss.life -= bullet_hit.lethality
                stats.bossLife = boss.life
                if boss.life <= 0:
                    #重置boss属性
                    stats.time_ = 0
                    boss.appeared = False
                    stats.game_windows['boss_appear'] = False
                    stats.game_windows['good_job'] = True
                    boss.time0 = 0.0
                    boss.rect.left, boss.rect.centery = sett.screen_width, 0.5 * sett.screen_height
                    boss._t = 0
                    boss.t = 0
                    boss.life = sett.bossLife

                    #continue
                    boss_burst(boss, bursts, sound)
                    stats.score += sett.enemy_points * 10
                    stats.game_windows['continue'] = True

                    # 增加下一关难度，发射子弹频率
                    for i in range(4):
                        sett.fire_T[i] -= 2 * (i + 1)
                        if sett.fire_T[i] < 5:
                            sett.fire_T[i] = 5
                    boss.fire_T = sett.fire_T[3]



                bullets[i].remove(bullet_hit)

    for i in range(3):
        collisions0 = pg.sprite.groupcollide(bullets[i], enemies, True, False)
        if collisions0:
            for bullet_hit, enemy_hits in collisions0.items():
                if i == 2:
                    start_burst(False, bullet_hit, bursts, sound)
                    sound.do_play['burst'] = True
                enemy_hits[0].life -= bullet_hit.lethality
                stats.score += bullet_hit.lethality
                if enemy_hits[0].life <= 0:
                    start_burst(True, enemy_hits[0], bursts, sound)
                    enemies.remove(enemy_hits[0])
                    stats.score += sett.enemy_points

    # 更新当前分数
    if stats.score >= stats.level ** 2 * 2 * sett.enemy_points:
        stats.level += 1
        sound.do_play['upgrade'] = True

        if stats.level % 3 == 0:
            hero.lethality += 0.5
        elif stats.level % 3 == 1:
            hero.life += 10
        elif stats.level % 3 == 2:
            hero.jump_init_speed -= 60

    # 更新最高分
    if stats.high_score < stats.score:
        stats.high_score = stats.score

    # 如果敌机数目比2小，则创建敌机
    if len(enemies) <= (0 if boss.appeared else 2):
        create_enemys(sett, screen, enemies)


def boss_burst(boss, bursts, sound):
    tmps = []
    for i in range(5):
        tmp = DefaultObj()
        tmps.append(tmp)
    tmps[0].rect.centerx, tmp.rect.centery = boss.rect.centerx, boss.rect.centery
    tmps[1].rect.centerx, tmp.rect.centery = boss.rect.centerx + 20, boss.rect.centery - 10
    tmps[2].rect.centerx, tmp.rect.centery = boss.rect.centerx - 15, boss.rect.centery - 20
    tmps[3].rect.centerx, tmp.rect.centery = boss.rect.centerx - 20, boss.rect.centery + 20
    tmps[4].rect.centerx, tmp.rect.centery = boss.rect.centerx + 30, boss.rect.centery + 15
    for i in range(5):
        start_burst(True, tmps[i], bursts, sound)


def hero_missile_get_shot(bullets, bursts, sound):
    """己方导弹中弹"""
    for i in range(3):
        collisions1 = pg.sprite.groupcollide(bullets[2], bullets[i + 3], False, False)
        if collisions1:
            for mymissile, enmbullets in collisions1.items():
                for enmbullet in enmbullets:
                    mymissile.life -= enmbullet.lethality
                    if mymissile.life <= 0:
                        start_burst(False, mymissile, bursts, sound)
                        bullets[2].remove(mymissile)
                    if i == 2:
                        enmbullet.life -= mymissile.lethality
                        if enmbullet.life <= 0:
                            start_burst(False, enmbullet, bursts, sound)
                            bullets[5].remove(enmbullet)
                    else:
                        bullets[i + 3].remove(enmbullet)


def enemy_missile_get_shot(bullets, bursts, sound):
    """敌方导弹中弹"""
    for i in range(3):
        collisions2 = pg.sprite.groupcollide(bullets[5], bullets[i], False, False)
        if collisions2:
            for enmmissile, mybullets in collisions2.items():
                for mybullet in mybullets:
                    enmmissile.life -= mybullet.lethality
                    if enmmissile.life <= 0:
                        start_burst(False, enmmissile, bursts, sound)
                        bullets[5].remove(enmmissile)
                    if i == 2:
                        mybullet.life -= enmmissile.lethality
                        if mybullet.life <= 0:
                            start_burst(False, mybullet, bursts, sound)
                            bullets[2].remove(mybullet)
                    else:
                        bullets[i].remove(mybullet)


def create_enemys(settings, screen, enemys):
    """创建3个敌机，并添加进enemys内"""
    for i in range(settings.enemy_num):
        # 选择创建敌机类型
        randnum = random.randint(1, 10)
        if randnum <= settings.separates[0]:  # 敌机0
            enemytemp = enemy.Ordin_plane(settings, screen)
            enemys.add(enemytemp)
        elif randnum > settings.separates[0] and randnum <= settings.separates[1]:  # 敌机1
            enemytemp = enemy.Multi_plane(settings, screen)
            enemys.add(enemytemp)
        else:  # 敌机2
            enemytemp = enemy.Missile_plane(settings, screen)
            enemys.add(enemytemp)


def night_or_day(t_interval, stats, sett):
    """当stats.time_ 每次加一定的时间（t_interval）,达到一定的数值后进入黑夜"""
    #boss出现前，黑夜白天轮转
    if not stats.game_windows['boss_appear'] and not stats.game_windows['show_danger']:
        stats.time_ += t_interval
        if stats.time_ > sett.night_interval * 4:
            stats.time_ = 0

        if stats.time_ >= sett.night_interval * 3:
            stats.night = True
        elif stats.time_ < sett.night_interval * 3:
            stats.night = False

    #boss出现5秒前模式
    else:
        # 黑夜，白天，闪电模式转换；黑夜：boss出现前5秒，闪电：boss出现(每隔0.4秒切换黑夜和白天)
        if stats.game_windows['show_danger']:
            stats.night = True  #进入黑夜模式，boss出现前5秒，在enemy文件里修改
            stats.time_ = 0
        elif stats.game_windows['boss_appear']:
            stats.time_ += t_interval
            if stats.time_ > 0.4:
                stats.night = not stats.night  #进入闪电模式
                stats.time_ = 0
