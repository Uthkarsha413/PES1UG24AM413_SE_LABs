# Traffic Escape

Cross 8 lanes of oncoming traffic to reach the other side (Frogger-style).

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| A/D or Left/Right | Change lane |
| W / UP | Move forward |
| S / DOWN | Move back |
| R | Restart |

## Tasks to Complete

### Task 1: Lives System
> Give the player 3 lives. Getting hit loses one; game over at 0.

**Done.** Hearts in the HUD; a hit respawns you on the start sidewalk with ~1.5 s of blinking invulnerability; 0 lives = GAME OVER.


### Task 2: Moving Log/Raft Lane
> Add a safe lane where the player must hop on a moving log to cross.

**Done.** A river band crosses the road. Standing in it without a log = splash (lose a life). Logs carry you sideways; being carried off-screen also drowns you. Cars run under the river, so they can't hit you on a log.


### Task 3: High Score Table
> Track and display the top 5 scores across sessions (save to JSON).

**Done.** Saved to `highscores.json` next to `main.py`. Shown on the title screen and the end screen (your run is highlighted). Score = furthest progress, plus a win bonus (500 + 250/life left + time bonus).

### Task 4: Day/Night Cycle
> Every 30 seconds switch between day and night. At night, cars have headlights visible further ahead.

**Done.** Switches every 30 s of play (2 s fade, countdown in HUD). At night the screen darkens and each car's beam grows from 40 px to 230 px.

## Bugs fixed in the original
- Player spawned at x=300, straddling lanes 3 and 4, so it could be hit by two lanes (now lane-centred).
- Player could move below the screen (no bottom clamp).
- The lane-hop cooldown also blocked forward/back movement.
- Car positions used int Rect truncation, so up-bound cars were faster than down-bound ones at fractional speeds (now float position).
- Win zone was hidden behind the HUD; forward speed ignored the `SPEED` constant (was hard-coded 8, now 4).
- Score rose every frame, rewarding stalling (now progress-based).
- Cars could spawn on top of each other in a lane.

## Folder Structure

```
traffic-escape/
├── main.py
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── player.py
│   └── traffic.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history

