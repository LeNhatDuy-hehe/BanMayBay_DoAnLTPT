import pygame
from bullet import Bullet
from settings import PLAYER_SIZE, rong  # lấy luôn rong để giới hạn biên

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, dan_group):
        super().__init__()
        # Load và scale ảnh player
        anh = pygame.image.load("assets/image/player/player.png").convert_alpha()
        self.image = pygame.transform.scale(anh, PLAYER_SIZE)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Thuộc tính
        self.speed = speed
        self.tim = 3
        self.dan_group = dan_group

        # Cooldown bắn
        self.cooldown = 300  # mili giây giữa 2 lần bắn
        self.last_shot = pygame.time.get_ticks()

        # Level súng
        self.sung_level = 1   # bắt đầu 1 tia

    def update(self):
        keys = pygame.key.get_pressed()
        # Di chuyển trái/phải
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < rong:
            self.rect.x += self.speed

        # Bắn đạn (Space)
        if keys[pygame.K_SPACE]:
            self.ban()

    def ban(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            self.last_shot = now

            # Bắn theo cấp độ súng
            if self.sung_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.dan_group.add(bullet)

            elif self.sung_level == 2:
                bullet1 = Bullet(self.rect.centerx - 10, self.rect.top)
                bullet2 = Bullet(self.rect.centerx + 10, self.rect.top)
                self.dan_group.add(bullet1, bullet2)

            elif self.sung_level >= 3:
                bullet1 = Bullet(self.rect.centerx, self.rect.top)
                bullet2 = Bullet(self.rect.centerx - 15, self.rect.top)
                bullet3 = Bullet(self.rect.centerx + 15, self.rect.top)
                self.dan_group.add(bullet1, bullet2, bullet3)
