import pygame
import random
import os

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, screen_height):
        super().__init__()
        self.type = item_type

        try:
            if self.type == "hp":
                self.image = pygame.image.load(
                    os.path.join("assets", "image", "item", "heart.png")
                ).convert_alpha()
            elif self.type == "power":
                self.image = pygame.image.load(
                    os.path.join("assets", "image", "item", "powerup.png")
                ).convert_alpha()
            else:
                # fallback: ô vuông đỏ
                self.image = pygame.Surface((25, 25))
                self.image.fill((255, 0, 0))
        except:
            # fallback: ô vuông tím nếu không load được ảnh
            self.image = pygame.Surface((25, 25))
            self.image.fill((128, 0, 128))

        # resize ảnh 25x25
        self.image = pygame.transform.scale(self.image, (25, 25))

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.kill()


def drop_item(x, y, screen_height):
    if random.random() < 0.15:  # 15% rơi item
        items = ["power", "hp"]
        weights = [0.09, 0.06]  # Power 9%, HP 6%
        item_type = random.choices(items, weights=weights, k=1)[0]
        return Item(x, y, item_type, screen_height)
    return None
