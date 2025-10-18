import pygame
import random
import os
import sys
import math
from highscores import add_score_with_name, load_highscores, clear_highscores
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
# Default background (required)
bg_default_path = os.path.join(assets_path, "scroll_background.png")
bg_menu_path = os.path.join(assets_path, "game-ban-may-bay-5.jpg")
bg_default = pygame.image.load(bg_default_path).convert()
bg_default = pygame.transform.scale(bg_default, (rong, cao))

# Optional tiered backgrounds (you can add these images into the folder):
bg_mid_path = os.path.join(assets_path, "scroll_background_mid.png")
bg_high_path = os.path.join(assets_path, "hinh-nen-vu-tru-1.png")
# Đổi background 1000 điểm 
bg_1000_path = os.path.join(assets_path, "hinh-nen-vu-tru-1.jpg")
# Đổi background 3000 điểm (file `3000.jpg`)
bg_3000_path = os.path.join(assets_path, "3000.jpg")


if os.path.exists(bg_mid_path):
    bg_mid = pygame.image.load(bg_mid_path).convert()
    bg_mid = pygame.transform.scale(bg_mid, (rong, cao))
else:
    bg_mid = bg_default

if os.path.exists(bg_high_path):
    bg_high = pygame.image.load(bg_high_path).convert()
    bg_high = pygame.transform.scale(bg_high, (rong, cao))
else:
    bg_high = bg_default

# load bg_1000 (Webb) if present
if os.path.exists(bg_1000_path):
    try:
        bg_1000 = pygame.image.load(bg_1000_path).convert()
        bg_1000 = pygame.transform.scale(bg_1000, (rong, cao))
    except Exception:
        bg_1000 = None
else:
    bg_1000 = None

# load bg_3000 if present
if os.path.exists(bg_3000_path):
    try:
        bg_3000 = pygame.image.load(bg_3000_path).convert()
        bg_3000 = pygame.transform.scale(bg_3000, (rong, cao))
    except Exception:
        bg_3000 = None
else:
    bg_3000 = None

if os.path.exists(bg_menu_path):
    bg_menu = pygame.image.load(bg_menu_path).convert()
    bg_menu = pygame.transform.scale(bg_menu, (rong, cao))
else:
    bg_menu = bg_default

#ảnh game over
bg_over_path = os.path.join(assets_path, "backgroundmenu.jpg")
if os.path.exists(bg_over_path):
    bg_over = pygame.image.load(bg_over_path).convert()
    bg_over = pygame.transform.scale(bg_over, (rong, cao))
else:
    bg_over = bg_menu

# optional boss background
bg_boss_path = os.path.join(assets_path, "hinh-nen-vu-tru-1.png")
if os.path.exists(bg_boss_path):
    bg_boss = pygame.image.load(bg_boss_path).convert()
    bg_boss = pygame.transform.scale(bg_boss, (rong, cao))
else:
    # fallback to a more intense background if boss image not present
    bg_boss = bg_high

# cuối trò chơi background
bg_endgame_path = os.path.join(assets_path, "endgame.jpg")
if os.path.exists(bg_endgame_path):
    try:
        bg_endgame = pygame.image.load(bg_endgame_path).convert()
        bg_endgame = pygame.transform.scale(bg_endgame, (rong, cao))
    except Exception:
        bg_endgame = None
else:
    bg_endgame = None

