import pygame
import sys
import random

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors and game constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15

# Paddle positions
player_x = 20
player_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

opponent_x = WIDTH - 20 - PADDLE_WIDTH
opponent_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

# Ball position and speed
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = random.choice([-4, 4])
ball_speed_y = random.choice([-4, 4])

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player paddle movement using W and S keys
    # This will be changed in the future to use a players brainwaves!
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_y > 0:
        player_y -= 5
    if keys[pygame.K_s] and player_y < HEIGHT - PADDLE_HEIGHT:
        player_y += 5

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision with top and bottom walls
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_speed_y *= -1

    # Collision with player paddle
    if (ball_x <= player_x + PADDLE_WIDTH and
        player_y < ball_y + BALL_SIZE and
        player_y + PADDLE_HEIGHT > ball_y):
        ball_speed_x *= -1

    # Collision with opponent paddle
    if (ball_x + BALL_SIZE >= opponent_x and
        opponent_y < ball_y + BALL_SIZE and
        opponent_y + PADDLE_HEIGHT > ball_y):
        ball_speed_x *= -1

    # Basic opponent AI: follow the ball
    if opponent_y + PADDLE_HEIGHT / 2 < ball_y:
        opponent_y += 3
    elif opponent_y + PADDLE_HEIGHT / 2 > ball_y:
        opponent_y -= 3

    # Check if ball goes off the screen
    if ball_x < 0 or ball_x > WIDTH:
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_speed_x = random.choice([-4, 4])
        ball_speed_y = random.choice([-4, 4])

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (player_x, player_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (opponent_x, opponent_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
