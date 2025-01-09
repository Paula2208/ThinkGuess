import pygame
import constants as const

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def show_level_completed_modal(screen, font1, font2):
    modal_width, modal_height = const.WIDTH // 2, const.HEIGHT // 3
    modal = pygame.Surface((modal_width, modal_height), pygame.SRCALPHA)
    pygame.draw.rect(modal, const.BROWN_OPAC, (0, 0, modal_width, modal_height), border_radius=20)

    # Center
    modal_rect = modal.get_rect(center=(const.WIDTH // 2, const.HEIGHT // 2))
    screen.blit(modal, modal_rect.topleft)

    draw_text("¡Nivel Completado!", font1, const.GREEN, screen, modal_rect.centerx, modal_rect.top + modal_height // 4)
    draw_text("Presiona Enter para continuar", font2, const.BLACK, screen, modal_rect.centerx, modal_rect.bottom - modal_height // 4)

def draw_battery(screen, x, y, hp, max_hp, font):
    battery_color = const.RED if hp < 25 else const.GREEN
    height = 50
    max_bars = max_hp // const.BATTERY_BAR_WIDTH
    max_width = max_bars * (const.BATTERY_BAR_WIDTH + 2)

    pygame.draw.rect(screen, const.BLACK, (x, y, max_width, height), border_radius=5, width=2) # Wrapper
    pygame.draw.rect(screen, const.BLACK, (x + max_width, y + height // 4, 10, height // 2)) # Terminal
    draw_text(f"{hp} HP", font, battery_color, screen, x + max_width + 50, y + (height // 4)*2)

    bars = hp // const.BATTERY_BAR_WIDTH  # Battery HP
    remaining_hp = hp % const.BATTERY_BAR_WIDTH # Remaining last bar

    for i in range(bars):
        padding = 4

        bar_x = x + padding + i * const.BATTERY_BAR_WIDTH + 2
        bar_y = padding + y + 1
        bar_width = const.BATTERY_BAR_WIDTH - 4 if i < bars - 1 or remaining_hp == 0 else int(
            (remaining_hp / const.BATTERY_BAR_WIDTH) * (const.BATTERY_BAR_WIDTH - 4)
        )

        pygame.draw.rect(screen, battery_color, (bar_x, bar_y, bar_width, height - 10))
    
def remove_enemy(player, maze):
    maze.enemies.remove(maze.current_enemy)
    maze.current_enemy = None
    print("Enemy beaten.")
