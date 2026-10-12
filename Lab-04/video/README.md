

## BEFORE (original game) — `Video/before.mp4`

What the original code did wrong:

| # | Bug / missing behavior | Where |
|---|------------------------|-------|
| 1 | Player starts at x=300, straddling lanes 3 and 4, and stays misaligned after every lane hop, so it can be hit by two lanes at once. | `player.py`, `game_engine.py` |
| 2 | No bottom clamp: holding S moves the player off the screen. | `player.py` |
| 3 | The lane-hop cooldown also blocks forward/back movement. | `player.py` |
| 4 | Cars use integer Rect truncation, so up-bound cars move faster than down-bound ones at fractional speeds (3.5, 4.5, ...). | `traffic.py` |
| 5 | Win line (`top <= 10`) is hidden behind the HUD; `SPEED` constant unused (hard-coded 8). | `game_engine.py`, `player.py` |
| 6 | Score rises every frame, rewarding standing still. | `game_engine.py` |
| 7 | Cars can spawn overlapping in the same lane. | `game_engine.py` |
| 8 | One hit = instant game over. No lives, no river, no high scores, no day/night. | — |

---

## AFTER (my changes) — `Video/after.mp4`

### Bug fixes
- Player is placed by lane index and always centred in a lane (re-snapped after riding a log).
- Player is clamped to the play area (cannot leave the screen).
- Lane-hop cooldown only affects sideways hops.
- Cars use a float position, so every lane moves at the same speed.
- Dedicated goal sidewalk below the HUD; forward speed uses `SPEED` (4 px/frame).
- Score is progress-based instead of time-based.
- Spawn guard keeps a minimum gap between cars entering the same lane.

