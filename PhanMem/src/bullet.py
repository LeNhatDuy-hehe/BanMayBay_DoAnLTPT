import pygame
from utils import load_image, load_sound

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, damage=10):  # thêm damage mặc định
        super().__init__()
        # Load và scale ảnh đạn
        self.image = load_image("image/bullet/normal_bullet.png")
        self.image = pygame.transform.scale(self.image, (8, 20))  # đạn nhỏ hơn chút
        
        # Vị trí xuất phát từ player
        self.rect = self.image.get_rect(center=(x, y))
        
        # Tốc độ bay
        self.speed = -12  # bay nhanh hơn
        
        # Sát thương gây ra
        self.damage = damage  # <== thêm dòng này
        
        # Âm thanh bắn
        self.sound = load_sound("sound/Shot/Laser Shot.wav")
        self.sound.set_volume(0.25)  # âm nhỏ hơn chút để dễ nghe
        self.sound.play()

    def update(self):
        # Đạn bay thẳng lên
        self.rect.y += self.speed
        
        # Nếu bay ra ngoài màn hình thì xóa
        if self.rect.bottom < 0:
            self.kill()
