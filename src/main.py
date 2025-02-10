import pygame
import random
from settings import WIDTH, HEIGHT, WHITE, FPS, JUMP_STRENGTH, MAX_HORIZONTAL_GAP, MAX_VERTICAL_GAP, PLATFORM_WIDTH
from player import Player
from platforms import Platform
from powerup import PowerUp

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump Game")

platforms = [Platform(WIDTH // 2 - 50, HEIGHT - 50)]
player = Player(platforms[0])
powerups = []

def restart_game():
    global player, platforms, powerups
    first_platform = Platform(WIDTH // 2 - 50, HEIGHT - 50, force_static=True)
    platforms = [first_platform]
    player = Player(platforms[0])
    powerups.clear()

def game_loop():
    global running
    clock = pygame.time.Clock()
    restart_game()
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()
        
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update(platforms)

        if player.y < HEIGHT // 3:
            shift = abs(player.vel_y)
            player.y += shift
            for platform in platforms:
                platform.y += shift
            for powerup in powerups:
                powerup.y += shift

        elif player.vel_y > 0 and player.y > HEIGHT // 1.5:
            shift = player.vel_y
            player.y -= shift
            for platform in platforms:
                platform.y -= shift
            for powerup in powerups:
                powerup.y -= shift


        if all(platform.y < -HEIGHT -200 for platform in platforms):
            for alpha in range(0, 255, 10):
                fade_surface = pygame.Surface((WIDTH, HEIGHT))
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                font = pygame.font.Font(None, 50)
                text = font.render("Game Over!", True, (255, 0, 0))
                screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                pygame.display.update()
                pygame.time.delay(50)
            pygame.time.delay(2000)
            restart_game()

        for platform in platforms:
            platform.update()

        platforms[:] = [p for p in platforms if p.y < HEIGHT + 100 and not p.is_gone]

        for powerup in powerups:
            powerup.update()
            if powerup.collect(player):
                player.vel_y = -15

        if platforms and platforms[-1].y > 50:
            prev_platform = platforms[-1]
            max_jump_height = max(50, JUMP_STRENGTH * 2)
            min_gap = 45
            max_gap = min(MAX_VERTICAL_GAP, max_jump_height)

            if max_gap < min_gap:
                max_gap = min_gap

            new_y = prev_platform.y - random.randint(min_gap, max_gap)
            max_reach = WIDTH // 3
            new_x = random.randint(
                max(0, prev_platform.x - min(MAX_HORIZONTAL_GAP, max_reach)),
                min(WIDTH - PLATFORM_WIDTH, prev_platform.x + min(MAX_HORIZONTAL_GAP, max_reach))
            )

            if new_y > 0:
                new_platform = Platform(new_x, new_y)
                platforms.append(new_platform)

                if random.random() < 0.1:
                    powerups.append(PowerUp(new_platform))

        powerups[:] = [p for p in powerups if p.active]

        player.draw(screen)
        for platform in platforms:
            platform.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)

        pygame.display.update()

    pygame.quit()

game_loop()
