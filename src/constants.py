from pygame import time
from pygame import USEREVENT
from pygame.font import Font
from pygame.mixer import Sound
import pygame

# Initialize pygame
pygame.init()

# Clock
CLOCK = time.Clock()

# Custom events
HIT_WALL = USEREVENT + 1

# Window dimensions
WIDTH = 1080
HEIGHT = 720

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 110

# Space between Paddle and wall
MARGIN = 10

# Score Font
FONT_SIZE = 30
FONT = Font("assets/font/bit5x3.ttf", FONT_SIZE)

# Sounds
SCORE_SOUND = Sound("assets/music/sfx/score.ogg")
PADDLE_SOUND = Sound("assets/music/sfx/pong.ogg")

# Create rect objs for scores
PLAYER_SCORE_RECT = pygame.Rect(0, 0, 70, 30)
OPPONENT_SCORE_RECT = pygame.Rect(0, 0, 70, 30)

# Set rect coords to desired locations
PLAYER_SCORE_RECT.right = WIDTH // 2 - 1
OPPONENT_SCORE_RECT.left = WIDTH // 2 + 2

# Ball image
BALL_IMG = pygame.image.load("assets/img/Ball.png")
