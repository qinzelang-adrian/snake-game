"""贪吃蛇游戏 - 使用 pygame"""

import pygame
import random
from enum import Enum

pygame.init()

# ============ 常量定义 ============
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SNAKE_HEAD_COLOR = (0, 200, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

SPEED = 10


# ============ 方向枚举 ============
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


# ============ 贪吃蛇类 ============
class Snake:
    def __init__(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT

    def update(self):
        """更新蛇的位置，返回被移除的尾部节点"""
        self.direction = self.next_direction

        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        return self.body.pop()

    def grow(self, removed_tail):
        """蛇吃到食物时增长：把移除的尾部加回来"""
        self.body.append(removed_tail)

    def change_direction(self, direction):
        """改变蛇的方向（防止向后转）"""
        dx, dy = direction.value
        if (-dx, -dy) != self.next_direction.value:
            self.next_direction = direction

    def check_collision_with_self(self):
        """检查蛇是否与自己碰撞"""
        return self.body[0] in self.body[1:]

    def check_boundary_collision(self):
        """检查蛇是否与边界碰撞"""
        head_x, head_y = self.body[0]
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT

    def draw(self, screen):
        """绘制蛇"""
        for i, (x, y) in enumerate(self.body):
            color = SNAKE_HEAD_COLOR if i == 0 else GREEN
            pygame.draw.rect(screen, color,
                             (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2))


# ============ 食物类 ============
class Food:
    def __init__(self, snake_body=None):
        self.spawn(snake_body)

    def spawn(self, snake_body=None):
        """生成食物，确保不与蛇重叠"""
        if snake_body:
            snake_set = set(snake_body)
            free_cells = [
                (x, y)
                for x in range(GRID_WIDTH)
                for y in range(GRID_HEIGHT)
                if (x, y) not in snake_set
            ]
            if free_cells:
                self.x, self.y = random.choice(free_cells)
            return
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)

    def draw(self, screen):
        """绘制食物"""
        pygame.draw.rect(screen, RED,
                         (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2))


# ============ 游戏类 ============
class Game:
    _KEY_MAP = {
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
    }

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("贪吃蛇游戏")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('simhei,microsoftyahei,arial', 36)
        self.reset_game()

    def reset_game(self):
        """重置游戏"""
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                direction = self._KEY_MAP.get(event.key)
                if direction:
                    self.snake.change_direction(direction)
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        return True

    def update(self):
        """更新游戏逻辑"""
        if self.game_over:
            return

        removed_tail = self.snake.update()

        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow(removed_tail)
            self.food.spawn(self.snake.body)
            self.score += 10

        if self.snake.check_collision_with_self() or self.snake.check_boundary_collision():
            self.game_over = True

    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)

        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y), 1)

        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        score_text = self.font.render(f"得分: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render("游戏结束！按空格重新开始", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        """游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(SPEED)
        pygame.quit()


# ============ 主程序 ============
if __name__ == "__main__":
    game = Game()
    game.run()
