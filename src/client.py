import sys
import pygame
from random import randint
from classes import Network, Player, Ball
from constants import (WIDTH, HEIGHT, CLOCK, MARGIN, PADDLE_WIDTH,
                       PADDLE_HEIGHT, HIT_WALL, FONT, SCORE_SOUND,
                       PADDLE_SOUND, PLAYER_SCORE_RECT, BALL_IMG,
                       OPPONENT_SCORE_RECT)

# Set up the main window (surface)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG - MULTIPLAYER")

# Connect to the server
client = Network(server=False)
client.send("!get")
player: Player = client.receive()

# Create pygame.Rect obj (Paddle) for the player
player.paddle = pygame.Rect(MARGIN, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
player.paddle.left = MARGIN
player.paddle.centery = HEIGHT // 2

# Create a Ball obj
ball = Ball.from_img(BALL_IMG)
ball.centerx = WIDTH // 2
ball.centery = HEIGHT // 2

# Music (~ Different for each player)
pygame.mixer.music.load(f"assets/music/Stage-{randint(1, 3)}.ogg")

def display_score(player, opponent=None):
    """Display players' scores"""

    # Create Surfaces for scores
    PLAYER_SCORE = FONT.render(f"{player.score}", True, "black")
    OPPONENT_SCORE = FONT.render(f"{opponent.score if opponent else 0}",
                                 True, "black")

    # Draw the recangles
    pygame.draw.rect(WIN, "lightsteelblue", PLAYER_SCORE_RECT)
    pygame.draw.rect(WIN, "lightsteelblue", OPPONENT_SCORE_RECT)

    # Draw scores on top of the rectangles
    temp = PLAYER_SCORE.get_rect()
    temp.center = PLAYER_SCORE_RECT.center
    WIN.blit(PLAYER_SCORE, temp)

    temp = OPPONENT_SCORE.get_rect()
    temp.center = OPPONENT_SCORE_RECT.center
    WIN.blit(OPPONENT_SCORE, temp)


def get_opponent(player):
    """Get opponent Player obj from the server"""
    # Send player to the server
    client.send(player)

    # Try to get opponent (Player obj) from the server
    try:
        opponent = client.receive()
    except (EOFError, ConnectionResetError):
        print("[ERROR] Server Down.")
        client.socket.close()
        sys.exit()

    # Return the opponent if it is a Player obj
    if isinstance(opponent, Player):
        return opponent


def main():
    """The game loop"""

    ball_xdir = 0
    ball_ydir = 0
    time_when_hit = 0
    ball_dir_reversed = False

    # Play music
    pygame.mixer.music.play(-1, 0, 2000)

    while True:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle ball and wall collision
            # Update players' scores
            if event.type == HIT_WALL:
                # Set x_dir for ball and update players' scores
                if ball.centerx > WIDTH // 2:
                    ball_xdir = -1
                    player.score += 1
                else:
                    ball_xdir = 1

                ball_ydir = -1 if ball.centery > HEIGHT // 2 else 1
                ball.centerx, ball.centery = WIDTH // 2, HEIGHT // 2
                player.paddle.centery = HEIGHT // 2

                # Play score sound
                SCORE_SOUND.play()

        # Set up background
        WIN.fill("grey5")
        pygame.draw.aaline(WIN, "lightsteelblue2",
                           (WIDTH // 2, 0),
                           (WIDTH // 2, HEIGHT))

        # Control the paddle
        keys = pygame.key.get_pressed()
        player.move_paddle(keys)

        # Raise HIT_WALL event if x_velocity and ball_xdir both are 0
        if ball.x_velocity == ball_xdir == 0:
            time_when_hit = pygame.time.get_ticks()
            pygame.event.post(pygame.event.Event(HIT_WALL))

        # 1000ms after HIT_WALL
        if pygame.time.get_ticks() - time_when_hit >= 1000 \
                and ball.x_velocity == 0:
            ball.x_velocity = ball_xdir * 7
            ball.y_velocity = ball_ydir * 7
            ball_xdir = 0
            time_when_hit = 0

        # Get opponent (Player obj) from the server
        opponent = get_opponent(player)

        # Draw opponent's paddle on the right side if
        # the two players are different Player objs
        if opponent and opponent.paddle and opponent != player:
            opponent.paddle.right = WIDTH - MARGIN
            pygame.draw.rect(WIN, "lightsteelblue2", opponent.paddle)

            # Set ball direction for player
            if player.id < opponent.id and not ball_dir_reversed:
                ball.x_velocity *= -1
            ball_dir_reversed = True

            # Animate the ball and check for collisions
            ball.animate()
            if ball.collidelist([player.paddle, opponent.paddle]) != -1:
                ball.x_velocity *= -1
                PADDLE_SOUND.play()

        # Otherwise draw a new pygame.Rect obj on the right side
        # and place the ball at the center
        else:
            pygame.draw.rect(WIN, "lightsteelblue2",
                             pygame.Rect(WIDTH - (PADDLE_WIDTH + MARGIN),
                                         HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                         PADDLE_WIDTH,
                                         PADDLE_HEIGHT))

            ball.centerx, ball.centery = WIDTH // 2, HEIGHT // 2

            # If ball_dir_reversed is True, then one of the players
            # has quit the game and the state needs to be reset
            if ball_dir_reversed:
                player.score = 0
                ball.x_velocity = 7
                ball.y_velocity = 7
                ball_dir_reversed = False

        # Display score
        display_score(player, opponent)

        # Draw player's paddle and ball
        pygame.draw.rect(WIN, "lightsteelblue2", player.paddle)
        WIN.blit(BALL_IMG, ball)
        # pygame.draw.ellipse(WIN, "white", ball)

        # Update the display (60 times/s)
        pygame.display.update()
        CLOCK.tick(60)


if __name__ == "__main__":
    main()
