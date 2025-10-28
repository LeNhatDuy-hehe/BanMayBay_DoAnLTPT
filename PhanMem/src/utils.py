import pygame, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, "assets")

def load_image(path):
    """Tải hình ảnh từ assets, chuyển đổi định dạng để hỗ trợ trong suốt.
    Tham số: path (str): Đường dẫn tương đối tới tệp hình ảnh trong thư mục 'assets'.
    Trả về:pygame.Surface: Đối tượng hình ảnh đã được tải và chuyển đổi."""
    return pygame.image.load(os.path.join(ASSET_DIR, path)).convert_alpha()

def load_sound(path):
    """Tải âm thanh từ assets.
    Tham số:path (str): Đường dẫn tương đối tới tệp âm thanh trong thư mục 'assets'.
    Trả về:pygame.mixer.Sound: Đối tượng âm thanh có thể phát được trong pygame."""
    return pygame.mixer.Sound(os.path.join(ASSET_DIR, path))

def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    """Vẽ chuỗi văn bản lên vị trí chỉ định.
    Tham số: surface (pygame.Surface): Bề mặt nơi sẽ hiển thị văn bản.
        text (str): Chuỗi văn bản cần hiển thị.
        size (int): Kích thước phông chữ (đơn vị pixel).
        x (int): Tọa độ X (theo pixel) trên bề mặt.
        y (int): Tọa độ Y (theo pixel) trên bề mặt.
        color (tuple[int, int, int], mặc định=(255, 255, 255)): Màu của văn bản (định dạng RGB).
    Chức năng:khởi tạo một phông chữ mặc định, kết xuất văn bản thành hình ảnh, vẽ lên bề mặt tại tọa độ (x, y)."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Backward-compatible Vietnamese alias
def ve_text(surface, text, size, x, y, color=(255,255,255)):
    """ Hàm tương thích ngược bằng tiếng Việt)
    Vẽ văn bản lên màn hình tại vị trí (x, y).
    Tham số giống với hàm draw_text()."""
    return draw_text(surface, text, size, x, y, color)
