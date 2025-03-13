# Cell Wars Documentation

## 1. Software Architecture and Structure

Cell Wars is a turn-based strategy game built using Python and Pygame, where two players compete to conquer cells on a grid-based battlefield using different cellular automaton patterns. The game implements a modular architecture with clear separation of concerns across multiple components.

### 1.1 Code Structure Overview

The project is organized into the following main components:

- **main.py**: Entry point containing the game loop, menu system, and UI rendering logic
- **game_manager.py**: Core component managing game state, player turns, and action execution
- **grid.py**: Handles the grid representation and cell state management
- **player.py**: Defines the Player class with player attributes and actions
- **player_action.py**: Implements the action system that players can select
- **cellular_automaton.py**: Contains all cellular automaton patterns and their execution logic
- **network.py**: Provides networking capabilities for multiplayer games
- **ui.py**: Contains UI components like buttons

### 1.2 Component Relationships

```
                    ┌───────────────┐
                    │    main.py    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ game_manager  │
                    └───┬───┬───┬───┘
                        │   │   │
         ┌──────────────┘   │   └──────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
   ┌───────────┐      ┌──────────┐      ┌─────────────┐
   │   grid    │      │  player  │      │  network    │
   └───────────┘      └─────┬────┘      └─────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ player_action │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   cellular    │
                    │  automaton    │
                    └───────────────┘
```

## 2. Action Selection to Cellular Automaton Execution Flow

One of the most important processes in Cell Wars is how player actions translate into cellular automaton patterns that conquer cells. Here's a detailed breakdown of this flow:

### 2.1 Action Selection Process

1. The player selects an action (like "Diamond Bomb" or "Snake Attack") by clicking one of the action buttons on their side of the screen.
2. In `main.py`, the `handle_button_click` function identifies which action was selected.
3. The function determines which player the button belongs to and ensures only the current player can select actions.
4. The selected action is passed to `GameManager` via the `select_action` method.
5. The button is visually highlighted to indicate it's been selected.

### 2.2 Target Cell Selection

1. After selecting an action, the player must click on the grid to choose a starting cell.
2. The `handle_input` function in `main.py` detects the grid click and checks if an action has been selected.
3. If both conditions are met, it calls `game_manager.apply_action(mouse_grid_x, mouse_grid_y)`.

### 2.3 Automaton Creation and Execution

1. Inside `apply_action`, the `GameManager` creates an instance of the selected cellular automaton:
   ```python
   automaton = self.selected_action.create_automaton(self.grid, current_player.player_id)
   ```
   
2. This calls the `create_automaton` method in `PlayerAction`, which initializes the appropriate automaton class (e.g., `SimpleExpansion`, `SnakePattern`, or `RootGrowth`) with the player's id and configured parameters.

3. The `set_starting_cell` method is called on the automaton to mark the initial cell:
   ```python
   initial_grid_changes = automaton.set_starting_cell(grid_x, grid_y)
   ```

4. The automaton is then executed by calling its `run` method:
   ```python
   all_changes = initial_grid_changes + automaton.run()
   ```

5. The `run` method in the `CellularAutomaton` base class:
   - Creates a temporary grid for simulation
   - Runs the automaton for the specified number of generations
   - For each generation, it calls the subclass's `simulate_step` method to determine which cells to conquer
   - Collects all changes without modifying the actual grid

6. Each automaton subclass (`SimpleExpansion`, `SnakePattern`, `RootGrowth`) implements its own `simulate_step` method with unique cellular automaton rules.

### 2.4 Animation and Grid Update

1. The collected changes are passed to `start_animation_playback` which sets up the animation state.
2. The animation is updated frame-by-frame in the `update_animation` method.
3. Each step of the animation applies a batch of cell changes to the actual grid.
4. Once all changes are applied, the turn is advanced to the next player.

## 3. Networking Architecture and Fault Handling

Cell Wars implements a peer-to-peer network architecture that allows two players to play over a network connection. Here's a detailed explanation of how it works:

### 3.1 Network Architecture

The networking system uses a simple client-server model:
- One player acts as the host (server)
- The other player joins as a client
- Both communicate using TCP sockets for reliable message delivery

