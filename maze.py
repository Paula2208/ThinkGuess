import pygame
import random
import constants as const
from enemy import Enemy

wall_img = pygame.Surface((const.TILE_SIZE, const.TILE_SIZE), pygame.SRCALPHA)
wall_img.fill((0, 0, 0, 0)) # Fill transparent
pygame.draw.circle(
    wall_img, 
    const.BROWN, 
    (const.TILE_SIZE // 2, const.TILE_SIZE // 2),
    const.WALL_THICKNESS // 2 
)

door_img = pygame.image.load("assets/backgrounds/Door.png")
door_img = pygame.transform.scale(door_img, (const.TILE_SIZE, const.TILE_SIZE))

path_img = pygame.image.load("assets/backgrounds/Path.png")
path_img = pygame.transform.scale(path_img, (const.TILE_SIZE, const.TILE_SIZE))

class Maze(pygame.sprite.Sprite):
    def __init__(self):
        super(Maze, self).__init__()
        # Grid
        self.COLS = const.WIDTH // const.TILE_SIZE
        self.ROWS = const.HEIGHT // const.TILE_SIZE

        # Maze
        self.maze = []

        # Enemies
        self.enemies = pygame.sprite.Group()
        self.current_enemy = None

    def create_maze(self):
        """
            Generate maze using recursive backtracking.
        """
        # Init with walls
        self.maze = [[1 for _ in range(self.COLS)] for _ in range(self.ROWS)]  # 1 = Wall, 0 = Path

        # Generate maze
        def carve(x, y):
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.ROWS - 1 and 0 < ny < self.COLS - 1 and self.maze[nx][ny] == 1:
                    # Create Path
                    self.maze[nx][ny] = 0
                    self.maze[x + dx // 2][y + dy // 2] = 0  # Open middle cell
                    carve(nx, ny)

        start_x, start_y = 1, 1
        self.maze[start_x][start_y] = 0 # Start on path
        carve(start_x, start_y)

        # Define door next level
        valid_positions = [(row, col) for row in range(1, self.ROWS - 1, 2) for col in range(1, self.COLS - 1, 2)]
        random.shuffle(valid_positions)

        for door_x, door_y in valid_positions:
            if self.maze[door_x][door_y] == 0: 
                self.maze[door_x][door_y] = 2  # 2 = Door
                break

        # Create Enemies
        num_enemies = const.ENEMIES_ON_MAZE
        for _ in range(num_enemies):
            enemy = Enemy(self)
            self.enemies.add(enemy)

        print('Maze Created')


    def draw_maze(self, screen, player_pos, player):
        # Draw Maze
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x, y = col * const.TILE_SIZE, row * const.TILE_SIZE
                if self.maze[row][col] == 1:
                    screen.blit(wall_img, (x, y))
                elif self.maze[row][col] == 0:
                    screen.blit(path_img, (x, y))
                elif self.maze[row][col] == 2:
                    screen.blit(door_img, (x, y))

        # Draw player
        player.draw(screen)

        # Draw Enemies
        for enemy in self.enemies:
            enemy.draw(screen)