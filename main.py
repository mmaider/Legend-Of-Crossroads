from game_methods import *


def main_menu():
    global running, menu_running, rules_running, screen, WIDTH, HEIGHT
    intro_text = ['THE FLOORS']
    buttons = ['Начать игру']
    rules = ['Правила игры']
    fon = pygame.transform.scale(load_image('main_back.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('verdana', 50)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH//2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.SysFont('verdana', 20)
    for line in rules:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect1 = string_rendered.get_rect()
        text_coord += 10
        intro_rect1.top = text_coord
        intro_rect1.x = 10
        print(intro_rect1)
        text_coord += intro_rect1.height
        screen.blit(string_rendered, intro_rect1)
    for line in buttons:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        print(intro_rect)
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

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
                if (pos[0] < intro_rect.right) and (pos[0] > intro_rect.left) and (pos[1] > intro_rect.top) and (
                        pos[1] < intro_rect.bottom):
                    menu_running = False
        pygame.display.flip()
        clock.tick(20)


def rules_menu():
    global running, menu_running, rules_running, screen, WIDTH, HEIGHT
    intro_text = ['Правила игры']
    rules_text = ['- Ваша задача - убить как можно больше призраков',
                  '- Если вы сталкиваетесь с призраком, ваше здоровье падает',
                  '- Используйте WASD для передвижения по полю',
                  '- Используйте пробел для стрельбы',
                  '- Используйте курсор для задания направления стрельбы']
    main_text = ['В главное меню']
    fon = pygame.transform.scale(load_image('main_back.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('verdana', 35)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH//2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.SysFont('verdana', 17)
    for line in rules_text:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.SysFont('verdana', 20)
    for line in main_text:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH//2
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
    global running, lost_running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullet = player.shoot(mouse_x, mouse_y)
                all_sprites.add(bullet)
                bullets.add(bullet)
    screen.blit(bgimg, (0, 0))
    all_sprites.update(player.rect.x, player.rect.y)

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob(mobimage, 6, 4)
        all_sprites.add(m)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        player.life -= 1
        m = Mob(mobimage, 6, 4)
        all_sprites.add(m)
        mobs.add(m)

    if player.life <= 0:
        lost_running = True
    font = pygame.font.Font(None, 32)
    all_sprites.draw(screen)
    text = font.render(
        str(player.life), True, WHITE)
    place = text.get_rect(center=(50, 30))
    screen.blit(text, place)
    blit_hp(screen, 5, 5, player.life)
    pygame.display.flip()


def game_over():
    global running, menu_running, lost_running, screen, WIDTH, HEIGHT
    clear_sprites()
    intro_text = ['ИГРА ОКОНЧЕНА']
    buttons = ['В главное меню']
    fon = pygame.transform.scale(load_image('lost_back.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('verdana', 50)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH//2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    font = pygame.font.SysFont('verdana', 17)
    for line in buttons:
        string_rendered = font.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.centerx = WIDTH//2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

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
        pygame.display.flip()
        clock.tick(20)


def clear_sprites():
    global all_sprites, mobs, bullets, player
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player(playerimage, 9, 4)
    all_sprites.add(player)
    for i in range(3):
        m = Mob(mobimage, 6, 4)
        all_sprites.add(m)
        mobs.add(m)


pygame.font.init()

img_dir = os.path.join(os.path.dirname(__file__), 'img')
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floors")
clock = pygame.time.Clock()

bgimg = pygame.transform.scale(load_image("bg.png"), (WIDTH, HEIGHT))
playerimage = pygame.transform.scale(load_image("playerimg.png"), (576, 256))
mobimage = pygame.transform.scale(load_image("mob.png"), (282, 190))

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player(playerimage, 9, 4)
all_sprites.add(player)

for i in range(3):
    m = Mob(mobimage, 6, 4)
    all_sprites.add(m)
    mobs.add(m)

running = True
menu_running = True
rules_running = False
lost_running = False

while running:
    clock.tick(FPS)
    if menu_running:
        main_menu()
    elif rules_running:
        rules_menu()
    elif lost_running:
        game_over()
    else:
        main_cycle()

pygame.quit()
