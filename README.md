# PyTetris

A Tetris clone written in Python with Pygame and NumPy.

## Overview

PyTetris is a single-script implementation of Tetris. The left half of the window is the playing field; the right half shows the title, the next piece, the current level and the score. The game runs at 60 updates per second.

## Features

- A 10-column by 24-row playing field drawn with 20-pixel blocks, in a 410 x 480 window titled "Tetris".
- All seven tetromino shapes (I, J, L, O, S, T and Z). Each new piece gets a random shape and a random colour from a palette of seven.
- Clockwise rotation, blocked if the rotated piece would collide with the walls, the floor or placed blocks.
- Soft drop while the down key is held.
- A ghost piece (drop shadow) outlining where the current piece will land.
- A preview of the next piece.
- Full rows are cleared and the rows above shift down.
- Scoring per clear of 40, 100, 300 or 1200 points for one, two, three or four rows, multiplied by (level + 1).
- The level goes up after every 10 cleared rows, to a maximum of 10, and pieces fall faster at higher levels.
- The game ends when a new piece cannot be placed.

## Tech stack

- Python 3
- [Pygame](https://www.pygame.org/), for the window, drawing, text and keyboard input
- [NumPy](https://numpy.org/), to store the board as a grid of RGB colours

## Getting started

### Prerequisites

- Python 3
- Pygame and NumPy

The repository has no `requirements.txt`, so install the two libraries directly:

```bash
pip install pygame numpy
```

### Run

```bash
python py_tetris.py
```

## Usage

| Key | Action |
|-----|--------|
| Left arrow | Move left |
| Right arrow | Move right |
| Up arrow | Rotate clockwise |
| Down arrow (hold) | Soft drop |

Holding Left, Right or Up repeats the action every fourth update, about 15 times a second. Closing the window quits.

## Project structure

```
py_tetris.py   # the whole game: Piece and Game classes (update, render, collision, row clearing, ghost piece) and the main loop
```

## Limitations

- There is no hard drop, hold piece, pause or game-over screen. When the game ends, the window closes.
- Pieces are chosen independently at random (no "bag" randomiser), so the same piece can come up many times in a row.
- Rotation has no wall kicks: a rotation that would collide is simply refused.
- The fall interval is `15 - 2 * level` updates, which goes negative above level 7, so speed stops rising steadily at levels 8 to 10.
