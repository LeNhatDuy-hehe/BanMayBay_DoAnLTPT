import pygame
import random
import os
import sys
from settings import rong, cao, DO, FPS
from player import Player
from enemy import Dich
from hud import Hud
from item import Item, drop_item

pygame.init()
man_hinh = pygame.display.set_mode((rong, cao))
pygame.display.set_caption("PLANE SHOOTER")
dong_ho = pygame.time.Clock()

# ======== PATH & BACKGROUND ========
current_path = os.path.dirname(__file__)
background_path = os.path.join(current_path, "..", "assets", "image", "scrollbackground", "scroll_background.png")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (rong, cao))


# ==================== MÀN HÌNH MENU ====================
def main_menu():
    menu_music = os.path.join(current_path, "..", "assets", "sound", "endgame", "Endgame.wav")
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
        man_hinh.blit(title_text, title_rect)
        man_hinh.blit(play_text, play_rect)
        man_hinh.blit(exit_text, exit_rect)
        pygame.display.flip()

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


# ==================== MÀN HÌNH GAME OVER ====================
def game_over_screen(score):
    gameover_music = os.path.join(current_path, "..", "assets", "sound", "endgame", "Endgame.wav")
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


# ==================== GAME CHÍNH ====================
def start_game():
    # Nhạc gameplay
    music_path = os.path.join(current_path, "..", "assets", "sound", "BackgroundMusic", "awestruck.wav")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    # Sprite groups
    tatca_sprites = pygame.sprite.Group()
    dichs = pygame.sprite.Group()
    dan_nguoi_choi = pygame.sprite.Group()
    items = pygame.sprite.Group()

    # Player
    may_bay = Player(rong // 2, cao - 80, 5, dan_nguoi_choi)
    tatca_sprites.add(may_bay)

    # HUD
    hud = Hud(may_bay)

    # Biến sinh địch
    thoi_gian_sinh_dich = 0
    delay_sinh_dich = 1000
    max_dich = 15
    bg_y = 0
    bg_speed = 2
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        dt = dong_ho.tick(FPS)
        thoi_gian_sinh_dich += dt

        # -------- Sự kiện --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # -------- Sinh địch --------
        if thoi_gian_sinh_dich >= delay_sinh_dich and len(dichs) < max_dich:
            thoi_gian_sinh_dich = 0
            x = random.randint(20, rong - 20)
            y = random.randint(-100, -40)
            base_speed = random.randint(2, 4)
            if hud.score > 500:
                base_speed += 1  
            if hud.score > 1000:
                base_speed += 1
                bg_speed += 0.5

            # 🎯 Level địch tăng dần theo thời gian (10s mỗi cấp)
            elapsed = (pygame.time.get_ticks() - start_time) // 10000
            enemy_level = min(1 + elapsed, 3)

            # 🎲 Tăng độ đa dạng: có địch yếu và mạnh xen kẽ
            random_level = random.randint(1, enemy_level)
            new_enemy = Dich(x, y, base_speed, level=random_level)

            tatca_sprites.add(new_enemy)
            dichs.add(new_enemy)

        # -------- Cập nhật --------
        tatca_sprites.update()
        dan_nguoi_choi.update()
        items.update()

        # -------- Cuộn nền --------
        man_hinh.blit(background, (0, bg_y))
        man_hinh.blit(background, (0, bg_y - cao))
        bg_y += bg_speed
        if bg_y >= cao:
            bg_y = 0

        # -------- Va chạm đạn ↔ địch --------
        hits = pygame.sprite.groupcollide(dan_nguoi_choi, dichs, True, False)
        for bullet, enemies in hits.items():
            for enemy in enemies:
                if enemy.tru_mau(1):  # nếu hết máu
                    enemy.kill()
                    hud.cong_diem(10)

                    # Rơi item
                    item = drop_item(enemy.rect.centerx, enemy.rect.centery, cao)
                    if item:
                        tatca_sprites.add(item)
                        items.add(item)

        # -------- Va chạm player ↔ địch --------
        hits = pygame.sprite.spritecollide(may_bay, dichs, True)
        for hit in hits:
            may_bay.tim -= 1
            if may_bay.sung_level > 1:
                may_bay.sung_level -= 1
                print(f"Mất 1 tim → súng giảm còn Level {may_bay.sung_level}")

            if may_bay.tim <= 0:
                if game_over_screen(hud.score):
                    return start_game()
                else:
                    running = False

        # -------- Va chạm player ↔ item --------
        collected = pygame.sprite.spritecollide(may_bay, items, True)
        for item in collected:
            if item.type == "hp":
                if may_bay.tim < 3:
                    may_bay.tim += 1
                    print("Nhặt tim ❤️ → +1 HP")
            elif item.type == "power":
                if may_bay.sung_level < 3:
                    may_bay.sung_level += 1
                    print(f"Nhặt POWER 🔥 → Súng Level {may_bay.sung_level}")

        # -------- Tăng độ khó dần theo điểm --------
        if hud.score > 0 and hud.score % 100 == 0:
            max_dich = min(35, max_dich + 1)
            delay_sinh_dich = max(400, delay_sinh_dich - 10)

        # -------- Vẽ --------
        tatca_sprites.draw(man_hinh)
        dan_nguoi_choi.draw(man_hinh)
        items.draw(man_hinh)
        hud.ve(man_hinh)
        pygame.display.flip()


# ==================== VÒNG LẶP CHÍNH ====================
while True:
    if main_menu():
        start_game()
