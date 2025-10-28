import pygame
import random
from utils import load_image
from settings import ENEMY_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    """ Lớp đại diện cho kẻ địch trong trò chơi bắn máy bay.

    Kế thừa từ pygame.sprite.Sprite để tận dụng hệ thống quản lý sprite.
    Kẻ địch có khả năng di chuyển từ trên xuống, nhận sát thương và respawn
    khi ra khỏi màn hình."""

    def __init__(self, x, y, speed, level=1):
        """Khởi tạo đối tượng địch với vị trí, tốc độ và cấp độ nhất định.
    - Cấp độ ảnh hưởng đến hình ảnh, tốc độ và máu của địch"""
        super().__init__()


        self.level = max(1, min(level, 2))


        image_paths = {
            1: "image/boss/boss1.png",
            2: "image/boss/boss2.png"
        }
        enemy_img = load_image(image_paths[self.level])


        self.image = pygame.transform.scale(enemy_img, ENEMY_SIZE)
        self.rect = self.image.get_rect(center=(x, y))


        self.base_speed = speed

        self.speed = speed + (self.level - 1) * 0.3

        self.hp = 1 + (self.level - 1) * 0.5

    def update(self):
        """Cập nhật vị trí của kẻ địch mỗi frame.
        
        Di chuyển kẻ địch xuống phía dưới màn hình theo tốc độ đã định.
        Khi vượt qua biên dưới màn hình, tự động respawn tại vị trí
        ngẫu nhiên phía trên với tọa độ X ngẫu nhiên."""
        self.rect.y += self.speed

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -random.randint(40, 120)
            self.rect.x = random.randint(20, SCREEN_WIDTH - 20)

    def take_damage(self, damage=1):
        """Nhận sát thương từ đạn hoặc va chạm.
        
        Giảm HP của kẻ địch theo lượng damage nhận vào. Trả về True
        nếu kẻ địch bị tiêu diệt (HP <= 0), ngược lại trả về False."""
        self.hp -= damage
        return self.hp <= 0
