from pygame import time
from pygame import USEREVENT
from pygame.font import SysFont
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
PADDLE_HEIGHT = 100

# Space between Paddle and wall
MARGIN = 10

# Score Font
FONT_SIZE = 30
FONT = SysFont("", FONT_SIZE)

# Sounds
SCORE_SOUND = Sound("assets/music/sfx/score.ogg")
PADDLE_SOUND = Sound("assets/music/sfx/pong.ogg")
