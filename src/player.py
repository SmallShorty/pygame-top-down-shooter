import pygame
from src.bullet import Bullet


class Player:
    def __init__(self, x, y, name):
        self.name = name

        self.pos_x = float(x)
        self.pos_y = float(y)

        self.rect = pygame.Rect(x, y, 50, 50)

        self.direction = [0, -1]

        self.speed = 250
        self.bullets = []
        self.shoot_cooldown = 0.3
        self.shoot_timer = 0

    def move(self, keys, dt, screen_width, screen_height):
        move_x, move_y = 0, 0

        if keys[pygame.K_LEFT]:
            move_x = -1
        if keys[pygame.K_RIGHT]:
            move_x = 1
        if keys[pygame.K_UP]:
            move_y = -1
        if keys[pygame.K_DOWN]:
            move_y = 1

        if move_x != 0 or move_y != 0:

            self.direction = [move_x, move_y]

            self.pos_x += move_x * self.speed * dt
            self.pos_y += move_y * self.speed * dt

            self.pos_x = max(0, min(self.pos_x, screen_width - self.rect.width))
            self.pos_y = max(0, min(self.pos_y, screen_height - self.rect.height))

            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)

    def shoot(self, dt):

        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            new_bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets.append(new_bullet)
            self.shoot_timer = self.shoot_cooldown

    def update_bullets(self, dt, width, height):
        for b in self.bullets[:]:
            b.update(dt)
            if b.rect.x < 0 or b.rect.x > width or b.rect.y < 0 or b.rect.y > height:
                self.bullets.remove(b)

    def draw(self, screen):
        pygame.draw.rect(screen, "cyan", self.rect)

        for b in self.bullets:
            b.draw(screen)
