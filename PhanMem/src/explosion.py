import pygame
import random
import math
import os

class Explosion(pygame.sprite.Sprite):
    """Hiệu ứng nổ cho va chạm và tiêu diệt enemy/boss"""
    
    def __init__(self, x, y, size="normal", color=None):
        super().__init__()
        self.x = x
        self.y = y
        self.size_type = size
        
        # Kích thước theo loại nổ (giảm kích thước)
        self.sizes = {
            "small": 10,      
            "normal": 20,      
            "large": 30,      
            "boss": 120       
        }
        
        self.max_radius = self.sizes.get(size, 35)
        self.radius = 3   
        self.expansion_speed = 2   
        
        # Màu sắc theo loại nổ
        if color:
            self.colors = color
        else:
            color_schemes = {
                "small": [(255, 100, 0), (255, 200, 0), (255, 255, 100)],
                "normal": [(255, 50, 0), (255, 150, 0), (255, 255, 0)],
                "large": [(255, 0, 0), (255, 100, 0), (255, 200, 0)],
                "boss": [(255, 0, 0), (255, 50, 0), (255, 150, 0), (255, 255, 255)]
            }
            self.colors = color_schemes.get(size, [(255, 100, 0), (255, 200, 0)])
        
        # Tạo surface trong suốt
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Load hình ảnh nổ cho player và enemy
        self.use_image = size in ["normal", "large"]  # Chỉ dùng hình cho player/enemy
        self.explosion_image = None
        
        if self.use_image:
            try:
                # Load hình player_hit.png
                image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "image", "player", "player_hit.png")
                if os.path.exists(image_path):
                    self.explosion_image = pygame.image.load(image_path).convert_alpha()
                    # Scale theo kích thước nổ
                    scale_size = int(self.max_radius * 1.5)
                    self.explosion_image = pygame.transform.scale(self.explosion_image, (scale_size, scale_size))
            except Exception:
                self.use_image = False
        
        # Hiệu ứng
        self.alpha = 255
        self.fade_speed = 8
        self.particles = []
        
        # Tạo particles cho hiệu ứng đẹp hơn (giảm số lượng)
        particle_count = {
            "small": 4,     
            "normal": 6,     
            "large": 8,       
            "boss": 24       
        }
        
        for _ in range(particle_count.get(size, 6)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2.5) 
            self.particles.append({
                'x': 0,
                'y': 0,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': random.randint(1, 3),  
                'color': random.choice(self.colors),
                'life': 180 
            })
        
        # Âm thanh nổ (nếu có)
        self.play_explosion_sound()
    
    def play_explosion_sound(self):
        """Phát âm thanh nổ"""
        try:
            sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "Shot", "Laser Shot.wav")
            if os.path.exists(sound_path):
                explosion_sound = pygame.mixer.Sound(sound_path)
                explosion_sound.set_volume(0.2)  # giảm từ 0.3
                explosion_sound.play()
        except Exception:
            pass
    
    def update(self):
        """Cập nhật hiệu ứng nổ"""
        # Xóa image cũ
        self.image.fill((0, 0, 0, 0))
        
        # Nếu sử dụng hình ảnh player_hit.png
        if self.use_image and self.explosion_image:
            if self.radius < self.max_radius:
                self.radius += self.expansion_speed
                
                # Tính toán scale và alpha dựa trên radius
                scale_factor = min(self.radius / self.max_radius * 2, 1.5)
                scaled_image = pygame.transform.scale(
                    self.explosion_image, 
                    (int(self.explosion_image.get_width() * scale_factor),
                     int(self.explosion_image.get_height() * scale_factor))
                )
                
                # Vẽ hình nổ ở giữa
                center_pos = (
                    self.max_radius - scaled_image.get_width() // 2,
                    self.max_radius - scaled_image.get_height() // 2
                )
                self.image.blit(scaled_image, center_pos)
        else:
            # Vẽ vòng tròn chính (cho boss và trường hợp không load được hình)
            if self.radius < self.max_radius:
                self.radius += self.expansion_speed
                
                # Vẽ nhiều vòng tròn với màu khác nhau
                center = (self.max_radius, self.max_radius)
                
                for i, color in enumerate(self.colors):
                    current_radius = max(1, self.radius - i * 6)  # giảm từ 8
                    if current_radius > 0:
                        pygame.draw.circle(self.image, (*color, self.alpha), center, current_radius)
        
        # Cập nhật và vẽ particles (giảm kích thước particles)
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 8  # tăng từ 6 để biến mất nhanh hơn
            particle['size'] = max(1, particle['size'] - 0.15)  # tăng từ 0.1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                continue
            
            # Vẽ particle nhỏ hơn
            pos = (
                int(self.max_radius + particle['x']), 
                int(self.max_radius + particle['y'])
            )
            
            if 0 <= pos[0] < self.max_radius * 2 and 0 <= pos[1] < self.max_radius * 2:
                pygame.draw.circle(self.image, particle['color'], pos, max(1, int(particle['size'])))
        
        # Fade out nhanh hơn
        if self.radius >= self.max_radius:
            self.alpha -= 12  # tăng từ 8
            if self.alpha <= 0:
                self.kill()
        
        # Cập nhật alpha cho toàn bộ surface
        self.image.set_alpha(self.alpha)

class ShockWave(pygame.sprite.Sprite):
    """Hiệu ứng sóng xung kích cho boss nổ"""
    
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 10
        self.max_radius = 200
        self.expansion_speed = 8
        self.alpha = 100
        
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        """Cập nhật sóng xung kích"""
        self.image.fill((0, 0, 0, 0))
        
        if self.radius < self.max_radius:
            self.radius += self.expansion_speed
            self.alpha -= 2
            
            center = (self.max_radius, self.max_radius)
            
            # Vẽ vòng tròn sóng xung kích
            pygame.draw.circle(self.image, (100, 150, 255), center, self.radius, 3)
            
        if self.alpha <= 0 or self.radius >= self.max_radius:
            self.kill()

def create_explosion(x, y, explosion_type="normal"):
    """Tạo hiệu ứng nổ tại vị trí (x, y)"""
    return Explosion(x, y, explosion_type)

def create_boss_explosion(x, y):
    """Tạo hiệu ứng nổ đặc biệt cho boss"""
    explosions = []
    
    # Nổ chính
    main_explosion = Explosion(x, y, "boss")
    explosions.append(main_explosion)
    
    # Sóng xung kích
    shockwave = ShockWave(x, y)
    explosions.append(shockwave)
    
    # Nổ phụ xung quanh
    for i in range(5):
        offset_x = random.randint(-60, 60)
        offset_y = random.randint(-60, 60)
        delay = i * 100  # Tạo độ trễ
        
        sub_explosion = Explosion(x + offset_x, y + offset_y, "large")
        explosions.append(sub_explosion)
    
    return explosions
