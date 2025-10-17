import pygame
import random
import math
import os

# ----------- Đạn Boss tỏa tròn -----------
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0, speed=4, color=(255, 0, 0), size=(8, 20)):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = speed
        self.rad = math.radians(angle)

    def update(self):
        self.rect.x += self.speed * math.cos(self.rad)
        self.rect.y += self.speed * math.sin(self.rad)
        if (self.rect.top > 800 or self.rect.left < 0 or 
            self.rect.right > 800 or self.rect.bottom < 0):
            self.kill()


# ----------- Đạn Laser 5 tia -----------
class BossLaser(BossBullet):
    def __init__(self, x, y, offset_x=0, speed=6):
        super().__init__(x + offset_x, y, angle=90, speed=speed, color=(0, 255, 255), size=(6, 25))
        self.rect = self.image.get_rect(center=(x + offset_x, y))


# ----------- Boss chính -----------
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=0.5, hp=600, bullet_group=None, level=1):
        super().__init__()
        current_path = os.path.dirname(__file__)

        # ======= Cấu hình theo cấp độ =======
        if level == 1:
            boss_img = "boss1.png"
            hp = 1200
            speed = 0.8
        elif level == 2:
            boss_img = "boss2.png"
            hp = 1800
            speed = 1.2

        # ======= Tải hình ảnh =======
        boss_img_path = os.path.join(current_path, "..", "assets", "image", "boss", boss_img)
        self.image = pygame.image.load(boss_img_path).convert_alpha()

        size_map = {1: (220, 160), 2: (240, 180)}
        self.image = pygame.transform.scale(self.image, size_map.get(level, (220, 160)))
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.level = level
        self.direction = 1
        self.bullet_group = bullet_group

        # ======= Điều chỉnh delay tấn công theo cấp độ =======
        self.shoot_delay = max(2000 - 300 * (level - 1), 1000)
        self.laser_delay = max(500 - 50 * (level - 1), 250)
        self.energy_wave_delay = max(100 - 10 * (level - 1), 40)
        self.triple_delay = max(1000 - 100 * (level - 1), 500)

        # ======= Bộ đếm bắn =======
        self.last_shot = pygame.time.get_ticks()
        self.last_laser = pygame.time.get_ticks()
        self.last_energy_wave = pygame.time.get_ticks()
        self.last_triple = pygame.time.get_ticks()

        self.laser_count = 0
        self.max_laser_shots = 3
        self.energy_wave_count = 0
        self.max_energy_wave = 3

        # ======= Hiệu ứng xuất hiện =======
        self.alpha = 0
        self.appearing = True

        # ======= Nhạc Boss - phát MusicBoss.wav cho cả boss 1 và boss 2 =======
        boss_music_path = os.path.join(current_path, "..", "assets", "sound", "Boss", "MusicBoss.wav")
        if os.path.exists(boss_music_path):
            try:
                pygame.mixer.music.load(boss_music_path)
                pygame.mixer.music.set_volume(0.7)  # Điều chỉnh âm lượng
                pygame.mixer.music.play(-1)  # Loop vô hạn
                print(f"🎵 Đang phát nhạc boss level {level}!")
            except pygame.error as e:
                print(f"⚠️ Không thể phát nhạc boss: {e}")
        else:
            print(f"⚠️ Không tìm thấy file nhạc boss: {boss_music_path}")

    def update(self):
        if self.appearing:
            self.alpha += 8
            if self.alpha >= 255:
                self.alpha = 255
                self.appearing = False
            self.image.set_alpha(self.alpha)
            return

        # Di chuyển ngang
        self.rect.x += self.speed * self.direction
        if self.rect.right >= 760 or self.rect.left <= 20:
            self.direction *= -1

        now = pygame.time.get_ticks()

        # Đạn tỏa tròn
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.level == 1:
                self.shoot_circle()  # bình thường
            elif self.level == 2:
                self.shoot_spiral()  # xoáy dần

        # 5 tia laser dưới 50% HP
        if self.hp <= self.max_hp / 2 and self.laser_count < self.max_laser_shots:
            if now - self.last_laser > self.laser_delay:
                self.last_laser = now
                if self.level == 1:
                    self.shoot_lasers()
                elif self.level == 2:
                    self.shoot_lasers_double()
                self.laser_count += 1

        # Sóng năng lượng dưới 75% HP
        if self.hp <= 0.75 * self.max_hp and self.energy_wave_count < self.max_energy_wave:
            if now - self.last_energy_wave > self.energy_wave_delay:
                self.last_energy_wave = now
                if self.level == 1:
                    self.shoot_energy_wave()
                elif self.level == 2:
                    self.shoot_energy_wave_fast()
                self.energy_wave_count += 1

        # 3 nòng tốc độ chậm dưới 25% HP
        if self.hp <= 0.25 * self.max_hp:
            if now - self.last_triple > self.triple_delay:
                self.last_triple = now
                if self.level == 1:
                    self.shoot_triple()
                elif self.level == 2:
                    self.shoot_triple_diagonal()

    # ====== Các kiểu tấn công ======
    def shoot_circle(self):
        if self.bullet_group is None:
            return
        num_bullets = random.randint(15, 20)
        for i in range(num_bullets):
            angle = (360 / num_bullets) * i
            bullet = BossBullet(self.rect.centerx, self.rect.centery, angle, speed=random.uniform(3, 5))
            self.bullet_group.add(bullet)

    # --- Boss 2 xoáy tròn ---
    def shoot_spiral(self):
        if self.bullet_group is None: return
        base = random.randint(0, 360)
        for i in range(30):
            angle = base + i * 12
            bullet = BossBullet(self.rect.centerx, self.rect.centery, angle, speed=4, color=(255, 150, 0))
            self.bullet_group.add(bullet)

    def shoot_lasers(self):
        if self.bullet_group is None:
            return
        offsets = [-80, -40, 0, 40, 80]
        for off in offsets:
            laser = BossLaser(self.rect.centerx, self.rect.bottom, offset_x=off)
            self.bullet_group.add(laser)

    # --- Boss 2 bắn laser kép ---
    def shoot_lasers_double(self):
        if self.bullet_group is None: return
        for off in [-60, -20, 20, 60]:
            laser1 = BossLaser(self.rect.centerx, self.rect.bottom, offset_x=off, speed=7)
            laser2 = BossLaser(self.rect.centerx, self.rect.bottom, offset_x=off+10, speed=7)
            self.bullet_group.add(laser1, laser2)

    def shoot_energy_wave(self):
        if self.bullet_group is None:
            return
        num_bullets = 25
        for i in range(num_bullets):
            angle = (360 / num_bullets) * i
            bullet = BossBullet(self.rect.centerx, self.rect.centery, angle, speed=3)
            self.bullet_group.add(bullet)

    # --- Boss 2: Sóng nhanh ---
    def shoot_energy_wave_fast(self):
        if self.bullet_group is None: return
        for i in range(30):
            angle = (360 / 30) * i
            bullet = BossBullet(self.rect.centerx, self.rect.centery, angle, speed=5, color=(255, 255, 0))
            self.bullet_group.add(bullet)

    def shoot_triple(self):
        if self.bullet_group is None:
            return
        offsets = [-60, 0, 60]
        for off in offsets:
            bullet = BossBullet(self.rect.centerx + off, self.rect.bottom, angle=90, speed=2)
            self.bullet_group.add(bullet)

    # --- Boss 2: Triple chéo ---
    def shoot_triple_diagonal(self):
        if self.bullet_group is None: return
        for angle in [60, 90, 120]:
            bullet = BossBullet(self.rect.centerx, self.rect.centery, angle, speed=4, color=(0, 255, 0))
            self.bullet_group.add(bullet)

    def tru_mau(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            return True
        return False

    def ve(self, man_hinh):
        man_hinh.blit(self.image, self.rect)
        self.ve_hp_bar(man_hinh)

    def ve_hp_bar(self, man_hinh):
        bar_width = 400
        bar_height = 20
        fill = int((self.hp / self.max_hp) * bar_width)
        outline_rect = pygame.Rect(200, 10, bar_width, bar_height)
        fill_rect = pygame.Rect(outline_rect.x, outline_rect.y, fill, bar_height)
        pygame.draw.rect(man_hinh, (255, 0, 0), fill_rect)
        pygame.draw.rect(man_hinh, (255, 255, 255), outline_rect, 3)

    def stop_boss_music(self):
        """Dừng nhạc boss khi boss bị tiêu diệt"""
        try:
            pygame.mixer.music.stop()
            print("🎵 Đã dừng nhạc boss!")
        except pygame.error as e:
            print(f"⚠️ Lỗi khi dừng nhạc boss: {e}")