The implementation follows this class hierarchy:
```
┌───────────────────┐
│  NetworkManager   │
│   (Base Class)    │
└─────────┬─────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌───────────┐ ┌───────────┐
│NetworkHost│ │NetworkClient│
└───────────┘ └───────────┘
```

### 3.2 Message Flow and Synchronization

1. **Game Initialization**:
   - Host initializes the game and waits for a client to connect
   - Client connects to the host's IP address
   - Once connected, the game starts with Player 1 (host) going first

2. **Action Execution and Synchronization**:
   - When a player applies an action, all resulting grid changes are captured
   - These changes are serialized into a message:
     ```python
     message = {
         "type": "action_result",
         "action_name": self.selected_action.name,
         "grid_x": grid_x,
         "grid_y": grid_y,
         "changes": all_changes
     }
     ```
   - The message is sent to the other player using `network_manager.send_message()`
   - On the receiving end, the message is processed and the same changes are animated on the receiving player's grid

3. **Message Processing**:
   - Messages are sent with a header containing the message length
   - The receiving side reads the header to determine how many bytes to read
   - Messages are queued for processing in `message_queue`
   - The game regularly checks for new messages via `process_network_messages()`

### 3.3 Network Fault Handling

The game implements several measures to handle network failures:

1. **Connection Monitoring**:
   - The `check_network_connection` method in `GameManager` periodically verifies the connection is active
   - In the main game loop, this check is performed every frame:
     ```python
     if game_manager.is_networked and not game_manager.check_network_connection():
         handle_network_disconnection(screen, game_manager, font, title_font)
     ```

2. **Disconnection Handling**:
   - If a connection loss is detected, `handle_network_disconnection` is called
   - This function displays a "Connection Lost!" message
   - After a brief delay, the game gracefully exits
   - Network resources are properly cleaned up via `network_manager.disconnect()`

3. **Error Handling in Network Operations**:
   - All network operations (send/receive) are wrapped in try-except blocks
   - If an exception occurs, the connection is marked as disconnected
   - The background thread for receiving messages exits safely when errors occur

4. **Clean Network Shutdown**:
   - When the game ends normally, network resources are properly released
   - Sockets are closed and threads are terminated
   - This happens in the `disconnect` method of the `NetworkManager` class

## 4. Cellular Automaton Implementation

Cell Wars features three distinct cellular automaton patterns, each providing unique gameplay strategies:

### 4.1 SimpleExpansion (Diamond Bomb)

This pattern expands outward in four directions (up, down, left, right) from each active cell, creating a diamond-shaped growth pattern. It's the most predictable pattern and good for claiming nearby territory.

Implementation highlights:
- Conquers cells in cardinal directions only (no diagonals)
- Default of 3 generations of growth
- Cannot overwrite enemy cells by default

### 4.2 SnakePattern (Snake Attack)

A more aggressive pattern that creates a winding, snake-like path across the grid. The snake can change direction randomly and can overwrite enemy cells, making it an offensive choice.

Implementation highlights:
- Picks a random initial direction and can change direction randomly
- When blocked, tries to find an alternative path
- Can overwrite both neutral and enemy cells
- Runs for more generations (20 by default)

### 4.3 RootGrowth (Root Growth)

Simulates organic root growth with branching patterns. It starts with high probability of growth that decreases with each generation and direction.

Implementation highlights:
- Grows in all eight directions (including diagonals)
- Each new direction has a decreasing probability of being taken
- Growth probability diminishes with each generation
- Creates natural-looking patterns with branches

## 5. Game Flow and Turn Management

The game follows a structured turn-based flow:

1. Player selects an action from their available moves
2. Player selects a target cell on the grid
3. The cellular automaton executes and conquers cells
4. The animation plays to show the cells being conquered
5. The turn switches to the other player
6. After a set number of turns, the game ends and the player with more cells wins

In networked games, this flow is synchronized between players, with each player able to act only during their turn.

## 6. Conclusion

Cell Wars demonstrates a well-structured game with clean separation of concerns between its components. The cellular automaton system provides varied gameplay through different patterns, while the networking system allows for multiplayer functionality with robust error handling.

The modular architecture makes it easy to extend the game with new cellular automaton patterns or additional features while maintaining the existing game flow and structure.