# ==================== MÀN HÌNH MENU ====================
def main_menu():
    menu_music = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "endgame", "Endgame.wav")
    try:
        pygame.mixer.music.load(menu_music)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    font = pygame.font.SysFont("Arial", 48, bold=True)
    title_text = font.render("PLANE SHOOTER", True, (255, 215, 0))
    # (record display removed from menu per request)
    play_text = font.render("NEW GAME", True, (255, 215, 0))
    hs_text = font.render("HIGHSCORES", True, (255, 215, 0))
    exit_text = font.render("EXIT", True, (255, 215, 0))

    title_rect = title_text.get_rect(center=(rong // 2, cao // 2 - 180))
    play_rect = play_text.get_rect(center=(rong // 2, cao // 2 - 60))
    hs_rect = hs_text.get_rect(center=(rong // 2, cao // 2 + 20))
    exit_rect = exit_text.get_rect(center=(rong // 2, cao // 2 + 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    print("[DEBUG] main_menu: NEW GAME clicked", event.pos)
                    return True
                if hs_rect.collidepoint(event.pos):
                    print("[DEBUG] main_menu: HIGHSCORES clicked", event.pos)
                    highscores_screen()
                if exit_rect.collidepoint(event.pos):
                    print("[DEBUG] main_menu: EXIT clicked", event.pos)
                    pygame.quit()
                    sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        play_text = font.render("NEW GAME", True, (255, 255, 0) if play_rect.collidepoint(mouse_pos) else (255, 215, 0))
        hs_text = font.render("HIGHSCORES", True, (255, 255, 0) if hs_rect.collidepoint(mouse_pos) else (255, 215, 0))
        exit_text = font.render("EXIT", True, (255, 255, 0) if exit_rect.collidepoint(mouse_pos) else (255, 215, 0))

        # Vẽ nền menu
        man_hinh.blit(bg_menu, (0, 0))
        man_hinh.blit(title_text, title_rect)
        # no record on menu
        man_hinh.blit(play_text, play_rect)
        man_hinh.blit(hs_text, hs_rect)
        man_hinh.blit(exit_text, exit_rect)
        pygame.display.flip()
        dong_ho.tick(FPS)


def highscores_screen():
    font = pygame.font.SysFont("Arial", 36)
    title = font.render("HIGHSCORES", True, (255, 215, 0))
    back_text = font.render("BACK", True, (255, 255, 255))
    clear_text = font.render("CLEAR", True, (255, 100, 100))

    title_rect = title.get_rect(center=(rong // 2, 80))
    back_rect = back_text.get_rect(center=(rong // 2 - 100, cao - 60))
    clear_rect = clear_text.get_rect(center=(rong // 2 + 100, cao - 60))

    hs_font = pygame.font.SysFont("Arial", 28)

    while True:
        man_hinh.fill((0, 0, 0))
        man_hinh.blit(title, title_rect)

        highs = load_highscores()
        for i, e in enumerate(highs):
            txt = hs_font.render(f"{i+1}. {e.get('name','---')} - {e.get('score',0)}", True, (255, 215, 0))
            rect = txt.get_rect(center=(rong // 2, 150 + i * 34))
            man_hinh.blit(txt, rect)

        man_hinh.blit(back_text, back_rect)
        man_hinh.blit(clear_text, clear_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                if clear_rect.collidepoint(event.pos):
                    clear_highscores()


# ==================== MÀN HÌNH GAME OVER ====================
def game_over_screen(score):
    gameover_music = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "endgame", "Endgame.wav")
    try:
        pygame.mixer.music.load(gameover_music)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    font_small = pygame.font.SysFont("Arial", 36)
    hs_font = pygame.font.SysFont("Arial", 28)

    score_text = font_small.render(f"Your Score: {score}", True, (255, 255, 255))
    prompt_text = font_small.render("Enter your name and press Enter:", True, (200, 200, 200))
    retry_text = font_small.render("PLAY AGAIN", True, (0, 255, 0))
    menu_text = font_small.render("MENU", True, (255, 255, 255))
    exit_text = font_small.render("EXIT", True, (255, 255, 255))

    score_rect = score_text.get_rect(center=(rong // 2, cao // 2 - 180))
    prompt_rect = prompt_text.get_rect(center=(rong // 2, cao // 2 - 120))
    retry_rect = retry_text.get_rect(center=(rong // 2, cao // 2 + 110))
    menu_rect = menu_text.get_rect(center=(rong // 2, cao // 2 + 160))
    exit_rect = exit_text.get_rect(center=(rong // 2, cao // 2 + 210))

    input_name = ""
    input_active = True
    saved = False
    new_record = False

    # get current top record
    top_record = None
    try:
        hs_all = load_highscores()
        if hs_all:
            top_record = hs_all[0]
    except Exception:
        top_record = None

    while True:
        # draw background (use bg_menu as requested)
        try:
            man_hinh.blit(bg_over, (0, 0))
        except Exception:
            man_hinh.fill((0, 0, 0))

        # semi-transparent overlay to improve readability
        overlay = pygame.Surface((rong, cao), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        man_hinh.blit(overlay, (0, 0))

        # show top record (if any) ABOVE the "Your Score" text
        if top_record:
            rec_surf = hs_font.render(f"RECORD: {top_record.get('name','---')} - {top_record.get('score',0)}", True, (255, 215, 0))
            # place it above the score_text
            rec_rect = rec_surf.get_rect(center=(rong // 2, score_rect.top - 40))
            man_hinh.blit(rec_surf, rec_rect)

        man_hinh.blit(score_text, score_rect)
        man_hinh.blit(prompt_text, prompt_rect)

        # draw input box
        input_box = pygame.Rect(rong // 2 - 150, cao // 2 - 80, 300, 40)
        pygame.draw.rect(man_hinh, (50, 50, 50), input_box)
        pygame.draw.rect(man_hinh, (200, 200, 200), input_box, 2)
        name_surf = hs_font.render(input_name, True, (255, 255, 255))
        man_hinh.blit(name_surf, (input_box.x + 8, input_box.y + 6))

        # (record already drawn above score)

        # show buttons
        man_hinh.blit(retry_text, retry_rect)
        man_hinh.blit(menu_text, menu_rect)
        man_hinh.blit(exit_text, exit_rect)

        if saved:
            ok_text = hs_font.render("Saved! Press PLAY AGAIN or EXIT.", True, (100, 255, 100))
            ok_rect = ok_text.get_rect(center=(rong // 2, cao // 2 + 80))
            man_hinh.blit(ok_text, ok_rect)
            if new_record:
                nr = hs_font.render("NEW RECORD!", True, (255, 100, 100))
                nr_rect = nr.get_rect(center=(rong // 2, cao // 2 - 80))
                man_hinh.blit(nr, nr_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    print("[DEBUG] game_over_screen: PLAY AGAIN clicked", event.pos)
                    return True
                if menu_rect.collidepoint(event.pos):
                    print("[DEBUG] game_over_screen: MENU clicked", event.pos)
                    return False
                if exit_rect.collidepoint(event.pos):
                    print("[DEBUG] game_over_screen: EXIT clicked", event.pos)
                    pygame.quit()
                    sys.exit()
                # click input box to activate
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN and input_active and not saved:
                if event.key == pygame.K_RETURN:
                    name_to_save = input_name.strip() or "ANON"
                    try:
                        # determine if this is a new record
                        previous_top = top_record.get('score', -1) if top_record else -1
                        if score > previous_top:
                            new_record = True
                        add_score_with_name(name_to_save, score)
                        saved = True
                        # reload top_record
                        try:
                            hs_all = load_highscores()
                            top_record = hs_all[0] if hs_all else None
                        except Exception:
                            top_record = None
                    except Exception:
                        saved = False
                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]
                else:
                    # limit name length
                    if len(input_name) < 20:
                        char = event.unicode
                        if char.isprintable():
                            input_name += char

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
    
    # Đếm ngược
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
    # track which boss stages have already been spawned to avoid repeats
    used_boss_stages = set()
    # endgame fade state (for boss final reveal)
    endgame_fade_active = False
    endgame_alpha = 0
    endgame_fade_speed = 120.0  # alpha per second

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

        # ======= Cuộn nền (chọn background theo điểm) =======
        # Immediate boss background when reaching a score threshold (e.g., 1000),
        # or when boss warning/active flags are set.
        score_now = hud.get_score() if hasattr(hud, 'get_score') else getattr(hud, 'score', 0)
        # Prefer tiered special backgrounds when reaching milestones:
        #  - score >= 3000 -> bg_3000
        #  - score >= 1000 -> bg_1000
        # Otherwise, if boss warning/active use bg_boss, else use tiered bg
        if score_now >= 2500:
            if 'bg_3000' in globals() and bg_3000 is not None:
                bg_current = bg_3000
            elif 'bg_1000' in globals() and bg_1000 is not None:
                bg_current = bg_1000
            else:
                bg_current = bg_boss
        elif score_now >= 1000 or boss_warning_active or boss_dang_ra:
            if 'bg_1000' in globals() and bg_1000 is not None:
                bg_current = bg_1000
            else:
                bg_current = bg_boss
        else:
            tier = hud.background_tier() if hasattr(hud, 'background_tier') else 0
            if tier == 2:
                bg_current = bg_high
            elif tier == 1:
                bg_current = bg_mid
            else:
                bg_current = bg_default

        man_hinh.blit(bg_current, (0, bg_y))
        man_hinh.blit(bg_current, (0, bg_y - cao))
        bg_y += bg_speed
        if bg_y >= cao:
            bg_y = 0

        # ======= Hệ thống báo động và sinh Boss =======
        boss_trigger_scores = {1: 1000, 2: 4000}
        current_time = pygame.time.get_ticks()
        
        # Kiểm tra điều kiện kích hoạt báo động boss
        if (boss_stage in boss_trigger_scores and not boss_dang_ra and 
            not boss_warning_active and hud.score >= boss_trigger_scores[boss_stage]
            and boss_stage not in used_boss_stages):
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
                # mark this stage as used so it won't be spawned again
                try:
                    used_boss_stages.add(boss_warning_stage)
                except Exception:
                    pass
                print(f"🔥 BOSS {boss_warning_stage} XUẤT HIỆN!!! 🔥")

        # If boss exists and is level 2, check for endgame fade trigger (<=25% HP)
        if boss and getattr(boss, 'level', 0) == 2:
            try:
                if boss.hp <= 0.25 * boss.max_hp and not endgame_fade_active:
                    endgame_fade_active = True
                    endgame_alpha = 0
                    print("🔔 Endgame fade started (boss <=25% HP)")
            except Exception:
                pass

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
                # capture the level before destroying the boss
                try:
                    _lvl = boss.level
                except Exception:
                    _lvl = None

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
                # Giới hạn boss_stage không vượt quá 2
                if boss_stage > 2:
                    boss_stage = 2

                # If this was boss level 2, stop boss bullets, show endgame image and end the run
                if _lvl == 2:
                    try:
                        endgame_triggered = True
                    except Exception:
                        pass
                    try:
                        # remove any remaining boss bullets
                        for b in list(boss_dan):
                            b.kill()
                        boss_dan.empty()
                    except Exception:
                        pass

                    # debug: report bg_endgame availability
                    try:
                        bg_present = ('bg_endgame' in globals() and bg_endgame is not None)
                        print(f"[DEBUG] boss death: level={_lvl}, bg_endgame_present={bg_present}")
                    except Exception:
                        print("[DEBUG] boss death: couldn't check bg_endgame")

                    if 'bg_endgame' in globals() and bg_endgame is not None:
                        endgame_fade_active = True
                        endgame_alpha = 255
                        try:
                            print("[DEBUG] Blitting bg_endgame now")
                            man_hinh.blit(bg_endgame, (0, 0))
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            print("[DEBUG] bg_endgame blit + flip done")
                        except Exception as e:
                            print(f"[DEBUG] Failed to blit bg_endgame: {e}")
                    else:
                        print("[DEBUG] bg_endgame not available, skipping blit")

                    # go to game over / highscores flow
                    try:
                        if game_over_screen(hud.score):
                            return start_game()
                        else:
                            return
                    except Exception:
                        return

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
        
        # Vẽ endgame fade (nếu active) - vẽ lên trên cùng
        if 'bg_endgame' in globals() and bg_endgame is not None and endgame_fade_active:
            try:
                # update alpha
                if endgame_alpha < 255:
                    endgame_alpha = min(255, endgame_alpha + endgame_fade_speed * (dt / 1000.0))
                surf = bg_endgame.copy()
                surf.set_alpha(int(endgame_alpha))
                man_hinh.blit(surf, (0, 0))
            except Exception:
                pass

        # Vẽ thông báo báo động boss (nếu có)
        if boss_warning_active:
            warning_elapsed = pygame.time.get_ticks() - boss_warning_start_time
            draw_boss_warning(man_hinh, boss_warning_stage, warning_elapsed)
        
        pygame.display.flip()

# ==================== VÒNG LẶP CHÍNH ====================
while True:
    if main_menu():
        start_game()
