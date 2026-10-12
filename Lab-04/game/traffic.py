import math
import random
import pygame

LANE_W = 80
CAR_W = 60
CAR_H = 80
CAR_GAP = 150   # min distance between cars entering the same lane
COLORS = [(220, 60, 60), (220, 140, 40), (140, 60, 180), (60, 180, 80), (180, 180, 40), (60, 80, 200)]

LOG_W = 160
LOG_GAP = 130


class Car:
    def __init__(self, lane_x, y, direction, speed, lane=0):
        self.rect = pygame.Rect(lane_x + 10, int(y), CAR_W, CAR_H)
        self.y = float(y)            # float position: Rect truncation made up/down cars differ in speed
        self.direction = direction   # 1=down, -1=up
        self.speed = speed
        self.lane = lane
        self.color = random.choice(COLORS)

    def update(self):
        self.y += self.direction * self.speed
        self.rect.y = round(self.y)

    def off_screen(self, height):
        return self.rect.top > height + 100 or self.rect.bottom < -100

    def lamp_positions(self):
        y = (self.rect.bottom - 4) if self.direction == 1 else (self.rect.top + 4)
        return [(self.rect.x + 14, y), (self.rect.right - 14, y)]

    def draw(self, screen):
        r = self.rect
        pygame.draw.rect(screen, self.color, r, border_radius=8)
        win_y = r.y + 10 if self.direction == -1 else r.bottom - 32
        pygame.draw.rect(screen, (180, 220, 240), pygame.Rect(r.x + 8, win_y, 44, 22), border_radius=4)
        for wx in [r.x + 6, r.right - 16]:
            for wy in [r.y + 4, r.bottom - 16]:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(wx, wy, 10, 12), border_radius=3)

    def draw_lamps(self, screen, night_level):
        for pos in self.lamp_positions():
            pygame.draw.circle(screen, (250, 235, 150), pos, 5)
            if night_level > 0.5:
                pygame.draw.circle(screen, (255, 220, 100), pos, 8, 2)


def make_car(lane_idx, height, speed):
    x = lane_idx * LANE_W
    direction = 1 if lane_idx % 2 == 0 else -1
    y = -90 if direction == 1 else height + 10
    return Car(x, y, direction, speed, lane_idx)


def lane_entry_clear(cars, lane_idx, height):
    """True if a new car can enter this lane without overlapping the last one."""
    direction = 1 if lane_idx % 2 == 0 else -1
    for c in cars:
        if c.lane != lane_idx:
            continue
        if direction == 1 and c.rect.top < -90 + CAR_GAP:
            return False
        if direction == -1 and c.rect.top > height + 10 - CAR_GAP:
            return False
    return True


# ---------- river / logs ----------

class Log:
    def __init__(self, x, top, height):
        self.rect = pygame.Rect(x, top + 6, LOG_W, height - 12)


class River:
    """A full-width water band with logs drifting sideways. The player must ride a log."""

    def __init__(self, top, height, width, speed=2):
        self.rect = pygame.Rect(0, top, width, height)
        self.width = width
        self.speed = speed                      # +right / -left, integer pixels per frame
        spacing = LOG_W + LOG_GAP
        count = math.ceil((width + LOG_W) / spacing)
        self.total = count * spacing            # wrap length
        self.logs = [Log(i * spacing - LOG_W, top, height) for i in range(count)]
        self.phase = 0

    def update(self):
        self.phase = (self.phase + 1) % 60
        for log in self.logs:
            log.rect.x += self.speed
            if self.speed > 0 and log.rect.left > self.width:
                log.rect.x -= self.total
            elif self.speed < 0 and log.rect.right < 0:
                log.rect.x += self.total

    def log_under(self, player_rect):
        cx = player_rect.centerx
        for log in self.logs:
            if log.rect.left < cx < log.rect.right:
                return log
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, (36, 92, 160), self.rect)
        for row in range(3):
            y = self.rect.top + 14 + row * 26
            off = (self.phase * 2 + row * 37) % 60
            for x in range(-60 + off, self.width, 60):
                pygame.draw.line(screen, (80, 140, 210), (x, y), (x + 18, y), 2)
        pygame.draw.line(screen, (20, 60, 110), (0, self.rect.top), (self.width, self.rect.top), 3)
        pygame.draw.line(screen, (20, 60, 110), (0, self.rect.bottom - 1), (self.width, self.rect.bottom - 1), 3)
        for log in self.logs:
            r = log.rect
            pygame.draw.rect(screen, (120, 78, 40), r, border_radius=12)
            for gx in range(r.x + 30, r.right - 20, 34):
                pygame.draw.line(screen, (90, 56, 28), (gx, r.y + 6), (gx, r.bottom - 6), 2)
            pygame.draw.ellipse(screen, (170, 120, 70), pygame.Rect(r.x, r.y, 24, r.height))
            pygame.draw.ellipse(screen, (170, 120, 70), pygame.Rect(r.right - 24, r.y, 24, r.height))


# ---------- headlight / glow masks (alpha = how much darkness to remove) ----------

_cone_cache = {}
_glow_cache = {}


def _build_cone(length):
    half0, spread, layers = 24, 0.35, 10
    w = int(2 * (half0 + spread * length)) + 2
    surf = pygame.Surface((w, length), pygame.SRCALPHA)
    cx = w / 2
    for i in range(layers):                     # longest + faintest first, shortest + brightest last
        l = length * (1 - i / layers)
        a = int(255 * 0.9 * (i + 1) / layers)
        pts = [(cx - half0, 0), (cx + half0, 0),
               (cx + half0 + spread * l, l), (cx - half0 - spread * l, l)]
        pygame.draw.polygon(surf, (0, 0, 0, a), pts)
    return surf


def get_cone(length, direction):
    """Headlight beam. direction 1 points down, -1 points up."""
    length = max(20, int(round(length / 10.0)) * 10)
    key = (length, direction)
    if key not in _cone_cache:
        base = _build_cone(length)
        _cone_cache[key] = base if direction == 1 else pygame.transform.flip(base, False, True)
    return _cone_cache[key]


def get_glow(radius):
    if radius not in _glow_cache:
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        for k in range(radius, 0, -4):
            a = int(255 * 0.85 * (1 - k / radius))
            pygame.draw.circle(surf, (0, 0, 0, a), (radius, radius), k)
        _glow_cache[radius] = surf
    return _glow_cache[radius]
