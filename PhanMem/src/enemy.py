import pygame
import random
from utils import load_image
from settings import ENEMY_SIZE, cao, rong  # lấy luôn chiều cao, rộng màn hình

class Dich(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, level=1):
        super().__init__()

        # Giới hạn level trong khoảng 1–2 (đã xóa boss 3)
        self.level = max(1, min(level, 2))

        # Chọn ảnh địch tùy theo level
        image_paths = {
            1: "image/boss/boss1.png",
            2: "image/boss/boss2.png"
        }
        enemy_img = load_image(image_paths[self.level])

        # Resize ảnh địch
        self.image = pygame.transform.scale(enemy_img, ENEMY_SIZE)
        self.rect = self.image.get_rect(center=(x, y))

        # Thuộc tính chiến đấu (đã cân bằng)
        self.base_speed = speed
        # tốc độ tăng nhẹ dần theo cấp
        self.speed = speed + (self.level - 1) * 0.3
        # máu tăng nhẹ theo cấp (Level 1:1.0, L2:1.5, L3:2.0)
        self.hp = 1 + (self.level - 1) * 0.5

    def update(self):
        """Cập nhật vị trí địch"""
        self.rect.y += self.speed

        # Nếu bay khỏi màn hình thì xuất hiện lại ngẫu nhiên ở trên
        if self.rect.top > cao:
            self.rect.y = -random.randint(40, 120)
            self.rect.x = random.randint(20, rong - 20)

    def tru_mau(self, damage=1):
        """Trừ máu khi trúng đạn — trả True nếu địch chết"""
        self.hp -= damage
        return self.hp <= 0
