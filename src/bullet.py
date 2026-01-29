import pygame


class Bullet:
    def __init__(self, x, y, direction):
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.direction = direction
        self.speed = 500

    def update(self, dt):
        self.pos_x += self.direction[0] * self.speed * dt
        self.pos_y += self.direction[1] * self.speed * dt
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", self.rect.center, 5)
