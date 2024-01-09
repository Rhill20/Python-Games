import pygame
import sys
import random
# Initialize 
pygame.init()
# Constants
WIDTH, HEIGHT = 600, 400
BALL_SPEED = 6
PADDLE_SPEED = 8
AI_PADDLE_SPEED = 5
PLAYER_SCORE_POS = (50, 20)
AI_SCORE_POS = (WIDTH - 80, 20)
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle properties
paddle_width, paddle_height = 15, 60
player_paddle = pygame.Rect(50, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ai_paddle = pygame.Rect(WIDTH - 50 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball properties
ball_size = 20
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
ball_direction = [random.choice([-1, 1]), random.uniform(-1, 1)]  # [x_direction, y_direction]

# Score Board 
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 36)

# Game loop
game_active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_active = True

    if game_active:
        # User Paddle Movment 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_paddle.top > 0:
            player_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
            player_paddle.y += PADDLE_SPEED

        # AI Paddle Tracking
        if ai_paddle.centery < ball.centery:
            ai_paddle.y += AI_PADDLE_SPEED
        elif ai_paddle.centery > ball.centery:
            ai_paddle.y -= AI_PADDLE_SPEED

        # Ball Movment 
        ball.x += BALL_SPEED * ball_direction[0]
        ball.y += BALL_SPEED * ball_direction[1]

        # Ball collision with paddles
        if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
            ball_direction[0] *= -1

            # Change ball's vertical direction based on where it hits the paddle
            paddle_center = player_paddle.centery if ball_direction[0] > 0 else ai_paddle.centery
            ball_relative_pos = (ball.centery - paddle_center) / (paddle_height / 2)

            # Ensure the vertical direction is always either positive or negative
            ball_direction[1] = random.choice([-1, 1]) if ball_relative_pos == 0 else ball_relative_pos

        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_direction[1] *= -1

        # Wall Collision loss LEFT
        if ball.left <= 0:
            ai_score += 1
            game_active = False
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2

        # Wall Collision Loss Right 
        if ball.right >= WIDTH:
            player_score += 1
            game_active = False
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, RED, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw scores
    player_text = font.render(str(player_score), True, WHITE)
    ai_text = font.render(str(ai_score), True, RED)
    screen.blit(player_text, PLAYER_SCORE_POS)
    screen.blit(ai_text, AI_SCORE_POS)

    # Start
    if not game_active:
        start_text = font.render("Press SPACE to start", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(start_text, start_rect)

    # Display
    pygame.display.flip()

    # frame rate
    pygame.time.Clock().tick(60)
