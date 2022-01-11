import pygame
import random
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.life = 10
        self.speedx = 0
        self.speedy = 0

    def update(self, *args):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_w]:
            self.speedy = -5
        if keystate[pygame.K_s]:
            self.speedy = 5
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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -40
        self.speed = random.randrange(1, 6)

    def update(self, *args):
        if self.rect.x < args[0]:
            self.rect.x += self.speed
        if self.rect.x > args[0]:
            self.rect.x -= self.speed
        if self.rect.y < args[1]:
            self.rect.y += self.speed
        if self.rect.y > args[1]:
            self.rect.y -= self.speed
        if self.rect.top > HEIGHT + 40 or self.rect.left < -10 or self.rect.right > WIDTH + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = -40

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self, *args):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
#player_img = pygame.image.load(path.join(img_dir, "whiteboi1.png")).convert()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(3):
    m = Mob()
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
                player.shoot()

    all_sprites.update(player.rect.x, player.rect.y)

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        for i in range(random.randrange(0, 3, 1)):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        player.life -= 1
        for i in range(random.randrange(0, 5, 1)):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

    if player.life == 0:
        running = False
    font = pygame.font.Font(None, 72)
    screen.fill(BLACK)
    all_sprites.draw(screen)
    text = font.render(
        str(player.life), True, WHITE)
    place = text.get_rect(
        center=(100, 100))
    screen.blit(text, place)
    pygame.display.flip()


pygame.quit()
