import sys
import pygame
from classes import (Network,
                     Player)


pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

c = Network(server=False)
c.send("!get")
player = c.receive()

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
player.paddle = pygame.Rect(0, 260, PADDLE_WIDTH, PADDLE_HEIGHT)
# right_paddle = pygame.Rect(WIDTH - PADDLE_WIDTH, 0, PADDLE_WIDTH, 80)

# player.paddle.centery = 300
# right_paddle.centery = 300

ball = pygame.Rect(0, 0, 20, 20)
ball.centerx = 400
ball.centery = 300


ball_x = 6
ball_y = 6


def handle_client(player):
    c.send(player)
    opponent = c.receive()

    if isinstance(opponent, Player):
        return opponent


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    WIN.fill("black")
    pygame.draw.line(WIN, "white", (400, 0), (400, HEIGHT))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.paddle.top > 0:
        player.paddle.y -= 6
    elif keys[pygame.K_s] and player.paddle.bottom < HEIGHT:
        player.paddle.y += 6

    if ball.left <= 0 or ball.right >= WIDTH or \
            ball.colliderect(player.paddle):
        ball_x = -ball_x
    ball.x += ball_x

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_y = -ball_y
    ball.y += ball_y

    opponent = handle_client(player)
    if opponent and opponent.paddle and opponent != player:
        opponent.paddle.right = WIDTH
        pygame.draw.rect(WIN, "white", opponent.paddle)
    else:
        pygame.draw.rect(WIN, "white", pygame.Rect(790, 260,
                                                   PADDLE_WIDTH,
                                                   PADDLE_HEIGHT))
    pygame.draw.rect(WIN, "white", player.paddle)
    pygame.draw.rect(WIN, "white", ball, border_radius=20)

    pygame.display.update()
    clock.tick(60)
