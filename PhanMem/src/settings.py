"""
Game settings. Migrated to English names with backward-compatible Vietnamese aliases.

English exports (preferred):
- SCREEN_WIDTH, SCREEN_HEIGHT, FPS
- PLAYER_SIZE, ENEMY_SIZE
- WHITE, RED, BLACK

Vietnamese aliases are kept for existing code:
- rong -> SCREEN_WIDTH, cao -> SCREEN_HEIGHT
- TRANG -> WHITE, DO -> RED, DEN -> BLACK
"""

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60  # frames per second

# Entity sizes (width, height)
PLAYER_SIZE = (50, 50)
ENEMY_SIZE = (40, 40)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# --- Backward compatibility aliases (Vietnamese) ---
rong = SCREEN_WIDTH   # chiều rộng màn hình
cao = SCREEN_HEIGHT   # chiều cao màn hình
TRANG = WHITE
DO = RED
DEN = BLACK
