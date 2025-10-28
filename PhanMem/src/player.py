import pygame
import math
import os
from utils import load_image
from settings import PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, bullet_group):
        super().__init__()
        self.image = load_image("image/player/player.png")
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(center=(x, y))
        # English primary names
        self.speed = speed
        self.bullet_group = bullet_group
        self.gun_level = 1
        self.lives = 3
        self.cooldown = 250  # ms
        self.last_shot = pygame.time.get_ticks()

        # Hiệu ứng súng siêu cấp
        self.aura_angle = 0
        self.aura_radius = 45
        self.aura_color = (255, 215, 0)
        self.aura_alpha = 100

        # Load shooting sound
        try:
            shot_sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "Shot", "Laser Shot.wav")
            self.shot_sound = pygame.mixer.Sound(shot_sound_path)
            self.shot_sound.set_volume(1.0)
        except Exception as e:
            self.shot_sound = None
            # silent fallback
 
    def update(self):
        """Cập nhật trạng thái người chơi mỗi khung hình:
      - Di chuyển theo phím mũi tên trong giới hạn màn hình.
      - Bắn đạn khi nhấn phím cách (SPACE).
      - Xoay hiệu ứng quanh người chơi nếu đạt cấp súng 5."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Xoay hiệu ứng quanh player nếu đang ở Level 5
        if self.gun_level == 5:
            self.aura_angle += 6
            if self.aura_angle >= 360:
                self.aura_angle = 0

    # Vietnamese alias for existing code
    def ban_dan(self):
        return self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            self.last_shot = now

            # Phát âm thanh bắn súng
            if self.shot_sound:
                self.shot_sound.play()

            x, y = self.rect.centerx, self.rect.top
                # C1: Đạn thẳng
            if self.gun_level == 1:
                self.bullet_group.add(BulletStraight(x, y, 0))
                # C2: Đạn đôi
            elif self.gun_level == 2:
                self.bullet_group.add(BulletStraight(x - 15, y, 0))
                self.bullet_group.add(BulletStraight(x + 15, y, 0))
             # C3: Đạn ba — tỏa cực nhẹ và cân đều
            elif self.gun_level == 3:
                self.bullet_group.add(BulletStraight(x, y, 0))           # giữa
                self.bullet_group.add(BulletStraight(x - 12, y, -1))     # trái nhẹ
                self.bullet_group.add(BulletStraight(x + 12, y, 1))      # phải nhẹ

            # C4: Hai đạn giữa thẳng + hai đạn ngoài tỏa cực nhẹ và đối xứng
            elif self.gun_level == 4:
            # Hai viên giữa
                self.bullet_group.add(BulletStraight(x - 8, y, 0))
                self.bullet_group.add(BulletStraight(x + 8, y, 0))

            # Hai viên ngoài, cân tuyệt đối
                self.bullet_group.add(BulletStraight(x - 20, y, -1))
                self.bullet_group.add(BulletStraight(x + 20, y, 1))


            elif self.gun_level == 5:
                # Đạn xoắn ốc
                for angle in range(0, 360, 60):
                    rad = math.radians(angle + self.aura_angle)
                    dx = math.cos(rad) * 6
                    dy = math.sin(rad) * 6 - 10  # bay lên
                    self.bullet_group.add(SpiralBullet(x, y, dx, dy))

    def draw_effect(self, surface):
        """✨ Hiệu ứng ánh sáng quanh máy bay ở cấp 5"""
        if self.gun_level == 5:
            for i in range(6):
                angle = math.radians(self.aura_angle + i * 60)
                px = self.rect.centerx + math.cos(angle) * self.aura_radius
                py = self.rect.centery + math.sin(angle) * self.aura_radius
                pygame.draw.circle(surface, self.aura_color, (int(px), int(py)), 5)
    
class BulletStraight(pygame.sprite.Sprite):
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

class SpiralBullet(pygame.sprite.Sprite):
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
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# --- Backward compatibility aliases (Vietnamese names) ---
# Constructor compatibility: allow old parameter names via kwargs
def _player_init_alias(self, x, y, toc_do=None, dan_nhom=None, **kwargs):
    # Map Vietnamese params if provided
    speed = kwargs.get('speed', toc_do)
    bullet_group = kwargs.get('bullet_group', dan_nhom)
    Player.__init__(self, x, y, speed, bullet_group)

# Attribute aliases
Player.toc_do = property(lambda self: self.speed, lambda self, v: setattr(self, 'speed', v))
Player.dan_nhom = property(lambda self: self.bullet_group, lambda self, v: setattr(self, 'bullet_group', v))
Player.sung_level = property(lambda self: self.gun_level, lambda self, v: setattr(self, 'gun_level', v))
Player.tim = property(lambda self: self.lives, lambda self, v: setattr(self, 'lives', v))

# Method aliases
Dan = BulletStraight
DanXoanOc = SpiralBullet
