# Traffic Escape

Cross 8 lanes of oncoming traffic to reach the other side (Frogger-style), built with **Pygame**.

## Setup

```bash
pip install -r requirements.txt
python main.py
```

(On macOS use `python3 -m pip install -r requirements.txt` and `python3 main.py`.)

## Controls

| Key | Action |
|-----|--------|
| SPACE | Start (title screen) |
| A/D or Left/Right | Change lane |
| W / Up | Move forward |
| S / Down | Move back |
| R | Restart |

## Folder Structure

```
Lab-04/
├── main.py
├── requirements.txt
├── README.md
├── LLM chat export.pdf
├── Video/
│   ├── before.mp4
│   └── after.mp4
└── game/
    ├── __init__.py
    ├── game_engine.py
    ├── player.py
    └── traffic.py
```

---

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

### Task 1: Lives System
> Give the player 3 lives. Getting hit loses one; game over at 0.

3 hearts in the HUD. A hit shows a "CRASH!" flash, respawns the player on the start sidewalk and gives ~1.5 s of blinking invulnerability. At 0 lives the GAME OVER screen appears.

### Task 2: Moving Log/Raft Lane
> Add a safe lane where the player must hop on a moving log to cross.

A river band crosses the road. Standing in the water without a log under you costs a life ("SPLASH!"). Logs carry you sideways; being carried off-screen also drowns you. Cars run under the river, so they cannot hit you while you ride a log. After leaving the river the player snaps back to a lane.

### Task 3: High Score Table
> Track and display the top 5 scores across sessions (save to JSON).

Top 5 scores are saved to `highscores.json` (created on first finished game, safe against missing/corrupt files). They are shown on the title screen and on the end screen, where the current run is highlighted. Score = furthest progress, plus a win bonus (500 + 250 per life left + time bonus).

### Task 4: Day/Night Cycle
> Every 30 seconds switch between day and night. At night, cars have headlights visible further ahead.

Switches every 30 s of play (`CYCLE_MS` in `game_engine.py`) with a 2 s fade and a countdown in the HUD. At night the screen darkens and each car's headlight beam grows from 40 px to 230 px ahead, lighting the lanes in front of it. The player's car has a short light too.

---

## Submission Checklist

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior — `Video/before.mp4`
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working — `Video/after.mp4`
- [ ] The Chat/LLM used page link, with the complete chat history — `LLM chat export.pdf` / link: _paste link here_
