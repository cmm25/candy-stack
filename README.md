# Stack Game

This is a simple stack game implemented using the Pygame library in Python. The game simulates a stack data structure with candies being pushed onto the stack and popped off the stack.

## Game Elements

### Colors

- **SILVER**: (192, 192, 192)
- **BLACK**: (0, 0, 0)
- **WHITE**: (255, 255, 255)
- **ORANGE**: (255, 165, 0)
- **RED**: (255, 0, 0)
- **GREEN**: (0, 255, 0)
- **BLUE**: (0, 0, 255)
- **BACKGROUND**: (228, 213, 199)

### Fonts

- **Arial, 25**: Main font for general text
- **Arial, 20**: Font for displaying candy names

### Classes

#### `PushedContainer`

- Represents a container that holds a pushed candy on the stack.
- Attributes:
  - `candy`: Candy name
  - `height`: Height of the container
  - `container_color`: Color of the container
  - `rect`: Pygame Rect object representing the container's position and size

#### `Button`

- Represents a clickable button in the game.
- Attributes:
  - `text`: Text displayed on the button
  - `color`: Color of the button
  - `x`, `y`: Position of the button
  - `width`, `height`: Dimensions of the button
- Methods:
  - `draw(screen)`: Draws the button on the specified Pygame screen
  - `is_over(mouse_pos)`: Checks if the mouse cursor is over the button

#### `Stack`

- Represents a stack data structure.
- Generic class that can hold instances of `PushedContainer`.

### Game Loop

The main game loop continuously checks for user input and updates the screen accordingly.

- **Pop Button**: Pops a candy container from the stack. If the stack is empty, displays an alert.
- **Push Button**: Pushes a new candy container onto the stack.
- **Peek Button**: Toggles the display of the top item on the stack.
- **Is Empty Button**: Toggles the display of whether the stack is empty.
- **Length Button**: Toggles the display of the stack size.

### Stack Visualization

- The stack is visualized as a vertical arrangement of candy containers.
- Containers are pushed onto the stack, and the spring at the bottom reflects the size of the stack.

### Additional Features

- Randomly selects candy names and container colors.
- Displays information such as stack size, top item, and stack emptiness status.

### Alerts

- An alert box is displayed when attempting to pop from an empty stack.

## Modifications

### Displaying Popped Item

- Added functionality to display the last popped item on the screen.

### Usage

1. Run the script.
2. Use the Pop, Push, Peek, Is Empty, and Length buttons to interact with the stack.

Enjoy playing the stack game!
