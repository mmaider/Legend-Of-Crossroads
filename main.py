import pygame.transform

from game_methods import *


def main_menu():
    global running, menu_running, rules_running, settings_running, screen, WIDTH, HEIGHT, musicvolume
    intro_text = ['THE FLOORS']
    buttons = ['Начать игру']
    rules = ['Правила игры']
    settings = ['Настройки']
    fon = pygame.transform.scale(load_image('main_back.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('verdana', 50)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.SysFont('verdana', 20)
    for line in buttons:
        string_rendered = font.render(line, 1, (0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    for line in rules:
        string_rendered = font.render(line, 1, (0, 0, 0))
        intro_rect1 = string_rendered.get_rect()
        text_coord += 10
        intro_rect1.top = text_coord
        intro_rect1.centerx = WIDTH // 2
        text_coord += intro_rect1.height
        screen.blit(string_rendered, intro_rect1)
    for line in settings:
        string_rendered = font.render(line, 1, (0, 0, 0))
        intro_rect2 = string_rendered.get_rect()
        text_coord += 10
        intro_rect2.top = text_coord
        intro_rect2.centerx = WIDTH // 2
        text_coord += intro_rect2.height
        screen.blit(string_rendered, intro_rect2)

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] < intro_rect1.right) and (pos[0] > intro_rect1.left) and (pos[1] > intro_rect1.top) and (
                        pos[1] < intro_rect1.bottom):
                    menu_running = False
                    rules_running = True
                if (pos[0] < intro_rect2.right) and (pos[0] > intro_rect2.left) and (pos[1] > intro_rect2.top) and (
                        pos[1] < intro_rect2.bottom):
                    menu_running = False
                    settings_running = True
                if (pos[0] < intro_rect.right) and (pos[0] > intro_rect.left) and (pos[1] > intro_rect.top) and (
                        pos[1] < intro_rect.bottom):
                    menu_running = False
                    pygame.mixer.music.load('music/battletheme.mp3')
                    pygame.mixer.music.set_volume(musicvolume)
                    pygame.mixer.music.play(loops=-1)
        pygame.display.flip()
        clock.tick(20)


def settings():
    global running, menu_running, settings_running, screen, WIDTH, HEIGHT, musicvolume, soundvolume
    intro_text = ['Настройки']
    font = pygame.font.SysFont('verdana', 35)
    buttons = [font.render('-', 1, (255, 255, 255)), font.render('-', 1, (255, 255, 255)),
               font.render('+', 1, (255, 255, 255)), font.render('+', 1, (255, 255, 255))]
    main_text = ['В главное меню']
    buttonsrect = [buttons[0].get_rect(), buttons[1].get_rect(), buttons[2].get_rect(), buttons[3].get_rect()]
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_running = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] < intro_rect.right) and (pos[0] > intro_rect.left) and (pos[1] > intro_rect.top) and (
                        pos[1] < intro_rect.bottom):
                    menu_running = True
                    settings_running = False
                elif (pos[0] < buttonsrect[0].right) and (pos[0] > buttonsrect[0].left) and (
                        pos[1] > buttonsrect[0].top) and (pos[1] < buttonsrect[0].bottom) and musicvolume > 0:
                    musicvolume = round(musicvolume - 0.1, 1)
                    pygame.mixer.music.set_volume(musicvolume)
                elif (pos[0] < buttonsrect[2].right) and (pos[0] > buttonsrect[2].left) and (
                        pos[1] > buttonsrect[2].top) and (pos[1] < buttonsrect[2].bottom) and musicvolume < 1:
                    musicvolume = round(musicvolume + 0.1, 1)
                    pygame.mixer.music.set_volume(musicvolume)
                elif (pos[0] < buttonsrect[1].right) and (pos[0] > buttonsrect[1].left) and (
                        pos[1] > buttonsrect[1].top) and (pos[1] < buttonsrect[1].bottom) and soundvolume > 0:
                    soundvolume = round(soundvolume - 0.1, 1)
                elif (pos[0] < buttonsrect[3].right) and (pos[0] > buttonsrect[3].left) and (
                        pos[1] > buttonsrect[3].top) and (pos[1] < buttonsrect[3].bottom) and soundvolume < 1:
                    soundvolume = round(soundvolume + 0.1, 1)
        rules_text = ['Громкость музыки: ' + str(musicvolume), 'Громкость звуков: ' + str(soundvolume)]
        fon = pygame.transform.scale(load_image('main_back.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        screen.blit(pygame.transform.scale(load_image("Dialog.png"), (WIDTH - 6, HEIGHT // 2 + 50)), (3, 20))
        screen.blit(pygame.transform.scale(load_image("martin.png"), (300, 400)), (WIDTH - 250, HEIGHT // 2 + 40))
        font = pygame.font.SysFont('verdana', 35)
        text_coord = 30
        for line in intro_text:
            string_rendered = font.render(line, 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.centerx = WIDTH // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_coord += 10
        for line in range(len(rules_text)):
            string_rendered = font.render(rules_text[line], 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            button_rect = buttons[line].get_rect()
            button_rect.top = intro_rect.top
            button_rect.right = intro_rect.right + 30
            screen.blit(buttons[line], button_rect)
            buttonsrect[line] = button_rect
            button1_rect = buttons[line + 2].get_rect()
            button1_rect.top = button_rect.top
            button1_rect.right = button_rect.right + 30
            screen.blit(buttons[line + 2], button1_rect)
            buttonsrect[line + 2] = button1_rect
        text_coord += 20
        font = pygame.font.SysFont('verdana', 20)
        for line in main_text:
            string_rendered = font.render(line, 1, (255, 255, 255))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.centerx = WIDTH // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            font = pygame.font.SysFont('verdana', 20)
        pygame.display.flip()
        clock.tick(20)


def rules_menu():
    global running, menu_running, rules_running, screen, WIDTH, HEIGHT
    intro_text = ['Правила игры']
    rules_text = ['- Привет! Слышал эту городскую легенду про демона перекрёстка? Нет?!',
                  '- Недалеко от города есть закрытое шоссе с подозрительным перекрёстком.',
                  '- Говорят, там люди пропадают. Ну, знаешь, нечисть всякая бесится... ',
                  '- Так вот, не поможешь мне разобраться с этой чертовщиной? Ты в деле? Супер!',
                  '- Используй WASD для управления. Можешь стрелять по врагам с помощью пробела,',
                  '- а в качестве прицела используй курсор... А, и ещё.',
                  '- Если тебе повезёт увидеть демона перекрёстка, не дай ему себя схватить',
                  '- и стреляй ему в голову. Патроны и аптечки иногда будут появляться на локации.',
                  '- На этом всё! Удачи!']
    main_text = ['В главное меню']
    fon = pygame.transform.scale(load_image('main_back.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(pygame.transform.scale(load_image("Dialog.png"), (WIDTH - 6, HEIGHT // 2 + 50)), (3, 20))
    screen.blit(pygame.transform.scale(load_image("martin.png"), (300, 400)), (WIDTH - 250, HEIGHT // 2 + 40))
    font = pygame.font.SysFont('verdana', 35)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.SysFont('verdana', 17)
    text_coord += 10
    for line in rules_text:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    text_coord += 20
    font = pygame.font.SysFont('verdana', 20)
    for line in main_text:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        font = pygame.font.SysFont('verdana', 20)
    while rules_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rules_running = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] < intro_rect.right) and (pos[0] > intro_rect.left) and (pos[1] > intro_rect.top) and (
                        pos[1] < intro_rect.bottom):
                    menu_running = True
                    rules_running = False
        pygame.display.flip()
        clock.tick(20)


def main_cycle():
    global running, lost_running, bfrunning, timer, curscore, penta, musicvolume, soundvolume
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.magazine > 0:
                shoot_sound.set_volume(soundvolume)
                shoot_sound.play()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullet = player.shoot(bulletimage, mouse_x, mouse_y)
                all_sprites.add(bullet)
                bullets.add(bullet)
                player.magazine -= 1
    screen.blit(bgimg, (0, 0))
    blit_alpha(screen, penta, (0, 0), (255 * curscore) // 20)
    all_sprites.update(player.rect.x, player.rect.y)

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        exp_sound.set_volume(soundvolume)
        exp_sound.play()
        m = Mob(mobimage, 6, 4)
        all_sprites.add(m)
        mobs.add(m)
        curscore += 1

    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        beat_sound.set_volume(soundvolume)
        beat_sound.play()
        player.life -= 1
        m = Mob(mobimage, 6, 4)
        all_sprites.add(m)
        mobs.add(m)

    if timer // 60 == 20:
        m = Heal(healimage, 2, 1)
        all_sprites.add(m)
        healers.add(m)
        timer = 0
        m = Heal(bulletsimage, 2, 1)
        all_sprites.add(m)
        amo.add(m)

    hits = pygame.sprite.spritecollide(player, healers, True)
    if hits:
        player.life += 3

    hits = pygame.sprite.spritecollide(player, amo, True)
    if hits:
        player.magazine += 10

    if player.life <= 0:
        lost_running = True
        pygame.mixer.music.load('music/loosetheme.mp3')
        pygame.mixer.music.set_volume(musicvolume)
        pygame.mixer.music.play(loops=-1)

    font = pygame.font.Font(None, 32)
    all_sprites.draw(screen)
    text = font.render(
        "HP: " + str(player.life), True, WHITE)
    place = text.get_rect(topleft=(10, 5))
    screen.blit(text, place)
    blit_stats(screen, text.get_width() + 20, 10, player.life, 10, GREEN)
    text = font.render(
        "BULLETS: " + str(player.magazine), True, WHITE)
    place = text.get_rect(topleft=(10, 30))
    screen.blit(text, place)
    blit_stats(screen, text.get_width() + 20, 40, player.magazine, 20, RED)
    text = font.render(
        "SCORE: " + str(curscore), True, WHITE)
    place = text.get_rect(topleft=(10, 55))
    screen.blit(text, place)

    if curscore >= 20:
        bfrunning = True

    pygame.display.flip()
    timer += 1


def game_over():
    global running, menu_running, lost_running, screen, WIDTH, HEIGHT, result, musicvolume
    if result:
        intro_text = ['!ПОБЕДА!']
        fon = pygame.transform.scale(load_image('win_back.png'), (WIDTH, HEIGHT))
    else:
        intro_text = ['ИГРА ОКОНЧЕНА']
        fon = pygame.transform.scale(load_image('lost_back.png'), (WIDTH, HEIGHT))
    buttons = ['В главное меню']
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('verdana', 50)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    font = pygame.font.SysFont('verdana', 17)
    for line in buttons:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clear_sprites()

    while lost_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lost_running = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] < intro_rect.right) and (pos[0] > intro_rect.left) and (pos[1] > intro_rect.top) and (
                        pos[1] < intro_rect.bottom):
                    lost_running = False
                    menu_running = True
                    pygame.mixer.music.load('music/menutheme.mp3')
                    pygame.mixer.music.set_volume(musicvolume)
                    pygame.mixer.music.play(loops=-1)
        pygame.display.flip()
        clock.tick(20)


def bossfight():
    global running, bfrunning, lost_running, screen, WIDTH, HEIGHT, result, timer, musicvolume, soundvolume
    all_sprites = pygame.sprite.Group()
    bosshead = DevilHead(devilhead)
    bossrhand = DevilHand(devilrhand)
    bossrhand.rotspeed = -0.1
    bossrhand.maxangle = -45
    bossrhand.rect.x = WIDTH // 2 + 50
    bosslhand = DevilHand(devillhand)
    bosslhand.rotspeed = 0.1
    bosslhand.rect.x = - bossrhand.rect.x
    player.rect.centerx = WIDTH // 2
    player.rect.bottom = HEIGHT
    all_sprites.add(player)
    all_sprites.add(bosshead)
    all_sprites.add(bossrhand)
    all_sprites.add(bosslhand)
    devil = pygame.sprite.Group()
    devil.add(bosshead)
    devil.add(bossrhand)
    devil.add(bosslhand)
    bad_bullets = pygame.sprite.Group()
    m = Bullet(bulletimage, random.randrange(0, WIDTH), 0, 0, 1)
    all_sprites.add(m)
    bad_bullets.add(m)
    timer = 0
    font = pygame.font.Font(None, 50)
    text = font.render("!BOSSFIGHT!", True, WHITE)
    place = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    boss_sound.set_volume(soundvolume)
    boss_sound.play()
    for i in range(1, 3):
        screen.blit(bgimg, (0, 0))
        screen.blit(penta, (0, 0))
        all_sprites.draw(screen)
        screen.blit(pygame.transform.scale(load_image("heart" + str(3 - i) + ".png"), (400, 300)), (220, 300))
        screen.blit(text, place)
        pygame.display.flip()
        pygame.time.wait(i * 1000)
    while bfrunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bfrunning = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_sound.set_volume(soundvolume)
                    shoot_sound.play()
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    bullet = player.shoot(bulletimage, mouse_x, mouse_y)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
        screen.blit(bgimg, (0, 0))
        screen.blit(penta, (0, 0))
        if pygame.sprite.spritecollide(player, devil, False, collided=pygame.sprite.collide_mask):
            player.life -= 1
        hits = pygame.sprite.spritecollide(bosshead, bullets, False, collided=pygame.sprite.collide_mask)
        for hit in hits:
            exp_sound.set_volume(soundvolume)
            exp_sound.play()
            bosshead.life -= 1
            hit.kill()
            if bosshead.life <= 0:
                boss_sound.set_volume(soundvolume)
                boss_sound.play()
                for i in range(1, 3):
                    screen.blit(bgimg, (0, 0))
                    screen.blit(penta, (0, 0))
                    all_sprites.draw(screen)
                    screen.blit(pygame.transform.scale(load_image("heart" + str(i) + ".png"), (400, 300)),
                                (220, 300))
                    pygame.display.flip()
                    pygame.time.wait(i * 1000)
                bfrunning = False
                lost_running = True
                result = True
                pygame.mixer.music.load('music/loosetheme.mp3')
                pygame.mixer.music.set_volume(musicvolume)
                pygame.mixer.music.play(loops=-1)
                break
        hits = pygame.sprite.spritecollide(player, bad_bullets, False, collided=pygame.sprite.collide_mask)
        for hit in hits:
            beat_sound.set_volume(soundvolume)
            beat_sound.play()
            player.life -= 1
            hit.kill()
        if player.life <= 0:
            bfrunning = False
            lost_running = True
            pygame.mixer.music.load('music/loosetheme.mp3')
            pygame.mixer.music.set_volume(musicvolume)
            pygame.mixer.music.play(loops=-1)
        if timer // 5:
            m = Bullet(bulletimage, random.randrange(0, WIDTH), 0, 0, 1)
            all_sprites.add(m)
            bad_bullets.add(m)
            timer = 0

        all_sprites.update()
        all_sprites.draw(screen)
        font = pygame.font.Font(None, 32)
        text = font.render(
            "HP: " + str(player.life), True, WHITE)
        place = text.get_rect(topleft=(10, 5))
        screen.blit(text, place)
        blit_stats(screen, text.get_width() + 20, 10, player.life, 10, GREEN)

        text1 = font.render(
            "DEVIL: " + str(bosshead.life), True, WHITE)
        place = text1.get_rect(topright=(WIDTH - 10, 5))
        blit_stats(screen, WIDTH - (text1.get_width() + 120), 10, bosshead.life, 20, RED)
        screen.blit(text1, place)
        timer += 1
        pygame.display.flip()
        clock.tick(FPS)


def clear_sprites():
    global all_sprites, mobs, bullets, player, curscore, result
    result = False
    curscore = 0
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player(playerimage, 4, 4)
    all_sprites.add(player)
    for i in range(3):
        m = Mob(mobimage, 6, 4)
        all_sprites.add(m)
        mobs.add(m)


pygame.font.init()

img_dir = os.path.join(os.path.dirname(__file__), 'img')

pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
toplayer = pygame.display.set_mode((WIDTH, HEIGHT))
toplayer.set_alpha(255)
pygame.display.set_caption("Legend of Crossroads")
pygame.display.set_icon(pygame.image.load("img/Crossroads.png"))

clock = pygame.time.Clock()
musicvolume = 0.5
soundvolume = 0.5

bgimg = pygame.transform.scale(load_image("bg.png"), (WIDTH, HEIGHT))
playerimage = pygame.transform.scale(load_image("playerimg1.png"), (380, 624))
mobimage = pygame.transform.scale(load_image("mob.png"), (350, 236))
healimage = pygame.transform.scale(load_image("heal.png"), (150, 57))
bulletsimage = pygame.transform.scale(load_image("bullets.png"), (150, 70))
devilhead = pygame.transform.scale(load_image("bosshead.png"), (WIDTH, HEIGHT))
devilrhand = pygame.transform.scale(load_image("bossrighthand1.png"), (WIDTH, HEIGHT))
devillhand = pygame.transform.scale(load_image("bosslefthand1.png"), (WIDTH, HEIGHT))
bulletimage = pygame.transform.scale(load_image("bullet.png"), (20, 30))
penta = pygame.transform.scale(load_image("penta.png"), (WIDTH, HEIGHT))
deadbosshead = pygame.transform.scale(load_image("deadbosshead.png"), (WIDTH, HEIGHT))
pygame.transform.scale(load_image("penta.png"), (WIDTH, HEIGHT))

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player(playerimage, 4, 4)
bosshead = DevilHead(devilhead)
bossrhand = DevilHand(devilrhand)
bossrhand.rotspeed = -0.1
bossrhand.maxangle = -45
bossrhand.rect.x = WIDTH // 2 + 50

bosslhand = DevilHand(devillhand)
bosslhand.rotspeed = 0.1
bosslhand.rect.x = - bossrhand.rect.x
healers = pygame.sprite.Group()
amo = pygame.sprite.Group()
all_sprites.add(player)
pygame.mixer.music.load('music/menutheme.mp3')
pygame.mixer.music.set_volume(musicvolume)
pygame.mixer.music.play(loops=-1)
shoot_sound = pygame.mixer.Sound('music/pew.wav')
exp_sound = pygame.mixer.Sound('music/expl3.wav')
shoot_sound = pygame.mixer.Sound('music/pew.wav')
beat_sound = pygame.mixer.Sound('music/beat.mp3')
boss_sound = pygame.mixer.Sound('music/bosssound.mp3')

for i in range(3):
    m = Mob(mobimage, 6, 4)
    all_sprites.add(m)
    mobs.add(m)

running = True
menu_running = True
settings_running = False
rules_running = False
lost_running = False
bfrunning = False
result = False

while running:
    clock.tick(FPS)
    if menu_running:
        main_menu()
    elif rules_running:
        rules_menu()
    elif settings_running:
        settings()
    elif lost_running:
        game_over()
    elif bfrunning:
        bossfight()
    else:
        main_cycle()

pygame.quit()
