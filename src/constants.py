from pygame import time
from pygame import USEREVENT

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
