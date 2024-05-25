import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

pygame.init()

# Define some colors
WHITE = (255, 255, 255)
DARKBLUE = (36, 90, 190)
LIGHTBLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK = (0, 0, 0)

score = 0
lives = 3

# Open a new window
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Create the Paddle
paddle = Paddle(GRAY, 100, 20)
paddle.rect.x = 350
paddle.rect.y = 560

# Create the ball sprite
ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

all_bricks = pygame.sprite.Group()
for i in range(7):
    brick = Brick(RED, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(ORANGE, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

# Add the paddle and the ball to the list of sprites
all_sprites_list.add(paddle)
all_sprites_list.add(ball)


carryOn = True
clock = pygame.time.Clock()

# Function to reset the ball and paddle position
def reset_ball_and_paddle():
    ball.rect.x = 345
    ball.rect.y = 195
    ball.velocity = [4, -4]
    paddle.rect.x = 350
    paddle.rect.y = 560
    pygame.time.wait(1000)  # Wait 1 second before resuming

# Function to display message
def display_message(message, duration=3000):
    font = pygame.font.Font(None, 74)
    text = font.render(message, 1, WHITE)
    # Center the message on the screen
    text_rect = text.get_rect(center=(size[0]/2, size[1]/2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(duration)

while carryOn:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            carryOn = False 

    # Moving the paddle when the use uses the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(5)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(5)

    all_sprites_list.update()

    # Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x >= 790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 590:
        ball.velocity[1] = -ball.velocity[1]
        lives -= 1
        if lives > 0:
            display_message("TRY AGAIN")
            reset_ball_and_paddle()  # Reset ball and paddle positions instead of reducing lives
        else:
            display_message("GAME OVER")
            carryOn = False  # Stop the game

    if ball.rect.y < 40:
        ball.velocity[1] = -ball.velocity[1]

    # Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
        ball.rect.x -= ball.velocity[0]
        ball.rect.y -= ball.velocity[1]
        ball.bounce()

    # Check if there is the ball collides with any of bricks
    brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
    for brick in brick_collision_list:
        ball.bounce()
        score += 1
        brick.kill()
        if len(all_bricks) == 0:
            # Display Level Complete Message for 3 seconds
            display_message("LEVEL COMPLETE")
            carryOn = False  # Stop the Game

    # First, clear the screen to dark blue.
    screen.fill(DARK)
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

    # Display the score and the number of lives at the top of the screen
    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(score), 1, WHITE)
    screen.blit(text, (20, 10))
    text = font.render("Lives: " + str(lives), 1, WHITE)
    screen.blit(text, (650, 10))

    all_sprites_list.draw(screen)

    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
