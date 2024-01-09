import pygame
import random

pygame.init()

# game constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
BROWN = (139, 69, 19)

# game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.size = 1
        self.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.direction = "RIGHT"
        self.body = [(self.x, self.y)]

    def move(self):
        if self.direction == "UP":
            self.y -= GRID_SIZE
        elif self.direction == "DOWN":
            self.y += GRID_SIZE
        elif self.direction == "LEFT":
            self.x -= GRID_SIZE
        elif self.direction == "RIGHT":
            self.x += GRID_SIZE

        # Add current position to the body
        self.body.append((self.x, self.y))

        # Remove the tail if the snake hasn't grown
        if len(self.body) > self.size:
            del self.body[0]

    def draw(self):
        for i, segment in enumerate(self.body):
            pygame.draw.circle(screen, GREEN,
                               (segment[0] + GRID_SIZE // 2, segment[1] + GRID_SIZE // 2), GRID_SIZE // 2)


class Food:
    def __init__(self):
        self.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, GRID_SIZE, GRID_SIZE))
        pygame.draw.circle(screen, BROWN,
                           (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 3)


snake = None
food = None
game_started = False
game_over = False


def start_game():
    global snake, food, game_started, game_over

    snake = Snake()
    food = Food()
    game_started = True
    game_over = False


def end_game():
    global game_over
    game_over = True


def show_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)


def show_start_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Start", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    button_rect = text_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, button_rect, 3)
    screen.blit(text, text_rect)
    return button_rect


def show_retry_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Retry", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    button_rect = text_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, button_rect, 3)
    screen.blit(text, text_rect)
    return button_rect


running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if not game_started:
                start_button_rect = show_start_button()
                if start_button_rect.collidepoint(mouse_pos):
                    start_game()
            elif game_over:
                retry_button_rect = show_retry_button()
                if retry_button_rect.collidepoint(mouse_pos):
                    start_game()
        elif event.type == pygame.KEYDOWN:
            if game_started and not game_over:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

    # game logic
    if game_started and not game_over:
        snake.move()

        # snake hits the borders
        if (
            snake.x < 0
            or snake.x >= WIDTH
            or snake.y < 0
            or snake.y >= HEIGHT
            or snake.body.count((snake.x, snake.y)) > 1
        ):
            end_game()

        # Check eats food
        if snake.x == food.x and snake.y == food.y:
            snake.size += 5
            food = Food()

 
    screen.fill(BLACK)

    # Draw  snake
    if game_started:
        snake.draw()

    # Draw the food
    if game_started:
        food.draw()

    # Show messages and buttons
    if not game_started:
        show_message("Click 'Start' to begin")
    elif game_over:
        show_message("You died. Click 'Retry' to play again")
        show_retry_button()
    else:
        pass

    # Update  display
    pygame.display.flip()

    # frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
