import pygame, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, "assets")

def load_image(path):
    """Tải hình ảnh từ assets, chuyển đổi định dạng để hỗ trợ trong suốt.
    Tham số: path (str) tương đối tới tệp hình ảnh trong thư mục 'assets'."""
    return pygame.image.load(os.path.join(ASSET_DIR, path)).convert_alpha()

def load_sound(path):
    """Tải âm thanh từ assets."""
    return pygame.mixer.Sound(os.path.join(ASSET_DIR, path))

def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    """Vẽ chuỗi văn bản lên vị trí chỉ định."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

