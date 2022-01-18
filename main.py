import pygame
import random
import os
from os import path

pygame.font.init()

img_dir = path.join(path.dirname(__file__), 'img')
WIDTH = 600
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floors")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_row = 0
        self.cur_frame = 0
        self.image = self.frames[self.cur_row][self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.life = 10
        self.speedx = 0
        self.speedy = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            self.frames.append([])
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames[j].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -5
            self.cur_row = 1
        elif keystate[pygame.K_d]:
            self.speedx = 5
            self.cur_row = 3
        if keystate[pygame.K_w]:
            self.speedy = -5
            self.cur_row = 0
        elif keystate[pygame.K_s]:
            self.speedy = 5
            self.cur_row = 2
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

        self.cur_frame = (self.cur_frame + 1) % len(self.frames[0])
        self.image = self.frames[self.cur_row][self.cur_frame]

    def shoot(self, mx, my):
        # print(mx, my, self.rect.x, self.rect.y)

        if my > self.rect.y:
            ky = 1
        elif my == self.rect.y:
            ky = 0
        else:
            ky = -1
        try:
            if ky == -1:
                kx = 1 / (((600 - my) - (600 - self.rect.y)) / (mx - self.rect.x))
            else:
                kx = -1 / (((600 - my) - (600 - self.rect.y)) / (mx - self.rect.x))
        except ZeroDivisionError:
            kx = 1
        # print(kx, ky)
        bullet = Bullet(self.rect.centerx, self.rect.top, kx, ky)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_row = 0
        self.cur_frame = 0
        self.image = self.frames[self.cur_row][self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -40
        self.speed = random.randrange(1, 6)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            self.frames.append([])
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames[j].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args):
        if self.rect.x < args[0]:
            self.rect.x += self.speed
            self.cur_row = 2
        elif self.rect.x > args[0]:
            self.rect.x -= self.speed
            self.cur_row = 1
        if self.rect.y < args[1]:
            self.rect.y += self.speed
            self.cur_row = 0
        elif self.rect.y > args[1]:
            self.rect.y -= self.speed
            self.cur_row = 3
        if self.rect.top > HEIGHT + 40 or self.rect.left < -10 or self.rect.right > WIDTH + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = -40

        self.cur_frame = (self.cur_frame + 1) % len(self.frames[0])
        self.image = self.frames[self.cur_row][self.cur_frame]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, kx, ky):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10 * kx
        self.speedy = 10 * ky

    def update(self, *args):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()


def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def blit_hp(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 10) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def main_menu():
    global running, menu_running, rules_running, screen, WIDTH, HEIGHT
    intro_text = ['THE FLOORS']
    buttons = ['Начать игру']
    rules = ['Правила игры']
    fon = pygame.transform.scale(load_image('main_back.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('verdana', 35)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
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

    font = pygame.font.SysFont('serif', 17)
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
                menu_running = False
                rules_running = True
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
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.SysFont('serif', 20)
    for line in rules_text:
        string_rendered = font.render(line, 1, (230, 230, 230))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.SysFont('serif', 25)
    for line in main_text:
        string_rendered = font.render(line, 1, (255, 255, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
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
                menu_running = True
                rules_running = False
        pygame.display.flip()
        clock.tick(20)

def main_cycle():
    global running
    print(1)


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

while running:
    clock.tick(FPS)
    if menu_running:
        main_menu()
    elif rules_running:
        rules_menu()
    else:
        main_cycle()

pygame.quit()
