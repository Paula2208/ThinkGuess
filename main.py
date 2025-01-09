import pygame
import sys
import utils
import random
import time
import constants as const
from player import Player
from maze import Maze

pygame.init()

# Window
screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
pygame.display.set_caption("Think Guess")
bg_menu = pygame.image.load("assets/backgrounds/rose_bg.jpg")
bg = pygame.image.load("assets/backgrounds/bg_dark.jpg")
bg_puzzle = pygame.image.load("assets/backgrounds/bg_purple.jpg")
bg_combat = pygame.image.load("assets/backgrounds/bg_combat.jpg")
player_menu = pygame.image.load("assets/player/player_left.png")

# Fonts
papyrus120 = pygame.font.SysFont("papyrus", 120)
papyrus80 = pygame.font.SysFont("papyrus", 80)
papyrus50 = pygame.font.SysFont("papyrus", 50)
papyrus30 = pygame.font.SysFont("papyrus", 30)
papyrus14 = pygame.font.SysFont("papyrus", 14)
arial30 = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

def main_menu():
    while True:
        initText_x, initText_y = const.WIDTH // 3, const.HEIGHT // 2

        screen.fill(const.BACKGROUND)
        screen.blit(bg_menu, (0, 0))
        screen.blit(player_menu, (const.WIDTH - 200, initText_y))
        
        utils.draw_text("Think Guess", papyrus120, const.BLUE, screen, initText_x, initText_y)
        utils.draw_text("Pelea o Piensa", papyrus80, const.BLUE, screen, initText_x, initText_y + 120)
        utils.draw_text("Presiona ENTER para jugar", papyrus30, const.BLACK, screen, (const.WIDTH // 3) * 2 , (const.HEIGHT // 4) * 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                
                if event.key == pygame.K_RETURN and game_over:
                    game_over = False
                    game_loop()

                if event.key == pygame.K_ESCAPE and game_over:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def game_loop():
    maze = Maze()
    maze.create_maze()
    player = Player()
    player_pos = [1, 1]

    running = True
    level_completed = False

    while running:
        screen.fill(const.BACKGROUND)
        screen.blit(bg, (0, 0))

        maze.draw_maze(screen, player_pos, player)
        utils.draw_battery(screen, 50, const.HEIGHT - 55, player.health, const.PLAYER_MAX_HEALTH, papyrus30)

        if level_completed:
            utils.show_level_completed_modal(screen, papyrus50, papyrus30)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN and level_completed:
                    maze.create_maze()  # Create new level
                    player_pos = [1, 1]
                    level_completed = False 

            elif event.type == pygame.QUIT:
                running = False

        # Handle player movement
        pressed_keys = pygame.key.get_pressed()
        player.move(pressed_keys, maze.maze)

        # Check Level completed
        if maze.maze[player.x][player.y] == 2:
            level_completed = True

        # Check enemy collision
        for enemy in maze.enemies:
            if player.rect.colliderect(enemy.rect):
                maze.current_enemy = enemy
                show_puzzle(player, maze)

        pygame.display.flip()
        clock.tick(30)


def show_puzzle(player, maze):

    # Riddle
    riddle = random.choice(const.RIDDLES)
    question = riddle[0]
    correct_answer = riddle[1]
    
    # User Input
    user_answer = ""
    active = True
    wrong = False

    def display_answer_lines():
        return " ".join(["_" if c != " " else " " for c in correct_answer])
    
    while active:
        screen.fill(const.BACKGROUND)
        screen.blit(bg_puzzle, (0, 0))

        utils.draw_text(question, papyrus50, const.BLUE, screen, const.WIDTH // 2, const.HEIGHT // 4)

        answer_lines = display_answer_lines()
        utils.draw_text(user_answer, arial30, const.PURPLE, screen, const.WIDTH // 2, (const.HEIGHT // 4) * 2 - 40)
        utils.draw_text(answer_lines, arial30, const.PURPLE, screen, const.WIDTH // 2, (const.HEIGHT // 4) * 2)

        utils.draw_text("Escribe la respuesta y presiona Enter", papyrus30, const.BLUE, screen, const.WIDTH // 2, const.HEIGHT // 1.5)
        utils.draw_text("O presiona tab para pelear", papyrus30, const.RED, screen, const.WIDTH // 2, const.HEIGHT - 100)

        if wrong:
            utils.draw_text("¡Incorrecto! Intenta de nuevo.", papyrus30, const.RED, screen, const.WIDTH // 2, const.HEIGHT // 1.5 + 40)

        # Get user answer
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_answer == correct_answer:
                        utils.remove_enemy(player, maze)
                        player.heal(const.PLAYER_HEAL)
                        active = False
                        wrong = False
                    else:
                        wrong = True
                        user_answer = ""

                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]

                elif event.key == pygame.K_TAB:
                    combat(player, maze)
                    active = False

                else:
                    if len(user_answer) < len(correct_answer):
                        user_answer += event.unicode.lower()

        pygame.display.flip()

def combat(player, maze):
    enemy = maze.current_enemy
    player.changeSize(const.ITEMS_WIDTH)
    maze.current_enemy.changeSize(const.ITEMS_WIDTH)
    active = True

    enemy.rect.centerx = const.WIDTH // 2
    enemy.rect.centery = const.HEIGHT // 2

    enemy_move_x_direction = 1
    enemy_move_y_direction = 1

    while active:
        screen.fill(const.BACKGROUND)
        screen.blit(bg_combat, (0, 0))

        player.draw(screen)
        enemy.draw(screen)
        player.projectiles.draw(screen)
        enemy.projectiles.draw(screen)

        # Enemy Health
        utils.draw_text(f"{player.health} HP", papyrus50, const.GREEN, screen, 300, 50)
        utils.draw_text(f"Enemigo: {enemy.health} HP", papyrus50, const.BLACK, screen, const.WIDTH - 300, 50)

        # Player Combat
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        keys = pygame.key.get_pressed()
        player.move_on_combat(keys)

        # Enemy automatic combat
        if time.time() - enemy.last_move_time > enemy.move_delay:
            enemy.last_move_time = time.time()

            enemy.rect.x += enemy.speed * enemy_move_x_direction
            if enemy.rect.right >= const.WIDTH or enemy.rect.left <= 0:
                enemy_move_x_direction *= -1

            enemy.rect.y += enemy.speed * enemy_move_y_direction
            if enemy.rect.bottom >= const.HEIGHT or enemy.rect.top <= 0:
                enemy_move_y_direction *= -1

        if random.randint(1, 100) == 1:
            enemy.shoot()

        # Projectiles Manage
        player.projectiles.update()
        enemy.projectiles.update()

        for projectile in player.projectiles:
            if enemy.rect.colliderect(projectile.rect):
                enemy.take_damage(const.PLAYER_DAMAGE) # Player hurts enemy
                projectile.kill()

        for projectile in enemy.projectiles:
            if player.rect.colliderect(projectile.rect):
                player.take_damage(enemy.damage) # Enemy hurts player
                projectile.kill()

        # Check Combat ended
        if player.health == 0:
            print("Game Over")
            game_over_screen()
            return

        if enemy.health == 0:
            player.changeSize(const.PLAYER_INIT)
            utils.remove_enemy(player, maze)
            active = False

        pygame.display.flip()

def game_over_screen():
    while True:
        screen.fill(const.BACKGROUND)
        screen.blit(bg_menu, (0, 0))

        utils.draw_text("¡GAME OVER!", papyrus120, const.RED, screen, const.WIDTH // 2, const.HEIGHT // 3)
        utils.draw_text("Presiona ENTER para volver a comenzar", papyrus50, const.BLUE, screen, const.WIDTH // 2, const.HEIGHT // 2)
        utils.draw_text("O presiona ESC para salir", papyrus50, const.BLUE, screen, const.WIDTH // 2, const.HEIGHT // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
