# pathfinding

the grid is 50x50 with cords x0 y0 to x49 y49

the grid you are selecting can be seen on title aswell as the block details (default \[-1\])

the format for block details is as follows:

\[block type, total cost, distance to end, distance to start, coming from x, coming from y\]

Blocks:

-1 = empty

0 = black (obstacle)

1 = green (start)

2 = red (end)

the following cannot be placed

3 = yellow (todo)

4 = orange (done)

5 = blue (solved path)

Controls

LMB
place current block type

RMB
switch block type (block type can be seen at bottom)

LCTRL+C
Clear entire grid

LCTRL+S
Saves grid to 'save.json' (will override)

LCTRL+R
clears screen and adds random blocks across it (block 0)

LCTRL+`
starts solving from green (block 1) to red (block 2) and if not found it wont solve

LCTRL+O
opens and loads from save.json (will remove/clean duplicate green or red blocks)

LALT+C
clears only solution blocks (blocks 3-5)
