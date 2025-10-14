from utils import ve_text

class Hud:
    def __init__(self, player):
        self.player = player
        self.score = 0

    def cong_diem(self, diem):
        self.score += diem

    def ve(self, surface):
        ve_text(surface, f"Score: {self.score}", 25, 10, 10)
        ve_text(surface, f"Heart: {self.player.tim}", 25, 700, 10)
