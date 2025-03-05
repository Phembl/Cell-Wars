### How does the automaton run

The Game Loop runs handle_input ->
<br>handle_input checks if an action is selected and the grid is clicked. If so, it tells the
GameManager to apply_action with the starting coordinate on the grid. The action is already saved from
clicking the button ->
<br>The GameManager gets the associated CA from the action, passes the starting coordinates and tells the CA to run() ->
<br>The CellularAutomaton runs itself by iterating through the next step() (if possible).->
<br>Step() is passed from the CA parent class to the currently active CA subclass where the actual 
calculation on which cell to use next happens. Grid.set_cell is called here to set the cell in the respective player color.




### Question:

In the Move (PlayerAction) class: Why do we need to use a default value for generations and overwrite_neutral/ enemy if we already have it build into the cellular automaton class?


### Answer:
You've identified an interesting case of seemingly redundant default values. There's actually a specific reason for having defaults in both classes:

### Why Have Defaults in Both Places

1. **Separation of Concerns**:
   - The defaults in `CellularAutomaton` represent the technical defaults for the pattern implementation
   - The defaults in `PlayerAction` represent the game design defaults for player abilities

2. **Explicit Configuration**:
   - When creating an action, we explicitly pass our configured values to the automaton
   - This makes it clear what values we're using rather than relying on the automaton's internal defaults

3. **Different Contexts**:
   - `CellularAutomaton` could potentially be used directly in other contexts (like AI moves or special events)
   - `PlayerAction` is specifically for player-triggered actions

### The Chain of Defaults

When the game runs, here's what happens:

1. We define a `PlayerAction` with specific parameters:
   ```python
   snake_action = PlayerAction("Snake", "Creates a winding path", SnakePattern, generations=10)
   ```

2. When used, `create_automaton()` explicitly passes these values to the automaton:
   ```python
   automaton = self.automaton_class(grid, player_id, 
                                   generations=self.generations,
                                   overwrite_neutral=self.overwrite_neutral,
                                   overwrite_enemy=self.overwrite_enemy)
   ```

3. The automaton receives these explicit values, overriding its own defaults

So in practice, the automaton's default values rarely come into play when used through `PlayerAction`. They're more of a fallback for direct usage or testing.

This approach gives us more flexibility in how we configure actions without modifying the underlying patterns.