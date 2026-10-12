import datetime
import json
import os
import random

import pygame

from game.player import Player, LANE_W
from game.traffic import make_car, lane_entry_clear, River, get_cone, get_glow

LANES = 8
WIDTH = LANES * LANE_W
HEIGHT = 600
FPS = 60
BG = (60, 60, 60)

# layout (y coordinates)
HUD_H = 40
GOAL_BOTTOM = 90            # top sidewalk spans HUD_H..GOAL_BOTTOM; reaching it wins
START_TOP = 540             # bottom sidewalk spans START_TOP..HEIGHT
RIVER_TOP = 300
RIVER_H = 80
RIVER_BOTTOM = RIVER_TOP + RIVER_H
START_LANE = 4
START_CENTER_Y = START_TOP + 30

# task 1: lives
MAX_LIVES = 3

# task 4: day / night
CYCLE_MS = 30_000           # switch every 30 s
FADE_MS = 2_000
NIGHT_ALPHA = 175
BEAM_DAY = 40
BEAM_NIGHT = 230

# task 3: high scores
SCORES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "highscores.json")
SCORE_LIMIT = 5


class HighScores:
    """Top-N scores persisted to a JSON file."""

    def __init__(self, path=SCORES_PATH, limit=SCORE_LIMIT):
        self.path = path
        self.limit = limit
        self.entries = self._load()

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            return []
        if not isinstance(data, list):
            return []
        clean = []
        for e in data:
            if isinstance(e, dict) and isinstance(e.get("score"), int) and not isinstance(e.get("score"), bool):
                clean.append({"score": e["score"],
                              "result": str(e.get("result", "")),
                              "date": str(e.get("date", ""))})
        clean.sort(key=lambda e: -e["score"])
        return clean[:self.limit]

    def best(self):
        return self.entries[0]["score"] if self.entries else 0

    def add(self, score, result):
        """Insert a score. Returns its 0-based rank in the table, or None if it didn't make the cut."""
        entry = {"score": int(score), "result": result, "date": datetime.date.today().isoformat()}
        ranked = sorted(self.entries + [entry], key=lambda e: -e["score"])   # stable: ties keep older first
        rank = next(i for i, e in enumerate(ranked) if e is entry)
        self.entries = ranked[:self.limit]
        self.save()
        return rank if rank < self.limit else None

    def save(self):
        tmp = self.path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, indent=2)
            os.replace(tmp, self.path)
        except OSError as exc:
            print(f"Could not save high scores: {exc}")


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 24, bold=True)
        self.hud_font = pygame.font.SysFont("monospace", 20, bold=True)
        self.small_font = pygame.font.SysFont("monospace", 18, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.dark = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.scores = HighScores()
        self.dt = 0
        self.reset()
        self.state = "title"

    # ------------------------------------------------------------ state
    def reset(self):
        self.player = Player(START_LANE, START_CENTER_Y)
        self.river = River(RIVER_TOP, RIVER_H, WIDTH)
        self.cars = []
        self.timer = 0
        self.spawn_interval = 50
        self.speed = 3
        self.frames = 0
        self.play_ms = 0
        self.best_progress = 0
        self.score = 0
        self.lives = MAX_LIVES
        self.was_in_water = False
        self.flash_timer = 0
        self.flash_text = ""
        self.flash_color = (255, 255, 255)
        self.cycle_ms = 0
        self.is_night = False
        self.night_level = 0.0
        self.last_rank = None
        self.state = "playing"

    @property
    def game_over(self):
        return self.state == "game_over"

    @property
    def won(self):
        return self.state == "won"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN) and self.state == "title":
                    self.reset()
        return True

    # ------------------------------------------------------------ rules
    def _in_water(self):
        return RIVER_TOP < self.player.rect.centery < RIVER_BOTTOM

    def _car_hits_player(self, car):
        p = self.player.rect
        if p.centery >= START_TOP or p.centery <= GOAL_BOTTOM:
            return False                                    # sidewalks are safe
        overlap = car.rect.clip(p)
        if overlap.width <= 0 or overlap.height <= 0:
            return False
        if overlap.top >= RIVER_TOP and overlap.bottom <= RIVER_BOTTOM:
            return False                                    # that part of the road is under the river
        return True

    def _lose_life(self, text):
        self.lives -= 1
        self.was_in_water = False
        self.flash_timer = 40
        self.flash_text = text
        self.flash_color = (220, 60, 60) if text == "CRASH!" else (60, 120, 220)
        if self.lives <= 0:
            self._finish(False)
        else:
            self.player.respawn(invulnerable=90)

    def _finish(self, won):
        if won:
            secs = self.play_ms / 1000
            bonus = 500 + self.lives * 250 + max(0, int((60 - secs) * 10))
            self.score = self.best_progress + bonus
            self.state = "won"
        else:
            self.score = self.best_progress
            self.state = "game_over"
        if self.score > 0:
            self.last_rank = self.scores.add(self.score, "WIN" if won else "DIED")

    def _update_daynight(self):
        self.cycle_ms += min(self.dt, 100)
        self.is_night = (self.cycle_ms // CYCLE_MS) % 2 == 1
        target = 1.0 if self.is_night else 0.0
        step = min(self.dt, 100) / FADE_MS
        if self.night_level < target:
            self.night_level = min(target, self.night_level + step)
        else:
            self.night_level = max(target, self.night_level - step)

    def _spawn_car(self):
        free = [l for l in range(LANES) if lane_entry_clear(self.cars, l, HEIGHT)]
        if free:
            self.cars.append(make_car(random.choice(free), HEIGHT, self.speed))

    def update(self):
        if self.state == "title":
            self.river.update()
            return
        if self.state != "playing":
            return

        self.frames += 1
        self.play_ms += min(self.dt, 100)
        self._update_daynight()

        # --- player input
        keys = pygame.key.get_pressed()
        self.player.move(keys, 0, WIDTH, HUD_H, HEIGHT)
        self.player.tick()

        # --- river: must be standing on a log while in the water band
        in_water = self._in_water()
        log = self.river.log_under(self.player.rect) if in_water else None
        self.river.update()
        if in_water:
            if log is None:
                self._lose_life("SPLASH!")
                return
            self.player.rect.x += self.river.speed          # ride the log
            if not (0 <= self.player.rect.centerx <= WIDTH):
                self._lose_life("SPLASH!")                  # carried off-screen
                return
        elif self.was_in_water:
            self.player.snap_to_lane()
        self.was_in_water = in_water

        # --- traffic
        self.timer += 1
        if self.timer >= self.spawn_interval:
            self._spawn_car()
            self.timer = 0
            self.spawn_interval = max(22, self.spawn_interval - 0.2)
        for c in self.cars:
            c.update()
        if self.player.invulnerable == 0:
            for c in self.cars:
                if self._car_hits_player(c):
                    self._lose_life("CRASH!")
                    break
        if self.state != "playing":
            return
        self.cars = [c for c in self.cars if not c.off_screen(HEIGHT)]
        if self.frames % 300 == 0:
            self.speed = min(10, self.speed + 0.5)

        # --- progress / win
        self.best_progress = max(self.best_progress, START_CENTER_Y - self.player.rect.centery)
        self.score = self.best_progress
        if self.player.rect.centery <= GOAL_BOTTOM:
            self._finish(True)

    # ------------------------------------------------------------ drawing
    def _draw_night(self):
        self.dark.fill((6, 10, 36, int(NIGHT_ALPHA * self.night_level)))
        self.light.fill((0, 0, 0, 0))
        length = BEAM_DAY + (BEAM_NIGHT - BEAM_DAY) * self.night_level
        for c in self.cars:
            cone = get_cone(length, c.direction)
            w, h = cone.get_size()
            x = c.rect.centerx - w // 2
            y = c.rect.bottom if c.direction == 1 else c.rect.top - h
            self.light.blit(cone, (x, y), special_flags=pygame.BLEND_RGBA_MAX)
        self.light.fill((0, 0, 0, 0), self.river.rect)      # cars are under the river: no light there
        if self.state in ("playing",):
            pr = self.player.rect
            cone = get_cone(100, -1)
            self.light.blit(cone, (pr.centerx - cone.get_width() // 2, pr.top - cone.get_height()),
                            special_flags=pygame.BLEND_RGBA_MAX)
            glow = get_glow(60)
            self.light.blit(glow, (pr.centerx - 60, pr.centery - 60), special_flags=pygame.BLEND_RGBA_MAX)
        self.dark.blit(self.light, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.screen.blit(self.dark, (0, 0))

    def _draw_heart(self, x, y, color):
        pygame.draw.circle(self.screen, color, (x - 5, y - 2), 6)
        pygame.draw.circle(self.screen, color, (x + 5, y - 2), 6)
        pygame.draw.polygon(self.screen, color, [(x - 11, y + 1), (x + 11, y + 1), (x, y + 13)])

    def _draw_hud(self):
        pygame.draw.rect(self.screen, (20, 20, 20), pygame.Rect(0, 0, WIDTH, HUD_H))
        s = self.hud_font.render(f"Score {self.score}", True, (220, 220, 220))
        self.screen.blit(s, (8, 10))
        best = self.hud_font.render(f"Best {max(self.scores.best(), self.score)}", True, (230, 200, 90))
        self.screen.blit(best, (150, 10))
        for i in range(MAX_LIVES):
            self._draw_heart(300 + i * 30, 14, (230, 60, 70) if i < self.lives else (70, 70, 70))
        left = int((CYCLE_MS - self.cycle_ms % CYCLE_MS) / 1000) + 1
        label = ("NIGHT " if self.is_night else "DAY ") + f"{left:>2}s"
        col = (150, 170, 255) if self.is_night else (255, 220, 100)
        t = self.hud_font.render(label, True, col)
        self.screen.blit(t, (WIDTH - t.get_width() - 8, 10))

    def _draw_table(self, y, highlight=None):
        head = self.font.render("TOP 5", True, (230, 200, 90))
        self.screen.blit(head, (WIDTH // 2 - head.get_width() // 2, y))
        for i in range(SCORE_LIMIT):
            if i < len(self.scores.entries):
                e = self.scores.entries[i]
                text = f"{i + 1}. {e['score']:>5}  {e['result']:<4}  {e['date']}"
            else:
                text = f"{i + 1}.   ---"
            color = (255, 220, 80) if i == highlight else (210, 210, 210)
            r = self.small_font.render(text, True, color)
            self.screen.blit(r, (WIDTH // 2 - 150, y + 34 + i * 28))

    def _overlay(self):
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 170))
        self.screen.blit(ov, (0, 0))

    def _center(self, font, text, color, y):
        m = font.render(text, True, color)
        self.screen.blit(m, (WIDTH // 2 - m.get_width() // 2, y))

    def _draw_end(self, title, color):
        self._overlay()
        self._center(self.big_font, title, color, 100)
        self._center(self.font, f"Score: {self.score}", (230, 230, 230), 160)
        if self.last_rank == 0:
            self._center(self.small_font, "NEW HIGH SCORE!", (255, 220, 80), 192)
        self._draw_table(225, self.last_rank)
        self._center(self.font, "Press R to Restart", (200, 200, 200), 450)

    def _draw_title(self):
        self._overlay()
        self._center(self.big_font, "TRAFFIC ESCAPE", (240, 200, 60), 70)
        for i, line in enumerate(["Cross the road, hop a log over the river,",
                                  "reach the top. You have 3 lives.",
                                  "A/D or arrows: change lane   W/S or arrows: forward/back"]):
            self._center(self.small_font, line, (220, 220, 220), 140 + i * 26)
        self._draw_table(240)
        self._center(self.font, "Press SPACE to start", (200, 200, 200), 450)

    def draw(self):
        self.screen.fill(BG)
        for i in range(LANES + 1):
            pygame.draw.line(self.screen, (100, 100, 100), (i * LANE_W, 0), (i * LANE_W, HEIGHT), 2)
        for y in range(0, HEIGHT, 60):
            for i in range(LANES):
                pygame.draw.rect(self.screen, (200, 200, 100), pygame.Rect(i * LANE_W + LANE_W // 2 - 3, y, 6, 30))
        for c in self.cars:
            c.draw(self.screen)
        self.river.draw(self.screen)                        # covers cars: the road runs under the river
        pygame.draw.rect(self.screen, (150, 130, 110), pygame.Rect(0, START_TOP, WIDTH, HEIGHT - START_TOP))
        pygame.draw.rect(self.screen, (150, 130, 110), pygame.Rect(0, HUD_H, WIDTH, GOAL_BOTTOM - HUD_H))
        if self.state != "title":
            self.player.draw(self.screen)
        if self.night_level > 0.01:
            self._draw_night()
        for c in self.cars:
            if GOAL_BOTTOM <= c.lamp_positions()[0][1] <= START_TOP and \
                    not RIVER_TOP <= c.lamp_positions()[0][1] <= RIVER_BOTTOM:
                c.draw_lamps(self.screen, self.night_level)
        self._draw_hud()

        if self.flash_timer > 0 and self.state == "playing":
            fl = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fl.fill((*self.flash_color, int(110 * self.flash_timer / 40)))
            self.screen.blit(fl, (0, 0))
            self._center(self.big_font, self.flash_text, (255, 255, 255), HEIGHT // 2 - 30)
            self.flash_timer -= 1

        if self.state == "title":
            self._draw_title()
        elif self.state == "game_over":
            self._draw_end("GAME OVER", (220, 60, 60))
        elif self.state == "won":
            self._draw_end("YOU MADE IT!", (80, 220, 80))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(FPS)
        pygame.quit()
