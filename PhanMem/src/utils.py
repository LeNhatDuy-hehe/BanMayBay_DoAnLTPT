import pygame, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, "assets")

def load_image(path):
    return pygame.image.load(os.path.join(ASSET_DIR, path)).convert_alpha()

def load_sound(path):
    return pygame.mixer.Sound(os.path.join(ASSET_DIR, path))

def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    """Render text to a surface at position (x, y)."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Backward-compatible Vietnamese alias
def ve_text(surface, text, size, x, y, color=(255,255,255)):
    return draw_text(surface, text, size, x, y, color)
