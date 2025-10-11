import pygame
from utils import load_image, load_sound

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load và scale ảnh đạn
        self.image = load_image("image/bullet/normal_bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 25))  # đạn nhỏ gọn
        
        # Vị trí xuất phát từ player
        self.rect = self.image.get_rect(center=(x, y))
        
        # Tốc độ bay
        self.speed = -10  # bay nhanh hơn
        
        # Âm thanh bắn
        self.sound = load_sound("sound/Shot/Laser Shot.wav")
        self.sound.set_volume(0.3)  # chỉnh nhỏ âm lượng
        self.sound.play()

    def update(self):
        # Đạn bay thẳng lên
        self.rect.y += self.speed
        
        # Nếu bay ra ngoài màn hình thì xóa
        if self.rect.bottom < 0:
            self.kill()
