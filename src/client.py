import sys
import pygame
from classes import Network, Player, Ball
from constants import (WIDTH, HEIGHT, CLOCK, MARGIN,
                       PADDLE_WIDTH, PADDLE_HEIGHT,
                       HIT_WALL)

# Initialize
pygame.init()

# Set up the main window (surface)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG - MULTIPLAYER")

# Connect to the server
client = Network(server=False)
client.send("!get")
player: Player = client.receive()

# Create pygame.Rect obj (Paddle) for the player
player.paddle = pygame.Rect(MARGIN, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
player.paddle.centery = HEIGHT // 2

# Create a Ball obj
ball = Ball(0, 0, 20, 20)
ball.centerx = WIDTH // 2
ball.centery = HEIGHT // 2


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

    time_when_hit = 0
    ball_xdir = 0
    ball_dir_reversed = False
    while True:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Move ball to center if it has hit left or right wall
            # If it has hit the right wall, set x_velocity to -1
            # otherwise, set it to 1
            if event.type == HIT_WALL:
                ball_xdir = -1 if ball.centerx > WIDTH // 2 else 1
                ball.centerx, ball.centery = WIDTH // 2, HEIGHT // 2
                player.paddle.centery = HEIGHT // 2

        # Set black background and draw a line in the center
        WIN.fill("black")
        pygame.draw.aaline(WIN, "white", (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

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
            ball.x_velocity = ball_xdir * 6
            ball.y_velocity = ball_xdir * 6
            ball_xdir = 0
            time_when_hit = 0

        # Check for collision with paddle
        if ball.colliderect(player.paddle):
            ball.x_velocity *= -1

        # Get opponent (Player obj) from the server
        opponent = get_opponent(player)

        # Draw opponent's paddle on the right side if
        # the two players are different Player objs
        if opponent and opponent.paddle and opponent != player:
            opponent.paddle.right = WIDTH - MARGIN
            pygame.draw.rect(WIN, "white", opponent.paddle)

            # Set ball direction for player
            if player.id < opponent.id and not ball_dir_reversed:
                ball.x_velocity *= -1
                ball_dir_reversed = True

            # Animate the ball and check for collisions
            ball.animate()

        # Otherwise draw a new pygame.Rect obj on the right side
        # and place the ball at the center
        else:
            pygame.draw.rect(WIN, "white",
                             pygame.Rect(WIDTH - (PADDLE_WIDTH + MARGIN),
                                         HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                         PADDLE_WIDTH,
                                         PADDLE_HEIGHT))

            ball.centerx, ball.centery = WIDTH // 2, HEIGHT // 2

        # Draw player's paddle and ball
        pygame.draw.rect(WIN, "white", player.paddle)
        pygame.draw.ellipse(WIN, "white", ball)

        # Update the display (60 times/s)
        pygame.display.update()
        CLOCK.tick(60)


if __name__ == "__main__":
    main()
