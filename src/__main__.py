import sys
import pygame
import socket

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(("", 5050))

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

PADDLE_WIDTH = 10
left_paddle = pygame.Rect(0, 0, PADDLE_WIDTH, 80)
right_paddle = pygame.Rect(WIDTH - PADDLE_WIDTH, 0, PADDLE_WIDTH, 80)

left_paddle.centery = 300
right_paddle.centery = 300

ball = pygame.Rect(0, 0, 20, 20)
ball.centerx = 400
ball.centery = 300


ball_x = 6
ball_y = 6


def handle_client(paddle):
    c.send(f"{paddle.y}".encode("utf-8"))
    opponent_y = c.recv(1024)

    if opponent_y:
        return int(opponent_y.decode("utf-8"))
    return 260


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    WIN.fill("black")
    pygame.draw.line(WIN, "white", (400, 0), (400, HEIGHT))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= 6
    elif keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += 6

    y = handle_client(left_paddle)
    right_paddle.y = y

    if ball.left <= 0 or ball.right >= WIDTH or \
            ball.colliderect(left_paddle) or \
            ball.colliderect(right_paddle):
        ball_x = -ball_x
    ball.x += ball_x

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_y = -ball_y
    ball.y += ball_y

    pygame.draw.rect(WIN, "white", left_paddle)
    pygame.draw.rect(WIN, "white", right_paddle)
    pygame.draw.rect(WIN, "white", ball, border_radius=20)

    pygame.display.update()
    clock.tick(60)
