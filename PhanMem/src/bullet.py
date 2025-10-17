import pygame
import math
from utils import load_image, load_sound

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0, damage=10, speed=12, spiral=False):
        super().__init__()
        self.original_image = load_image("image/bullet/normal_bullet.png")
        self.original_image = pygame.transform.scale(self.original_image, (8, 20))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        # Hướng bay
        self.angle = angle
        self.speed = speed
        self.vel_x = self.speed * math.sin(math.radians(self.angle))
        self.vel_y = -self.speed * math.cos(math.radians(self.angle))

        # Sát thương
        self.damage = damage

        # Cờ xoắn ốc
        self.spiral = spiral
        self.time_alive = 0
        self.radius = 0
        self.center_x = x
        self.center_y = y

        # Âm thanh bắn
        self.sound = load_sound("sound/Shot/Laser Shot.wav")
        self.sound.set_volume(0.25)
        self.sound.play()

    
        # --- Đạn thường ---
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Nếu bay ra ngoài màn hình thì xóa
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > 800:
            self.kill()

