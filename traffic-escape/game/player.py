import pygame

SPEED = 4            # forward/back pixels per frame
LANE_W = 80
PLAYER_W = 40
PLAYER_H = 60
LANE_HOP_COOLDOWN = 12
INVULNERABLE_FRAMES = 90


def lane_center(lane):
    return lane * LANE_W + LANE_W // 2


class Player:
    def __init__(self, lane, center_y):
        self.start_lane = lane
        self.start_center_y = center_y
        self.color = (60, 160, 220)
        self.rect = pygame.Rect(0, 0, PLAYER_W, PLAYER_H)
        self.respawn()

    def respawn(self, invulnerable=0):
        """Put the player back on the start sidewalk, centred in a lane."""
        self.rect.center = (lane_center(self.start_lane), self.start_center_y)
        self.move_cooldown = 0
        self.invulnerable = invulnerable

    def snap_to_lane(self):
        """Re-centre in the nearest lane (used after riding a log)."""
        lane = round((self.rect.centerx - LANE_W // 2) / LANE_W)
        lane = max(0, min(7, lane))
        self.rect.centerx = lane_center(lane)

    def tick(self):
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def move(self, keys, min_x, max_x, min_y, max_y):
        # Lane hops have their own cooldown; forward/back is never blocked by it.
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
        else:
            dx = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx -= LANE_W
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += LANE_W
            if dx:
                self.rect.x = max(min_x, min(max_x - self.rect.width, self.rect.x + dx))
                self.move_cooldown = LANE_HOP_COOLDOWN
        dy = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += SPEED
        if dy:
            self.rect.y = max(min_y, min(max_y - self.rect.height, self.rect.y + dy))

    def draw(self, screen):
        # blink while invulnerable after being hit
        if self.invulnerable > 0 and (self.invulnerable // 5) % 2 == 0:
            return
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (180, 220, 240),
                         pygame.Rect(self.rect.x + 6, self.rect.y + 8, 28, 18), border_radius=4)
        for wx in [self.rect.x + 4, self.rect.right - 12]:
            for wy in [self.rect.y + 4, self.rect.bottom - 14]:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(wx, wy, 8, 10), border_radius=3)
        for lx in [self.rect.x + 9, self.rect.right - 9]:
            pygame.draw.circle(screen, (250, 235, 150), (lx, self.rect.y + 3), 3)
