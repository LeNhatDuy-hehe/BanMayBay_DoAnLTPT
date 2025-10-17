import pygame
import random
import os
import sys
import math
from settings import rong, cao, DO, FPS
from player import Player
from enemy import Dich
from hud import Hud
from item import Item, drop_item
from boss import Boss

pygame.init()
man_hinh = pygame.display.set_mode((rong, cao))
pygame.display.set_caption("PLANE SHOOTER")
dong_ho = pygame.time.Clock()

# ======== ĐƯỜNG DẪN ẢNH ========
assets_path = os.path.join(os.path.dirname(__file__), "..", "assets", "image", "scrollbackground")
bg_game = pygame.image.load(os.path.join(assets_path, "scroll_background.png")).convert()
bg_menu = pygame.image.load(os.path.join(assets_path, "backgroundmenu.jpg")).convert()
bg_game = pygame.transform.scale(bg_game, (rong, cao))
bg_menu = pygame.transform.scale(bg_menu, (rong, cao))

# ==================== MÀN HÌNH MENU ====================
def main_menu():
    menu_music = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "endgame", "Endgame.wav")
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)

    font = pygame.font.SysFont("Arial", 48, bold=True)
    title_text = font.render("PLANE SHOOTER", True, (255, 215, 0))
    play_text = font.render("NEW GAME", True, (255, 215, 0))
    exit_text = font.render("EXIT", True, (255, 215, 0))

    title_rect = title_text.get_rect(center=(rong // 2, cao // 2 - 150))
    play_rect = play_text.get_rect(center=(rong // 2, cao // 2))
    exit_rect = exit_text.get_rect(center=(rong // 2, cao // 2 + 80))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return True
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        play_text = font.render("NEW GAME", True, (255, 255, 0) if play_rect.collidepoint(mouse_pos) else (255, 215, 0))
        exit_text = font.render("EXIT", True, (255, 255, 0) if exit_rect.collidepoint(mouse_pos) else (255, 215, 0))

        # Vẽ nền menu
        man_hinh.blit(bg_menu, (0, 0))
        man_hinh.blit(title_text, title_rect)
        man_hinh.blit(play_text, play_rect)
        man_hinh.blit(exit_text, exit_rect)
        pygame.display.flip()
        dong_ho.tick(FPS)

# ==================== MÀN HÌNH GAME OVER ====================
def game_over_screen(score):
    gameover_music = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "endgame", "Endgame.wav")
    pygame.mixer.music.load(gameover_music)
    pygame.mixer.music.play(-1)

    font_small = pygame.font.SysFont("Arial", 36)
    score_text = font_small.render(f"Your Score: {score}", True, (255, 255, 255))
    retry_text = font_small.render("PLAY AGAIN", True, (0, 255, 0))
    exit_text = font_small.render("EXIT", True, (255, 255, 255))

    score_rect = score_text.get_rect(center=(rong // 2, cao // 2 - 80))
    retry_rect = retry_text.get_rect(center=(rong // 2, cao // 2))
    exit_rect = exit_text.get_rect(center=(rong // 2, cao // 2 + 80))

    while True:
        man_hinh.fill((0, 0, 0))
        man_hinh.blit(score_text, score_rect)
        man_hinh.blit(retry_text, retry_rect)
        man_hinh.blit(exit_text, exit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return True
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# ==================== HÀM HIỂN THỊ THÔNG BÁO BOSS ====================
def draw_boss_warning(screen, boss_stage, warning_time):
    """Hiển thị thông báo báo động boss"""
    # Tạo hiệu ứng nhấp nháy
    alpha = int(255 * (0.5 + 0.5 * math.sin(warning_time * 0.01)))
    
    # Tạo surface cho text với alpha
    warning_surface = pygame.Surface((rong, cao), pygame.SRCALPHA)
    
    # Vẽ nền đỏ mờ
    red_overlay = pygame.Surface((rong, cao), pygame.SRCALPHA)
    red_overlay.fill((255, 0, 0, 50))
    warning_surface.blit(red_overlay, (0, 0))
    
    # Font cho text
    big_font = pygame.font.Font(None, 72)
    medium_font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)
    
    # Text chính
    main_text = "Give Warning Of Danger"
    main_surface = big_font.render(main_text, True, (255, 255, 0))
    main_surface.set_alpha(alpha)
    main_rect = main_surface.get_rect(center=(rong//2, cao//2 - 80))
    warning_surface.blit(main_surface, main_rect)
    
    # Text boss
    boss_text = f"BOSS {boss_stage}"
    boss_surface = medium_font.render(boss_text, True, (255, 100, 100))
    boss_surface.set_alpha(alpha)
    boss_rect = boss_surface.get_rect(center=(rong//2, cao//2 - 20))
    warning_surface.blit(boss_surface, boss_rect)
    
    # Text hướng dẫn
    instruction_text = "Prepare For Battle"
    instruction_surface = small_font.render(instruction_text, True, (255, 255, 255))
    instruction_surface.set_alpha(alpha)
    instruction_rect = instruction_surface.get_rect(center=(rong//2, cao//2 + 40))
    warning_surface.blit(instruction_surface, instruction_rect)
    
    # Countdown
    remaining_time = max(0, 3 - warning_time // 1000)
    if remaining_time > 0:
        countdown_text = f"{remaining_time + 1}"
        countdown_surface = big_font.render(countdown_text, True, (255, 0, 0))
        countdown_surface.set_alpha(255)
        countdown_rect = countdown_surface.get_rect(center=(rong//2, cao//2 + 100))
        warning_surface.blit(countdown_surface, countdown_rect)
    
    screen.blit(warning_surface, (0, 0))

# ==================== HÀM KHỞI TẠO GAME ====================
def start_game():
    music_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "BackgroundMusic", "awestruck.wav")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    tatca_sprites = pygame.sprite.Group()
    dichs = pygame.sprite.Group()
    dan_nguoi_choi = pygame.sprite.Group()
    items = pygame.sprite.Group()
    boss_dan = pygame.sprite.Group()
    boss_nhom = pygame.sprite.Group()

    may_bay = Player(rong // 2, cao - 80, 5, dan_nguoi_choi)
    tatca_sprites.add(may_bay)

    hud = Hud(may_bay)

    # ======= Load âm thanh báo động =======
    try:
        warning_sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "Shot", "Laser Shot.wav")
        warning_sound = pygame.mixer.Sound(warning_sound_path)
        warning_sound.set_volume(0.8)
    except:
        warning_sound = None
        print("⚠️ Không thể load âm thanh báo động")

    thoi_gian_sinh_dich = 0
    delay_sinh_dich = 1000
    max_dich = 30
    bg_y = 0
    bg_speed = 2
    start_time = pygame.time.get_ticks()

    boss_stage = 1
    boss = None
    boss_dang_ra = False

    # ======= Hệ thống báo động boss =======
    boss_warning_active = False
    boss_warning_start_time = 0
    boss_warning_duration = 3000  # 3 giây báo động
    boss_warning_stage = 0  # Stage của boss sắp xuất hiện

    running = True
    while running:
        dt = dong_ho.tick(FPS)
        thoi_gian_sinh_dich += dt

        # ======= Sự kiện =======
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT + 1:
                may_bay.sung_level = 4
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)

        tatca_sprites.update()
        dan_nguoi_choi.update()
        items.update()
        boss_dan.update()
        if boss:
            boss.update()

        # ======= Cuộn nền =======
        man_hinh.blit(bg_game, (0, bg_y))
        man_hinh.blit(bg_game, (0, bg_y - cao))
        bg_y += bg_speed
        if bg_y >= cao:
            bg_y = 0

        # ======= Hệ thống báo động và sinh Boss =======
        boss_trigger_scores = {1: 1000, 2: 4000}
        current_time = pygame.time.get_ticks()
        
        # Kiểm tra điều kiện kích hoạt báo động boss
        if (boss_stage in boss_trigger_scores and not boss_dang_ra and 
            not boss_warning_active and hud.score >= boss_trigger_scores[boss_stage]):
            # Bắt đầu báo động
            boss_warning_active = True
            boss_warning_start_time = current_time
            boss_warning_stage = boss_stage
            # Phát âm thanh báo động
            if warning_sound:
                warning_sound.play()
            print(f"🚨 CẢNH BÁO: BOSS {boss_stage} SẮP XUẤT HIỆN! 🚨")
        
        # Xử lý báo động đang diễn ra
        if boss_warning_active:
            warning_elapsed = current_time - boss_warning_start_time
            
            # Phát âm thanh báo động mỗi 0.5 giây
            if warning_sound and warning_elapsed % 500 < 50:
                warning_sound.play()
            
            if warning_elapsed >= boss_warning_duration:
                # Hết thời gian báo động, spawn boss
                for enemy in dichs:
                    enemy.kill()
                boss = Boss(rong // 2, 120, 2, bullet_group=boss_dan, level=boss_warning_stage)
                tatca_sprites.add(boss)
                boss_nhom.add(boss)
                boss_dang_ra = True
                boss_warning_active = False
                print(f"🔥 BOSS {boss_warning_stage} XUẤT HIỆN!!! 🔥")

        # ======= Sinh địch =======
        if not boss_dang_ra:
            current_delay = delay_sinh_dich
            if hud.score > 500:
                current_delay = 700
            if hud.score > 1000:
                current_delay = 500

            if thoi_gian_sinh_dich >= current_delay and len(dichs) < max_dich:
                thoi_gian_sinh_dich = 0
                for _ in range(random.randint(2, 4)):
                    x = random.randint(20, rong - 20)
                    y = random.randint(-100, -40)
                    base_speed = random.randint(2, 4)
                    if hud.score > 500:
                        base_speed += 1
                    if hud.score > 1000:
                        base_speed += 1
                        bg_speed += 0.5
                    elapsed = (pygame.time.get_ticks() - start_time) // 10000
                    enemy_level = min(1 + elapsed, 2)
                    random_level = random.randint(1, enemy_level)
                    new_enemy = Dich(x, y, base_speed, level=random_level)
                    tatca_sprites.add(new_enemy)
                    dichs.add(new_enemy)

        # ======= Va chạm =======
        hits = pygame.sprite.groupcollide(dan_nguoi_choi, dichs, True, False)
        for bullet, enemies in hits.items():
            for enemy in enemies:
                if enemy.tru_mau(1):
                    enemy.kill()
                    hud.cong_diem(10)
                    item = drop_item(enemy.rect.centerx, enemy.rect.centery, cao)
                    if item:
                        tatca_sprites.add(item)
                        items.add(item)

        hits = pygame.sprite.spritecollide(may_bay, dichs, True)
        for hit in hits:
            may_bay.tim -= 1
            if may_bay.sung_level > 1:
                may_bay.sung_level -= 1
            if may_bay.tim <= 0:
                if game_over_screen(hud.score):
                    return start_game()
                else:
                    running = False

        collected = pygame.sprite.spritecollide(may_bay, items, True)
        for item in collected:
            if item.type == "hp":
                may_bay.tim = min(3, may_bay.tim + 1)
            elif item.type == "power":
                if may_bay.sung_level < 4:
                    may_bay.sung_level += 1
                elif may_bay.sung_level == 4:
                    may_bay.sung_level = 5
                    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

        # ======= Boss =======
        if boss:
            boss_hits = pygame.sprite.spritecollide(boss, dan_nguoi_choi, True)
            for _ in boss_hits:
                boss.tru_mau(5)
            if boss.hp <= 0:
                hud.cong_diem(500 * boss_stage)
                boss.stop_boss_music()  # Dừng nhạc boss khi boss chết
                boss.kill()
                boss_dang_ra = False
                boss = None
                print(f"💥 BOSS {boss_stage} BỊ TIÊU DIỆT! 🔥")
                
                # Khôi phục nhạc nền sau khi boss chết
                try:
                    music_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "BackgroundMusic", "awestruck.wav")
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    print("🎵 Đã khôi phục nhạc nền!")
                except pygame.error as e:
                    print(f"⚠️ Lỗi khi khôi phục nhạc nền: {e}")
                
                for _ in range(3):
                    item = drop_item(rong // 2 + random.randint(-40, 40), 200 + random.randint(-30, 30), cao)
                    if item:
                        tatca_sprites.add(item)
                        items.add(item)
                boss_stage += 1
                # Giới hạn boss_stage không vượt quá 2 (đã xóa boss 3)
                if boss_stage > 2:
                    boss_stage = 2

        boss_bullet_hits = pygame.sprite.spritecollide(may_bay, boss_dan, True)
        if boss_bullet_hits:
            may_bay.tim -= 1
            if may_bay.tim <= 0:
                if game_over_screen(hud.score):
                    return start_game()
                else:
                    running = False

        # ======= Vẽ =======
        tatca_sprites.draw(man_hinh)
        dan_nguoi_choi.draw(man_hinh)
        boss_dan.draw(man_hinh)
        items.draw(man_hinh)
        if boss:
            boss.ve(man_hinh)
        may_bay.ve_hieu_ung(man_hinh)
        hud.ve(man_hinh)
        
        # Vẽ thông báo báo động boss (nếu có)
        if boss_warning_active:
            warning_elapsed = pygame.time.get_ticks() - boss_warning_start_time
            draw_boss_warning(man_hinh, boss_warning_stage, warning_elapsed)
        
        pygame.display.flip()

# ==================== VÒNG LẶP CHÍNH ====================
while True:
    if main_menu():
        start_game()
