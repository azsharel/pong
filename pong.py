import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pong Game")

# Set up the paddles
paddle_width = 10
paddle_height = 60
paddle_speed = 3

left_paddle_x = 50
left_paddle_y = (window_height - paddle_height) // 2

right_paddle_x = window_width - paddle_width - 50
right_paddle_y = (window_height - paddle_height) // 2

# Set up the AI paddle
ai_paddle_speed = 3
ai_paddle_x = window_width - paddle_width - 50
ai_paddle_y = (window_height - paddle_height) // 2


# Set up the scores
left_score = 0
right_score = 0
font = pygame.font.Font(None, 36)

# Set up the ball
ball_radius = 5
ball_speed_x = 3
ball_speed_y = 3

ball_x = window_width // 2
ball_y = window_height // 2


def reset_game():
    global left_score, right_score, ball_x, ball_y, ball_speed_x, ball_speed_y, left_paddle_y, ai_paddle_y
    left_score = right_score = 0
    ball_x = window_width // 2
    ball_y = window_height // 2
    ball_speed_x = ball_speed_y = 3
    left_paddle_y = ai_paddle_y = (window_height - paddle_height) // 2


def show_score():
    score_surface = font.render(f"Player: {left_score} AI: {right_score}", True, (255, 255, 255))
    window.blit(score_surface, (window_width // 2 - score_surface.get_width() // 2, 10))


def game_over_screen(win=False):
    window.fill((0, 0, 0))
    if win:
        game_over_surface = font.render("Thanks for playing, a game by - Joshua Bradley", True, (255, 255, 255))
    else:
        game_over_surface = font.render("Game Over! AI wins.", True, (255, 255, 255))

    window.blit(game_over_surface, (window_width // 2 - game_over_surface.get_width() // 2, window_height // 2))

    play_again_surface = font.render("Press Y to play again, N to quit.", True, (255, 255, 255))
    window.blit(play_again_surface, (window_width // 2 - play_again_surface.get_width() // 2, window_height // 2 + 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    reset_game()
                    return
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def score_point():
    global left_score, right_score, ball_x, ball_y, ball_speed_x, ball_speed_y

    if ball_x - ball_radius <= 0:
        right_score += 1
        ball_x = window_width // 2
        ball_y = window_height // 2
        ball_speed_x = ball_speed_y = 3
        if right_score == 5:  # AI wins
            game_over_screen(win=False)
    elif ball_x + ball_radius >= window_width:
        left_score += 1
        ball_x = window_width // 2
        ball_y = window_height // 2
        ball_speed_x = ball_speed_y = 3
        if left_score == 5:  # Player wins
            game_over_screen(win=True)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Handle keyboard input for the player paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < window_height - paddle_height:
        left_paddle_y += paddle_speed

    # Handle collisions with walls
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= window_height:
        ball_speed_y *= -1

    # Handle collisions with paddles
    if (ball_x - ball_radius <= left_paddle_x + paddle_width and
            left_paddle_y <= ball_y <= left_paddle_y + paddle_height):
        ball_speed_x *= -1
        ball_speed_x += 1 if ball_speed_x > 0 else -1
        ball_speed_y += 1 if ball_speed_y > 0 else -1
    elif (ball_x + ball_radius >= ai_paddle_x and
          ai_paddle_y <= ball_y <= ai_paddle_y + paddle_height):
        ball_speed_x *= -1
        ball_speed_x += 1 if ball_speed_x > 0 else -1
        ball_speed_y += 1 if ball_speed_y > 0 else -1

    # Handle scoring
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= window_width:
        score_point()

    # AI paddle movement
    if ball_y < ai_paddle_y + paddle_height // 2 and ai_paddle_y > 0:
        ai_paddle_y -= ai_paddle_speed
    if ball_y > ai_paddle_y + paddle_height // 2 and ai_paddle_y < window_height - paddle_height:
        ai_paddle_y += ai_paddle_speed

    # Update the screen
    window.fill((0, 0, 0))  # Fill the window with black color

    # Draw the paddles, ball, and show the score
    pygame.draw.rect(window, (255, 255, 255), (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(window, (255, 255, 255), (ai_paddle_x, ai_paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(window, (255, 255, 255), (ball_x, ball_y), ball_radius)
    show_score()

    pygame.display.flip()  # Update the display

    # Limit the frame rate
    pygame.time.Clock().tick(60)