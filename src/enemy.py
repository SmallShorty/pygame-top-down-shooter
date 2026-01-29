import pygame
import random


class Enemy:
    def __init__(self, x, y):
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 100
        self.color = "red"
        self.health = 1
        self.reward = 10

    @staticmethod
    def spawn(spawn_points):
        coords = random.choice(spawn_points)
        chance = random.random()

        if chance < 0.1:
            return BigEnemy(coords[0], coords[1])
        elif chance < 0.3:
            return FastEnemy(coords[0], coords[1])
        else:
            return Enemy(coords[0], coords[1])

    def update(self, dt, player_pos):
        dx = player_pos[0] - self.pos_x
        dy = player_pos[1] - self.pos_y
        dist = (dx**2 + dy**2) ** 0.5

        if dist != 0:
            self.pos_x += (dx / dist) * self.speed * dt
            self.pos_y += (dy / dist) * self.speed * dt

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "orange"
        self.speed = 200
        self.reward = 25


class BigEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "purple"
        self.speed = 50
        self.health = 5
        self.rect.size = (80, 80)
        self.reward = 100
