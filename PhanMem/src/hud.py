from utils import ve_text

class Hud:
    def __init__(self, player):
        self.player = player
        self.score = 0

    def cong_diem(self, diem):
        self.score += diem

    def get_score(self):
        return self.score

    def background_tier(self):
        """Return an integer tier based on score to select background images.
        0 = default, 1 = mid, 2 = high
        """
        if self.score >= 4000:
            return 2
        if self.score >= 1000:
            return 1
        return 0

    def ve(self, surface):
        ve_text(surface, f"Score: {self.score}", 25, 10, 10)
        ve_text(surface, f"Heart: {self.player.tim}", 25, 700, 10)
