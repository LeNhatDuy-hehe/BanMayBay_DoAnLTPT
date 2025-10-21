import pygame
import math
import os
from utils import load_image
from settings import PLAYER_SIZE, rong, cao

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, toc_do, dan_nhom):
        super().__init__()
        self.image = load_image("image/player/player.png")
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(center=(x, y))
        self.toc_do = toc_do
        self.dan_nhom = dan_nhom
        self.sung_level = 1
        self.tim = 3
        self.cooldown = 250  # ms
        self.last_shot = pygame.time.get_ticks()

        # Hiệu ứng súng siêu cấp
        self.aura_angle = 0
        self.aura_radius = 45
        self.aura_color = (255, 215, 0)
        self.aura_alpha = 100

        # Load âm thanh bắn súng
        try:
            shot_sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "Shot", "Laser Shot.wav")
            self.shot_sound = pygame.mixer.Sound(shot_sound_path)
            self.shot_sound.set_volume(1.0)  # Điều chỉnh âm lượng để không quá to
            print("✅ Đã load âm thanh bắn súng thành công!")
        except Exception as e:
            self.shot_sound = None
            print(f"⚠️ Không thể load âm thanh bắn súng: {e}")
 
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.toc_do
        if keys[pygame.K_RIGHT] and self.rect.right < rong:
            self.rect.x += self.toc_do
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.toc_do
        if keys[pygame.K_DOWN] and self.rect.bottom < cao:
            self.rect.y += self.toc_do
        if keys[pygame.K_SPACE]:
            self.ban_dan()

        # Xoay hiệu ứng quanh player nếu đang ở Level 5
        if self.sung_level == 5:
            self.aura_angle += 6
            if self.aura_angle >= 360:
                self.aura_angle = 0

    def ban_dan(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            self.last_shot = now

            # 🔊 Phát âm thanh bắn súng
            if self.shot_sound:
                self.shot_sound.play()

            x, y = self.rect.centerx, self.rect.top
                # C1: Đạn thẳng
            if self.sung_level == 1:
                self.dan_nhom.add(Dan(x, y, 0))
                # C2: Đạn đôi
            elif self.sung_level == 2:
                self.dan_nhom.add(Dan(x - 15, y, 0))
                self.dan_nhom.add(Dan(x + 15, y, 0))
             # C3: Đạn ba — tỏa cực nhẹ và cân đều
            elif self.sung_level == 3:
                self.dan_nhom.add(Dan(x, y, 0))           # giữa
                self.dan_nhom.add(Dan(x - 12, y, -1))     # trái nhẹ
                self.dan_nhom.add(Dan(x + 12, y, 1))      # phải nhẹ

            # C4: Hai đạn giữa thẳng + hai đạn ngoài tỏa cực nhẹ và đối xứng
            elif self.sung_level == 4:
            # Hai viên giữa
                self.dan_nhom.add(Dan(x - 8, y, 0))
                self.dan_nhom.add(Dan(x + 8, y, 0))

            # Hai viên ngoài, cân tuyệt đối
                self.dan_nhom.add(Dan(x - 20, y, -1))
                self.dan_nhom.add(Dan(x + 20, y, 1))


            elif self.sung_level == 5:
                # Đạn xoắn ốc (cực đẹp)
                for angle in range(0, 360, 60):
                    rad = math.radians(angle + self.aura_angle)
                    dx = math.cos(rad) * 6
                    dy = math.sin(rad) * 6 - 10  # bay lên
                    self.dan_nhom.add(DanXoanOc(x, y, dx, dy))

    def ve_hieu_ung(self, man_hinh):
        """✨ Hiệu ứng ánh sáng quanh máy bay ở cấp 5"""
        if self.sung_level == 5:
            for i in range(6):
                angle = math.radians(self.aura_angle + i * 60)
                px = self.rect.centerx + math.cos(angle) * self.aura_radius
                py = self.rect.centery + math.sin(angle) * self.aura_radius
                pygame.draw.circle(man_hinh, self.aura_color, (int(px), int(py)), 5)
    
class Dan(pygame.sprite.Sprite):
    def __init__(self, x, y, dx):
        super().__init__()
        self.image = pygame.Surface((6, 14))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speedy = -10
        self.speedx = dx

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()

class DanXoanOc(pygame.sprite.Sprite):
    """Đạn siêu cấp xoắn ốc (cấp 5)"""
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((8, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 255, 0), (0, 0, 8, 16))
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > rong:
            self.kill()
