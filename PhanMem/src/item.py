import pygame
import random
import os


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, screen_height):
        super().__init__()
        self.type = item_type

        # --- Xác định đường dẫn gốc ---
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # => PhanMem/
        item_folder = os.path.join(BASE_DIR, "assets", "image", "item")

        try:
            if self.type == "hp":
                path = os.path.join(item_folder, "heart.png")
                self.image = pygame.image.load(path).convert_alpha()
            elif self.type == "power":
                path = os.path.join(item_folder, "powerup.png")
                self.image = pygame.image.load(path).convert_alpha()
            else:
                # fallback: ô vuông đỏ
                self.image = pygame.Surface((25, 25))
                self.image.fill((255, 0, 0))
        except Exception as e:
            print(f"⚠️ Lỗi load ảnh item: {e}")
            # fallback: ô vuông tím nếu không load được ảnh
            self.image = pygame.Surface((25, 25))
            self.image.fill((128, 0, 128))

        # --- Resize ảnh item ---
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.kill()


def drop_item(x, y, screen_height):
    """Tạo item ngẫu nhiên (15% rơi ra)"""
    if random.random() < 0.15:
        items = ["power", "hp"]
        weights = [0.09, 0.06]  # Power 9%, HP 6%
        item_type = random.choices(items, weights=weights, k=1)[0]
        return Item(x, y, item_type, screen_height)
    return None
