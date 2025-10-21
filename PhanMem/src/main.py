import pygame
import random
import os
import sys
import math
from highscores import add_score_with_name, load_highscores, clear_highscores
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, RED, FPS
from player import Player
from enemy import Enemy
from hud import Hud
from item import Item, drop_item
from boss import Boss
from explosion import create_explosion, create_boss_explosion

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PLANE SHOOTER")
clock = pygame.time.Clock()

# ======== ĐƯỜNG DẪN ẢNH ========
assets_path = os.path.join(os.path.dirname(__file__), "..", "assets", "image", "scrollbackground")
# Default background (required)
bg_default_path = os.path.join(assets_path, "scroll_background.png")
bg_menu_path = os.path.join(assets_path, "game-ban-may-bay-5.jpg")
bg_default = pygame.image.load(bg_default_path).convert()
bg_default = pygame.transform.scale(bg_default, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Optional tiered backgrounds (you can add these images into the folder):
bg_mid_path = os.path.join(assets_path, "scroll_background_mid.png")
bg_high_path = os.path.join(assets_path, "hinh-nen-vu-tru-1.png")
# Đổi background 1000 điểm 
bg_1000_path = os.path.join(assets_path, "hinh-nen-vu-tru-1.jpg")
# Đổi background 3000 điểm (file `3000.jpg`)
bg_3000_path = os.path.join(assets_path, "3000.jpg")


if os.path.exists(bg_mid_path):
    bg_mid = pygame.image.load(bg_mid_path).convert()
    bg_mid = pygame.transform.scale(bg_mid, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    bg_mid = bg_default

if os.path.exists(bg_high_path):
    bg_high = pygame.image.load(bg_high_path).convert()
    bg_high = pygame.transform.scale(bg_high, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    bg_high = bg_default

# load bg_1000 (Webb) if present
if os.path.exists(bg_1000_path):
    try:
        bg_1000 = pygame.image.load(bg_1000_path).convert()
        bg_1000 = pygame.transform.scale(bg_1000, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        bg_1000 = None
else:
    bg_1000 = None

# load bg_3000 if present
if os.path.exists(bg_3000_path):
    try:
        bg_3000 = pygame.image.load(bg_3000_path).convert()
        bg_3000 = pygame.transform.scale(bg_3000, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        bg_3000 = None
else:
    bg_3000 = None

if os.path.exists(bg_menu_path):
    bg_menu = pygame.image.load(bg_menu_path).convert()
    bg_menu = pygame.transform.scale(bg_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    bg_menu = bg_default

#ảnh game over
bg_over_path = os.path.join(assets_path, "backgroundmenu.jpg")
if os.path.exists(bg_over_path):
    bg_over = pygame.image.load(bg_over_path).convert()
    bg_over = pygame.transform.scale(bg_over, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    bg_over = bg_menu

# optional boss background
bg_boss_path = os.path.join(assets_path, "hinh-nen-vu-tru-1.png")
if os.path.exists(bg_boss_path):
    bg_boss = pygame.image.load(bg_boss_path).convert()
    bg_boss = pygame.transform.scale(bg_boss, (SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    # fallback to a more intense background if boss image not present
    bg_boss = bg_high

# cuối trò chơi background - thử các ảnh có sẵn
bg_endgame_path = os.path.join(assets_path, "vutru.jpg")
# Backup: thử game_over.png trong endgame
bg_endgame_path2 = os.path.join(os.path.dirname(__file__), "..", "assets", "image", "endgame", "game_over.png")
if os.path.exists(bg_endgame_path):
    try:
        bg_endgame = pygame.image.load(bg_endgame_path).convert()
        bg_endgame = pygame.transform.scale(bg_endgame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print(f"Loaded endgame image from: {bg_endgame_path}")
    except Exception as e:
        print(f"Error loading endgame image: {e}")
        bg_endgame = None
elif os.path.exists(bg_endgame_path2):
    try:
        bg_endgame = pygame.image.load(bg_endgame_path2).convert()
        bg_endgame = pygame.transform.scale(bg_endgame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print(f"Loaded endgame image from: {bg_endgame_path2}")
    except Exception as e:
        print(f"Error loading endgame image: {e}")
        bg_endgame = None
else:
    print(f"Endgame image not found at: {bg_endgame_path} or {bg_endgame_path2}")
    bg_endgame = None

# Tạo background endgame tự làm nếu không load được ảnh
if bg_endgame is None:
    print("Creating custom endgame background...")
    bg_endgame = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Tạo gradient background từ đen đến xanh dương đậm
    for y in range(SCREEN_HEIGHT):
        color_intensity = int(y / SCREEN_HEIGHT * 100)  # 0 -> 100
        color = (0, 0, color_intensity)  # Gradient xanh dương
        pygame.draw.line(bg_endgame, color, (0, y), (SCREEN_WIDTH, y))
    
    # Thêm một số ngôi sao
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        brightness = random.randint(100, 255)
        pygame.draw.circle(bg_endgame, (brightness, brightness, brightness), (x, y), 1)
    
    print("Custom endgame background created successfully")

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

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180))
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

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
        screen.blit(bg_menu, (0, 0))
        screen.blit(title_text, title_rect)
        # no record on menu
        screen.blit(play_text, play_rect)
        screen.blit(hs_text, hs_rect)
        screen.blit(exit_text, exit_rect)
        pygame.display.flip()
        clock.tick(FPS)


def highscores_screen():
    font = pygame.font.SysFont("Arial", 36)
    title = font.render("HIGHSCORES", True, (255, 215, 0))
    back_text = font.render("BACK", True, (255, 255, 255))

    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2 , SCREEN_HEIGHT - 60))

    hs_font = pygame.font.SysFont("Arial", 28)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title, title_rect)

        highs = load_highscores()
        for i, e in enumerate(highs):
            txt = hs_font.render(f"{i+1}. {e.get('name','---')} - {e.get('score',0)}", True, (255, 215, 0))
            rect = txt.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 34))
            screen.blit(txt, rect)

        screen.blit(back_text, back_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return


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

    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180))
    prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
    retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 210))

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
            screen.blit(bg_over, (0, 0))
        except Exception:
            screen.fill((0, 0, 0))

        # semi-transparent overlay to improve readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # show top record (if any) ABOVE the "Your Score" text
        if top_record:
            rec_surf = hs_font.render(f"RECORD: {top_record.get('name','---')} - {top_record.get('score',0)}", True, (255, 215, 0))
            # place it above the score_text
            rec_rect = rec_surf.get_rect(center=(SCREEN_WIDTH // 2, score_rect.top - 40))
            screen.blit(rec_surf, rec_rect)

        screen.blit(score_text, score_rect)
        screen.blit(prompt_text, prompt_rect)

        # draw input box
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 80, 300, 40)
        pygame.draw.rect(screen, (50, 50, 50), input_box)
        pygame.draw.rect(screen, (200, 200, 200), input_box, 2)
        name_surf = hs_font.render(input_name, True, (255, 255, 255))
        screen.blit(name_surf, (input_box.x + 8, input_box.y + 6))

        # (record already drawn above score)

        # show buttons
        screen.blit(retry_text, retry_rect)
        screen.blit(menu_text, menu_rect)
        screen.blit(exit_text, exit_rect)

        if saved:
            ok_text = hs_font.render("Saved! Press PLAY AGAIN or EXIT.", True, (100, 255, 100))
            ok_rect = ok_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            screen.blit(ok_text, ok_rect)
            if new_record:
                nr = hs_font.render("NEW RECORD!", True, (255, 100, 100))
                nr_rect = nr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
                screen.blit(nr, nr_rect)

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

# ==================== MÀN HÌNH KẾT THÚC GAME (HAPPY ENDING) ====================
def happy_ending_screen(score):
    """Hiển thị màn hình kết thúc với ảnh endgame và dòng chữ Happy Ending"""
    global bg_endgame
    
    # Dừng nhạc hiện tại và phát nhạc kết thúc
    pygame.mixer.music.stop()
    endgame_music = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "endgame", "Endgame.wav")
    try:
        pygame.mixer.music.load(endgame_music)
        pygame.mixer.music.play(-1)
    except Exception:
        pass
    
    # Font cho text
    big_font = pygame.font.SysFont("Arial", 72, bold=True)
    medium_font = pygame.font.SysFont("Arial", 48)
    small_font = pygame.font.SysFont("Arial", 36)
    
    # Tạo text
    happy_text = big_font.render("HAPPY ENDING", True, (255, 215, 0))
    congratulations_text = medium_font.render("Congratulations! You defeated all bosses!", True, (255, 255, 255))
    score_text = small_font.render(f"Final Score: {score}", True, (200, 200, 200))
    continue_text = small_font.render("Click anywhere to continue...", True, (100, 255, 100))
    
    # Vị trí text
    happy_rect = happy_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    congratulations_rect = congratulations_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
    
    # Hiệu ứng fade in
    fade_alpha = 0
    fade_speed = 120  # alpha per second
    text_visible = False
    show_time = 0
    
    clock = pygame.time.Clock()
    
    while True:
        dt = clock.tick(60)
        show_time += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and text_visible:
                return  # Trở về menu chính
            if event.type == pygame.KEYDOWN and text_visible:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return  # Trở về menu chính
        
        # Vẽ background endgame
        if bg_endgame:
            screen.blit(bg_endgame, (0, 0))
        else:
            # Nếu không có ảnh endgame, vẽ background đen với hiệu ứng
            screen.fill((0, 0, 0))
        
        # Fade in effect
        if fade_alpha < 255:
            fade_alpha = min(255, fade_alpha + fade_speed * (dt / 1000.0))
        else:
            text_visible = True
        
        # Tạo overlay mờ để text dễ đọc hơn
        if text_visible:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))
        
        # Hiệu ứng nhấp nháy cho text "HAPPY ENDING"
        if text_visible:
            glow_alpha = int(255 * (0.7 + 0.3 * math.sin(show_time * 0.005)))
            
            # Vẽ text với hiệu ứng glow
            happy_surface = happy_text.copy()
            happy_surface.set_alpha(glow_alpha)
            screen.blit(happy_surface, happy_rect)
            
            # Vẽ các text khác
            congratulations_surface = congratulations_text.copy()
            congratulations_surface.set_alpha(fade_alpha)
            screen.blit(congratulations_surface, congratulations_rect)
            
            score_surface = score_text.copy()
            score_surface.set_alpha(fade_alpha)
            screen.blit(score_surface, score_rect)
            
            # Text continue nhấp nháy
            if (show_time // 500) % 2 == 0:
                continue_surface = continue_text.copy()
                continue_surface.set_alpha(fade_alpha)
                screen.blit(continue_surface, continue_rect)
        
        pygame.display.flip()

# ==================== HÀM HIỂN THỊ THÔNG BÁO BOSS ====================
def draw_boss_warning(screen, boss_stage, warning_time):
    """Hiển thị thông báo báo động boss"""
    # Tạo hiệu ứng nhấp nháy
    alpha = int(255 * (0.5 + 0.5 * math.sin(warning_time * 0.01)))
    
    # Tạo surface cho text với alpha
    warning_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    # Vẽ nền đỏ mờ
    red_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
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
    main_rect = main_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
    warning_surface.blit(main_surface, main_rect)
    
    # Text boss
    boss_text = f"BOSS {boss_stage}"
    boss_surface = medium_font.render(boss_text, True, (255, 100, 100))
    boss_surface.set_alpha(alpha)
    boss_rect = boss_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
    warning_surface.blit(boss_surface, boss_rect)
    
    # Text hướng dẫn
    instruction_text = "Prepare For Battle"
    instruction_surface = small_font.render(instruction_text, True, (255, 255, 255))
    instruction_surface.set_alpha(alpha)
    instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
    warning_surface.blit(instruction_surface, instruction_rect)
    
    # Đếm ngược
    remaining_time = max(0, 3 - warning_time // 1000)
    if remaining_time > 0:
        countdown_text = f"{remaining_time + 1}"
        countdown_surface = big_font.render(countdown_text, True, (255, 0, 0))
        countdown_surface.set_alpha(255)
        countdown_rect = countdown_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        warning_surface.blit(countdown_surface, countdown_rect)
    
    screen.blit(warning_surface, (0, 0))

# ==================== HÀM KHỞI TẠO GAME ====================
def start_game():
    music_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "BackgroundMusic", "awestruck.wav")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    items = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    explosions = pygame.sprite.Group()  # Nhóm hiệu ứng nổ

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, 5, player_bullets)
    all_sprites.add(player)

    hud = Hud(player)

    # ======= Load âm thanh báo động =======
    try:
        warning_sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sound", "Shot", "Laser Shot.wav")
        warning_sound = pygame.mixer.Sound(warning_sound_path)
        warning_sound.set_volume(0.8)
    except:
        warning_sound = None
        print("⚠️ Không thể load âm thanh báo động")

    spawn_timer = 0
    spawn_delay = 1000
    max_enemies = 30
    bg_y = 0
    bg_speed = 2
    start_time = pygame.time.get_ticks()

    boss_stage = 1
    boss = None
    boss_dang_ra = False
    # track which boss stages have already been spawned to avoid repeats
    used_boss_stages = set()

    # ======= Hệ thống báo động boss =======
    boss_warning_active = False
    boss_warning_start_time = 0
    boss_warning_duration = 3000  # 3 giây báo động
    boss_warning_stage = 0  # Stage của boss sắp xuất hiện

    # ======= Hệ thống tạm dừng =======
    paused = False

    running = True
    while running:
        dt = clock.tick(FPS)
        spawn_timer += dt

        # ======= Sự kiện =======
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            if event.type == pygame.USEREVENT + 1:
                player.gun_level = 4
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)

        # Nếu đang pause, chỉ hiển thị màn hình pause và bỏ qua phần còn lại
        if paused:
            # Vẽ game hiện tại
            screen.blit(bg_current, (0, bg_y))
            screen.blit(bg_current, (0, bg_y - SCREEN_HEIGHT))
            all_sprites.draw(screen)
            player_bullets.draw(screen)
            boss_bullets.draw(screen)
            items.draw(screen)
            if boss:
                boss.draw(screen)
            player.draw_effect(screen)
            hud.draw(screen)
            
            # Overlay mờ
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            # Text PAUSED
            pause_font = pygame.font.SysFont("Arial", 72, bold=True)
            pause_text = pause_font.render("PAUSED", True, (255, 255, 0))
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(pause_text, pause_rect)
            
            # Hướng dẫn
            instruction_font = pygame.font.SysFont("Arial", 36)
            instruction_text = instruction_font.render("Press P or ESC to resume", True, (255, 255, 255))
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(instruction_text, instruction_rect)
            
            # Tạo các nút
            button_font = pygame.font.SysFont("Arial", 42)
            resume_text = button_font.render("RESUME", True, (0, 255, 0))
            home_text = button_font.render("HOME", True, (255, 255, 255))
            exit_text = button_font.render("EXIT", True, (255, 100, 100))
            
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            home_rect = home_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180))
            
            # Làm nổi bật nút khi hover
            mouse_pos = pygame.mouse.get_pos()
            if resume_rect.collidepoint(mouse_pos):
                resume_text = button_font.render("RESUME", True, (100, 255, 100))
            if home_rect.collidepoint(mouse_pos):
                home_text = button_font.render("HOME", True, (255, 255, 0))
            if exit_rect.collidepoint(mouse_pos):
                exit_text = button_font.render("EXIT", True, (255, 150, 150))
            
            # Vẽ các nút
            screen.blit(resume_text, resume_rect)
            screen.blit(home_text, home_rect)
            screen.blit(exit_text, exit_rect)
            
            pygame.display.flip()
            
            # Xử lý sự kiện trong pause
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        paused = False
                        pygame.mixer.music.unpause()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_rect.collidepoint(event.pos):
                        paused = False
                        pygame.mixer.music.unpause()
                    elif home_rect.collidepoint(event.pos):
                        # Về menu chính
                        pygame.mixer.music.stop()
                        return
                    elif exit_rect.collidepoint(event.pos):
                        # Lưu điểm và thoát
                        pygame.mixer.music.stop()
                        if game_over_screen(hud.score):
                            return start_game()
                        else:
                            return            
            continue

        all_sprites.update()
        player_bullets.update()
        items.update()
        boss_bullets.update()
        explosions.update()  # Cập nhật hiệu ứng nổ
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

        screen.blit(bg_current, (0, bg_y))
        screen.blit(bg_current, (0, bg_y - SCREEN_HEIGHT))
        bg_y += bg_speed
        if bg_y >= SCREEN_HEIGHT:
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
                for enemy in enemies:
                    enemy.kill()
                boss = Boss(SCREEN_WIDTH // 2, 120, 2, bullet_group=boss_bullets, level=boss_warning_stage)
                all_sprites.add(boss)
                boss_group.add(boss)
                boss_dang_ra = True
                boss_warning_active = False
                # mark this stage as used so it won't be spawned again
                try:
                    used_boss_stages.add(boss_warning_stage)
                except Exception:
                    pass
                print(f"🔥 BOSS {boss_warning_stage} XUẤT HIỆN!!! 🔥")

        # ======= Sinh địch =======
        if not boss_dang_ra:
            current_delay = spawn_delay
            if hud.score > 500:
                current_delay = 700
            if hud.score > 1000:
                current_delay = 500

            if spawn_timer >= current_delay and len(enemies) < max_enemies:
                spawn_timer = 0
                
                # Tính số địch cần spawn (không vượt max_dich)
                to_spawn = random.randint(2, 4)
                to_spawn = min(to_spawn, max_enemies - len(enemies))
                
                # Điều chỉnh bg_speed một lần (không trong vòng lặp)
                if hud.score > 1000:
                    bg_speed = min(bg_speed + 0.1, 5.0)  # cap tối đa 5.0
                
                for _ in range(to_spawn):
                    x = random.randint(20, SCREEN_WIDTH - 20)
                    # Tránh spawn quá gần player
                    if abs(x - player.rect.centerx) < 60:
                        offset = random.choice([-100, 100])
                        x = max(20, min(SCREEN_WIDTH - 20, player.rect.centerx + offset))
                    
                    y = random.randint(-120, -40)
                    base_speed = random.randint(2, 4)
                    if hud.score > 500:
                        base_speed += 1
                    if hud.score > 1000:
                        base_speed += 1                    # Cap tốc độ tối đa
                    base_speed = min(base_speed, 8)
                    
                    elapsed = (pygame.time.get_ticks() - start_time) // 10000
                    enemy_level = min(1 + elapsed, 2)
                    random_level = random.randint(1, enemy_level)
                    new_enemy = Enemy(x, y, base_speed, level=random_level)
                    all_sprites.add(new_enemy)
                    enemies.add(new_enemy)

        # ======= Va chạm =======
        hits = pygame.sprite.groupcollide(player_bullets, enemies, True, False)
        for bullet, enemies_in in hits.items():
            for enemy in enemies_in:
                if enemy.take_damage(1):                    # Tạo hiệu ứng nổ khi enemy chết
                    explosion = create_explosion(enemy.rect.centerx, enemy.rect.centery, "normal")
                    explosions.add(explosion)
                    
                    enemy.kill()
                    hud.add_score(10)
                    item = drop_item(enemy.rect.centerx, enemy.rect.centery, SCREEN_HEIGHT)
                    if item:
                        all_sprites.add(item)
                        items.add(item)

        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            # Tạo hiệu ứng nổ khi player va chạm với enemy
            explosion = create_explosion(hit.rect.centerx, hit.rect.centery, "large")
            explosions.add(explosion)
            
            player.lives -= 1
            if player.gun_level > 1:
                player.gun_level -= 1
            if player.lives <= 0:
                if game_over_screen(hud.score):
                    return start_game()
                else:
                    running = False

        collected = pygame.sprite.spritecollide(player, items, True)
        for item in collected:
            if item.type == "hp":
                player.lives = min(3, player.lives + 1)
            elif item.type == "power":
                if player.gun_level < 4:
                    player.gun_level += 1
                elif player.gun_level == 4:
                    player.gun_level = 5
                    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)        # ======= Boss =======
        if boss:
            boss_hits = pygame.sprite.spritecollide(boss, player_bullets, True)
            for _ in boss_hits:
                boss.take_damage(5)
            if boss.hp <= 0:
                # capture the level before destroying the boss
                try:
                    _lvl = boss.level
                except Exception:
                    _lvl = None

                # Tạo hiệu ứng nổ đặc biệt cho boss
                boss_explosions = create_boss_explosion(boss.rect.centerx, boss.rect.centery)
                for explosion in boss_explosions:
                    explosions.add(explosion)

                hud.add_score(500 * boss_stage)
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
                    item = drop_item(SCREEN_WIDTH // 2 + random.randint(-40, 40), 200 + random.randint(-30, 30), SCREEN_HEIGHT)
                    if item:
                        all_sprites.add(item)
                        items.add(item)

                boss_stage += 1
                # Giới hạn boss_stage không vượt quá 2
                if boss_stage > 2:
                    boss_stage = 2                # If this was boss level 2, prepare for happy ending but wait for explosions
                if _lvl == 2:
                    try:
                        # remove any remaining boss bullets
                        for b in list(boss_bullets):
                            b.kill()
                        boss_bullets.empty()
                    except Exception:
                        pass
                    
                    print("🎉 HAPPY ENDING! Bạn đã tiêu diệt tất cả boss! 🎉")
                    
                    # Delay để hiệu ứng nổ có thời gian diễn ra
                    explosion_delay_start = pygame.time.get_ticks()
                    explosion_delay_duration = 3000  # 3 giây để xem hiệu ứng nổ
                    
                    # Vòng lặp chờ hiệu ứng nổ
                    while pygame.time.get_ticks() - explosion_delay_start < explosion_delay_duration:
                        dt = clock.tick(FPS)
                        
                        # Cập nhật và vẽ game bình thường nhưng không sinh địch mới
                        all_sprites.update()
                        explosions.update()
                        
                        # Vẽ game
                        screen.blit(bg_current, (0, bg_y))
                        screen.blit(bg_current, (0, bg_y - SCREEN_HEIGHT))
                        bg_y += bg_speed
                        if bg_y >= SCREEN_HEIGHT:
                            bg_y = 0
                            
                        all_sprites.draw(screen)
                        player_bullets.draw(screen)
                        items.draw(screen)
                        explosions.draw(screen)  # Vẽ hiệu ứng nổ
                        player.draw_effect(screen)
                        hud.draw(screen)
                        
                        # Text thông báo kết thúc game
                        end_font = pygame.font.SysFont("Arial", 48, bold=True)
                        end_text = end_font.render("FINAL BOSS DEFEATED!", True, (255, 215, 0))
                        end_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                        
                        # Tạo hiệu ứng nhấp nháy
                        elapsed_time = pygame.time.get_ticks() - explosion_delay_start
                        if (elapsed_time // 300) % 2 == 0:  # Nhấp nháy mỗi 300ms
                            screen.blit(end_text, end_rect)
                        
                        pygame.display.flip()
                        
                        # Xử lý sự kiện để có thể thoát nếu cần
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                    
                    # Hiển thị màn hình Happy Ending sau khi hiệu ứng nổ kết thúc
                    try:
                        happy_ending_screen(hud.score)
                    except Exception as e:
                        print(f"Lỗi khi hiển thị happy ending: {e}")
                    
                    # Sau khi xem happy ending, vào màn hình game over để lưu điểm
                    try:
                        if game_over_screen(hud.score):
                            return start_game()
                        else:
                            return
                    except Exception:
                        return

        boss_bullet_hits = pygame.sprite.spritecollide(player, boss_bullets, True)
        if boss_bullet_hits:
            player.lives -= 1
            if player.lives <= 0:
                if game_over_screen(hud.score):
                    return start_game()
                else:
                    running = False        # ======= Vẽ =======
        all_sprites.draw(screen)
        player_bullets.draw(screen)
        boss_bullets.draw(screen)
        items.draw(screen)
        explosions.draw(screen)  # Vẽ hiệu ứng nổ
        if boss:
            boss.draw(screen)
        player.draw_effect(screen)
        hud.draw(screen)
        
        # Vẽ thông báo báo động boss (nếu có)
        if boss_warning_active:
            warning_elapsed = pygame.time.get_ticks() - boss_warning_start_time
            draw_boss_warning(screen, boss_warning_stage, warning_elapsed)
        
        pygame.display.flip()

# ==================== VÒNG LẶP CHÍNH ====================
while True:
    if main_menu():
        start_game()
