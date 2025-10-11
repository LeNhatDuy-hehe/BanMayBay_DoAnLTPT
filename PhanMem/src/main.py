import pygame
from settings import rong, cao, DO, FPS
from player import Player
from enemy import Dich
from hud import Hud
import sys
import os
import random


pygame.init()
man_hinh = pygame.display.set_mode((rong, cao))
pygame.display.set_caption("Trò Chơi Bắn Máy Bay")
dong_ho = pygame.time.Clock()

# Path
current_path = os.path.dirname(__file__)
background_path = os.path.join(current_path, "..", "assets", "image", "scrollbackground", "scroll_background.png")

# Load ảnh nền cuộn
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (rong, cao))


def main_menu():
    # Nhạc menu
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
        #man_hinh.blit(background_menu, (0, 0))
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


def game_over_screen(score):
    # Nhạc game over
    gameover_music = os.path.join(current_path, "..", "assets", "sound", "endgame", "Endgame.wav")
    pygame.mixer.music.load(gameover_music)
    pygame.mixer.music.play(-1)

    font_big = pygame.font.SysFont("Arial", 64, bold=True)
    font_small = pygame.font.SysFont("Arial", 36)

    score_text = font_small.render(f"Your Score: {score}", True, (255, 255, 255))
    retry_text = font_small.render("PLAY AGAIN", True, (0, 255, 0))
    exit_text = font_small.render("EXIT", True, (255, 255, 255))

    score_rect = score_text.get_rect(center=(rong // 2, cao // 2 - 80))
    retry_rect = retry_text.get_rect(center=(rong // 2, cao // 2))
    exit_rect = exit_text.get_rect(center=(rong // 2, cao // 2 + 80))

    while True:
        #man_hinh.blit(gameover_img, gameover_rect)
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


def start_game():
    # Nhạc gameplay
    music_path = os.path.join(current_path, "..", "assets", "sound", "BackgroundMusic", "awestruck.wav")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    # Sprite group
    tatca_sprites = pygame.sprite.Group()
    dichs = pygame.sprite.Group()
    dan_nguoi_choi = pygame.sprite.Group()

    # Máy bay người chơi
    may_bay = Player(rong // 2, cao - 80, 5, dan_nguoi_choi)
    tatca_sprites.add(may_bay)

    # HUD
    hud = Hud(may_bay)

    # Địch
    so_luong_dich = 10
    for i in range(so_luong_dich):
        x = random.randint(20, rong - 20)
        y = random.randint(-600, -40)
        speed = random.randint(2, 5)
        dich = Dich(x, y, speed)
        tatca_sprites.add(dich)
        dichs.add(dich)

    # Nền cuộn
    bg_y = 0
    bg_speed = 2

    running = True
    while running:
        dong_ho.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tatca_sprites.update()
        dan_nguoi_choi.update()

        # Nền cuộn
        man_hinh.blit(background, (0, bg_y))
        man_hinh.blit(background, (0, bg_y - cao))
        bg_y += bg_speed
        if bg_y >= cao:
            bg_y = 0

        # Đạn trúng địch
        hits = pygame.sprite.groupcollide(dan_nguoi_choi, dichs, True, True)
        for hit in hits:
            hud.cong_diem(10)
            # Spawn lại enemy mới
            x = random.randint(20, rong - 20)
            y = random.randint(-600, -40)
            speed = random.randint(2, 5)
            new_enemy = Dich(x, y, speed)
            tatca_sprites.add(new_enemy)
            dichs.add(new_enemy)

        # Địch va chạm máy bay
        hits = pygame.sprite.spritecollide(may_bay, dichs, True)
        for hit in hits:
            may_bay.tim -= 1
            if may_bay.sung_level > 1:
                may_bay.sung_level -= 1
                print(f"Mất 1 tim → súng giảm còn Level {may_bay.sung_level}")

            # Spawn lại enemy mới
            x = random.randint(20, rong - 20)
            y = random.randint(-600, -40)
            speed = random.randint(2, 5)
            new_enemy = Dich(x, y, speed)
            tatca_sprites.add(new_enemy)
            dichs.add(new_enemy)

            if may_bay.tim <= 0:
                if game_over_screen(hud.score):
                    return start_game()
                else:
                    running = False

        # Vẽ sprite + HUD
        tatca_sprites.draw(man_hinh)
        dan_nguoi_choi.draw(man_hinh)
        hud.ve(man_hinh)

        pygame.display.flip()


while True:
    if main_menu():
        if start_game():
            if not game_over_screen():
                break
