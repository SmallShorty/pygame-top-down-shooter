import pygame
import sys
from src.database import ScoreBoard
from src.player import Player
from src.enemy import Enemy
from settings import WIDTH, HEIGHT, FPS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
header = pygame.font.SysFont("Arial", 72)


def main():
    scene = "menu"
    player_name = ""
    player = None
    enemies = []
    score = 0

    db = ScoreBoard()
    data_saved = False
    top_scores = []

    game_timer = 20.0
    spawn_timer = 0
    spawn_delay = 1.5

    spawn_points = [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]

    while True:
        dt = clock.tick(FPS) / 1000.0
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if scene == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        player = Player(WIDTH // 2, HEIGHT // 2, player_name)
                        scene = "game"
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 12:
                            player_name += event.unicode

            elif scene == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        scene = "menu"

        screen.fill((30, 30, 30))

        if scene == "menu":
            title_surf = header.render("Введите имя и нажмите Enter:", True, "white")
            screen.blit(
                title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            )

            name_surf = font.render(
                player_name if player_name else "...", True, "yellow"
            )
            screen.blit(
                name_surf, name_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
            )

        elif scene == "game":
            spawn_timer += dt
            if spawn_timer >= spawn_delay:
                enemies.append(Enemy.spawn(spawn_points))
                spawn_timer = 0

            keys = pygame.key.get_pressed()
            player.move(keys, dt, WIDTH, HEIGHT)
            player.shoot(dt)
            player.update_bullets(dt, WIDTH, HEIGHT)

            for e in enemies[:]:
                e.update(dt, player.rect.center)

                if e.rect.colliderect(player.rect):
                    scene = "game_over"

                for b in player.bullets[:]:
                    if b.rect.colliderect(e.rect):
                        e.health -= 1
                        if b in player.bullets:
                            player.bullets.remove(b)
                        if e.health <= 0:
                            score += e.reward
                            if e in enemies:
                                enemies.remove(e)

            game_timer -= dt
            if game_timer <= 0:
                scene = "win"

            player.draw(screen)
            for e in enemies:
                e.draw(screen)

            score_surf = font.render(f"Очки: {score}", True, "white")
            screen.blit(score_surf, (20, 20))

            timer_surf = font.render(f"Время: {max(0, int(game_timer))}", True, "red")
            screen.blit(timer_surf, (WIDTH - 150, 20))

        elif scene == "game_over":

            if not data_saved:
                db.save_score(player.name, score)
                top_scores = db.get_top_scores()
                data_saved = True

            msg = header.render("ИГРА ОКОНЧЕНА", True, (255, 50, 50))
            msg_rect = msg.get_rect(center=(WIDTH // 2, 100))
            screen.blit(msg, msg_rect)

            current_score_surf = font.render(f"Ваш результат: {score}", True, "white")
            screen.blit(
                current_score_surf,
                current_score_surf.get_rect(center=(WIDTH // 2, 180)),
            )

            pygame.draw.line(
                screen, "gray", (WIDTH // 2 - 150, 220), (WIDTH // 2 + 150, 220), 2
            )

            y_pos = 250
            title_top = font.render("ЛУЧШИЕ РЕЗУЛЬТАТЫ", True, "yellow")
            screen.blit(title_top, title_top.get_rect(center=(WIDTH // 2, y_pos)))

            for i, (name, s) in enumerate(top_scores):

                rank_surf = font.render(f"{i+1}.", True, "gray")
                name_surf = font.render(f"{name}", True, "cyan")
                points_surf = font.render(f"{s}", True, "white")

                row_y = y_pos + 50 + i * 40

                screen.blit(rank_surf, (WIDTH // 2 - 140, row_y))
                screen.blit(name_surf, (WIDTH // 2 - 100, row_y))
                screen.blit(points_surf, (WIDTH // 2 + 80, row_y))

            hint_surf = font.render(
                "Нажмите ENTER, чтобы вернуться в меню", True, (150, 150, 150)
            )
            screen.blit(hint_surf, hint_surf.get_rect(center=(WIDTH // 2, HEIGHT - 50)))

        pygame.display.flip()


if __name__ == "__main__":
    main()
