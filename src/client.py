import sys
import pygame
from random import choice
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
    opponent = client.receive()

    # Return the opponent if it is a Player obj
    if isinstance(opponent, Player):
        return opponent


def main():
    """The game loop"""

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
                ball.x_velocity = -1 if ball.centerx > WIDTH // 2 else 1
                ball.centerx, ball.centery = WIDTH // 2, HEIGHT // 2
                ball.x_velocity *= 6

        # Set black background and draw a line in the center
        WIN.fill("black")
        pygame.draw.aaline(WIN, "white", (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Control the paddle
        keys = pygame.key.get_pressed()
        player.move_paddle(keys)

        # Raise HIT_WALL event if x_velocity is 0
        if ball.x_velocity == 0:
            pygame.event.post(pygame.event.Event(HIT_WALL))

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
