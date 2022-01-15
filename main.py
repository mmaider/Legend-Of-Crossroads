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
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player.shoot(mouse_x, mouse_y)
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

    if player.life == 0:
        running = False
    font = pygame.font.Font(None, 32)
    all_sprites.draw(screen)
    text = font.render(
        str(player.life), True, WHITE)
    place = text.get_rect(center=(50, 30))
    screen.blit(text, place)
    blit_hp(screen, 5, 5, player.life)
    pygame.display.flip()

pygame.quit()
