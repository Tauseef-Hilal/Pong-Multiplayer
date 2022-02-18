import sys
import pygame
from classes import (Network,
                     Player,
                     Ball)

# Initialize
pygame.init()

# Set up the main window (surface)
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Set up FPS clock
clock = pygame.time.Clock()

# Connect to the server
client = Network(server=False)
client.send("!get")
player: Player = client.receive()

# Create pygame.Rect obj (Paddle) for the player
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
player.paddle = pygame.Rect(0, 260, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create a Ball obj
ball = Ball(0, 0, 20, 20)
ball.centerx = 400
ball.centery = 300


def get_opponent(player):
    # Send player to the server
    client.send(player)

    # Try to get opponent (Player obj) from the server
    opponent = client.receive()

    # Return the opponent if it is a Player obj
    if isinstance(opponent, Player):
        return opponent


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Set black background and draw a line in the center
    WIN.fill("black")
    pygame.draw.line(WIN, "white", (400, 0), (400, HEIGHT))

    # Control the paddle
    keys = pygame.key.get_pressed()
    player.move_paddle(keys)

    # Animate the ball and check for collisions
    ball.animate()

    if ball.colliderect(player.paddle):
        ball.x = -ball.x_velocity

    # Get opponent (Player obj) from the server
    opponent = get_opponent(player)

    # Check if it is another player
    if opponent and opponent.paddle and opponent != player:
        # Draw opponent's paddle on the right side
        opponent.paddle.right = WIDTH
        pygame.draw.rect(WIN, "white", opponent.paddle)
    else:
        # Otherwise draw a new pygame.Rect obj on the right side
        pygame.draw.rect(WIN, "white", pygame.Rect(790, 260,
                                                   PADDLE_WIDTH,
                                                   PADDLE_HEIGHT))

    # Draw player's paddle and ball
    pygame.draw.rect(WIN, "white", player.paddle)
    pygame.draw.rect(WIN, "white", ball, border_radius=20)

    # Update the display (60 times/s)
    pygame.display.update()
    clock.tick(60)
