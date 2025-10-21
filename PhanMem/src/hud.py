from utils import ve_text, draw_text

class Hud:
    def __init__(self, player):
        self.player = player
        self.score = 0

    # Vietnamese alias remains
    def cong_diem(self, diem):
        return self.add_score(diem)

    def add_score(self, points):
        self.score += points

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

    # Vietnamese alias remains
    def ve(self, surface):
        return self.draw(surface)

    def draw(self, surface):
        draw_text(surface, f"Score: {self.score}", 25, 10, 10)
        draw_text(surface, f"Heart: {self.player.tim}", 25, 700, 10)
