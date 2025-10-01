# Passo AI Bot

This repository contains the code for an AI bot designed to play the strategic board game, Passo. The bot uses a classic game theory algorithm to analyze the board and make intelligent moves against an opponent.

### Technical Overview

*   **Programming Language:** Python
*   **Key Libraries:** Standard Library
*   **Core Concepts Covered:** Game Theory, Adversarial Search, Minimax Algorithm with Alpha-Beta Pruning, Heuristic Evaluation Functions.

---

### Project Goal

The primary goal of this project is to implement a competitive AI agent that can play the game of Passo effectively. This involves creating a robust game logic engine, a move generation system, and an intelligent decision-making algorithm to select the optimal move at any given state of the game.

---

### How to Play Passo

#### 1. Components and Setup

*   **Board:** The playing area is a 5×5 square grid formed by arranging 25 separate small tiles.
*   **Pieces:** Each player takes 5 disks of their color (e.g., Black or White).
*   **Starting Position:** Players place their 5 disks on the row of tiles closest to them.

#### 2. How to Play (The Turn)

Players take turns alternating actions. A turn consists of a single disk movement followed by a tile removal or preservation action.

**A. Movement**

*   **Select a Piece:** Choose one of your disks on the board.
*   **Move:** Move the disk exactly one space in any direction: orthogonally (forward, backward, or sideways) or diagonally.
*   **Landing Spot (Stacking):** The disk must land on an existing tile that has no more than two other pieces (of any color) already on it. The moving piece is placed on top of the stack. The maximum stack size is three pieces.

**B. Tile Removal**

The action you take after moving depends on what you left behind on the starting tile:

*   **Remove the Tile:** If the tile you moved from is now completely empty, you must remove that tile from the game. This permanently shrinks the board.
*   **Tile Remains:** If you moved a disk from the top of an existing stack (meaning pieces are still on the tile), the tile remains on the board.

#### 3. Special Board State Rules

*   **Impassable Spaces:** You cannot move through, across, or land on the empty spaces where tiles have been removed.
*   **Isolated Pieces/Tiles:** If a tile becomes completely isolated (no longer orthogonally or diagonally adjacent to any other tile), that tile and any pieces on it are immediately removed from the game.

#### 4. Winning Conditions

The game ends immediately when one of the following conditions is met:

*   **Pass Victory (The Primary Goal):** The player who is first to move one of their disks to a tile that is past the opponent's furthest back piece wins.
*   **Blocking Victory:** The player whose opponent cannot make any legal move on their turn wins.

---

### How the Bot Works

The bot's intelligence is powered by the **Minimax algorithm with Alpha-Beta Pruning**. This is a search algorithm commonly used in two-player, turn-based games like Chess or Tic-Tac-Toe.

1.  **Thinking Ahead:** The bot doesn't just look at the current board; it simulates moves several turns into the future (up to a set `MAX_DEPTH`). It assumes the opponent will also make the best possible move at each step.

2.  **The Evaluation Function:** The core of the bot's "brain" is its evaluation function (`calculateScore`). This function assigns a numerical score to any board position, representing how favorable it is for the bot. The score is calculated based on several key heuristics:
    *   **Piece Count:** More of your pieces on the board is better.
    *   **Stack Control:** It's highly advantageous to have your piece on top of a stack, especially a full stack of three.
    *   **Forward Progress:** The bot is heavily incentivized to move its pieces forward toward the opponent's side to pursue the primary "Pass Victory" condition.
    *   **Aggressive Stacking:** The bot gets bonus points for moving onto a tile to stack on top of an opponent's piece.
    *   **The "Fortress" Strategy:** The bot has a hardcoded opening strategy to build a powerful 3-piece stack in a specific corner, which it considers a highly valuable position to maintain.

3.  **Finding the Best Move:**
    *   First, the bot checks if it has an immediate **winning move**. If so, it takes it.
    *   Otherwise, it generates all legal moves and uses the Minimax algorithm to "search" through the tree of possible future game states.
    *   It chooses the move that leads to the future board state with the highest possible score, effectively picking the most strategic action according to its evaluation heuristics.
    *   **Alpha-Beta Pruning** is an optimization that allows the bot to "prune" branches of the search tree that it knows won't lead to a better outcome, making its search much faster and more efficient.
