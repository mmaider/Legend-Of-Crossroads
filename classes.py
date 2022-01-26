import pygame
import random
import os
from os import path
from ini import *


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
        return bullet


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
