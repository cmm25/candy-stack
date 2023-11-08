import sys
from typing import TypeVar, Generic

import pygame
import random
import tkinter as tk
from tkinter import messagebox

from pygame import Vector2, Rect

# Initialize pygame
pygame.init()

# Define colors
SILVER = (192, 192, 192)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND = (228, 213, 199)

# Define screen size and title
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Stack Game")

# Define font
font = pygame.font.SysFont("Arial", 32)

# Define stack class
T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self):
        self.items: list[T] = []

    def is_empty(self):
        return not bool(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1] if not self.is_empty() else None

    def size(self):
        return len(self.items)


# Define PushedContainer class
class PushedContainer:
    def __init__(self, candy, container_color, mid_bottom: tuple[float, float]):
        self.size = 150, 50
        self.candy = candy
        self.x = x
        self.y = y
        self.height = height
        self.container_color = container_color
        self.rect = Rect((0, 0), self.size)
        self.rect.midbottom = mid_bottom


stack: Stack[PushedContainer] = Stack()
candy_names = ["Snickers", "Kit Kat", "Twix", "M&M's", "Skittles", "Big Daddy", "Toblerone", "Hershey's", "Reese's",
               "Milky Way", "Butterfinger", "Twizzlers"]

pushed_containers = []


# Define button class
class Button:
    def __init__(self, text, color, x, y, width, height):
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
        screen.blit(text_surface, text_rect)

    def is_over(self, mouse_pos):
        x, y = mouse_pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


# Game loop
running = True
clock = pygame.time.Clock()
fps = 60

# Define a gap between the buttons row and the main container
gap_between_buttons_and_container = 30

# Reduce the gap between "Is Empty" output and the buttons by 5 pixels
gap_between_is_empty_and_buttons = 25

# Load the spring image
spring_image = pygame.image.load("spring.png").convert_alpha()
spring_image = pygame.transform.scale_by(spring_image, (1, 0.85))
spring_image_rect = Rect(Vector2(0, 0),
                         spring_image.get_rect().size)

# Define container variables
container_x = screen_width // 2 - 300
container_y = screen_height - 500 + gap_between_buttons_and_container
container_width = spring_image.get_width() - 235
container_height = 450
container_color = WHITE

spring_image_rect.midbottom = Vector2(container_x + (container_width / 2), container_y + container_height)

height = 10
gap = 20

spring_shrink_rate = 0.9  # Rate at which the spring grows
spring_grow_rate = 1 / spring_shrink_rate  # Rate at which the spring shrinks
spring_height = spring_image.get_height() - 10

max_pushed_items = len(candy_names)

pop_button = Button("Pop", RED, 50, container_y - 60, 100, 50)
push_button = Button("Push", GREEN, 200, container_y - 60, 100, 50)
peek_button = Button("Peek", BLUE, 350, container_y - 60, 100, 50)
is_empty_button = Button("Is Empty", SILVER, 500, container_y - 60, 122, 50)
length_button = Button("Length", ORANGE, 650, container_y - 60, 100, 50)

# Define container colors for candies
container_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

show_stack_size = False
show_peek_result = False
show_is_empty = False


# Function to display an alert box
def show_alert(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Alert", message)
    root.destroy()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if pop_button.is_over(mouse_pos):
                if not stack.is_empty():
                    stack.pop()
                    show_stack_size = False
                    show_peek_result = False
                    show_is_empty = False
                    if stack.is_empty():
                        spring_image = pygame.image.load("spring.png").convert_alpha()
                        spring_image = pygame.transform.scale_by(spring_image, (1, 0.85))
                    else:
                        spring_image = pygame.transform.smoothscale_by(spring_image,
                                                                       (1, spring_grow_rate)).convert_alpha()
                else:
                    show_alert("Container is empty!")
            if push_button.is_over(mouse_pos) and stack.size() < (container_height - gap) // (
                    height + gap) and stack.size() < max_pushed_items:
                candy = random.choice(candy_names)
                container_color = random.choice(container_colors)
                spring_image = pygame.transform.scale_by(spring_image, (1, spring_shrink_rate))

                if stack.is_empty():
                    pushed_container = PushedContainer(candy, container_color, spring_image_rect.midtop)
                else:
                    pushed_container = PushedContainer(candy, container_color, stack.peek().rect.midtop)

                stack.push(pushed_container)
                # pushed_containers.append(pushed_container)
                show_stack_size = False
                show_peek_result = False
                show_is_empty = False

            if peek_button.is_over(mouse_pos):
                show_peek_result = not show_peek_result
                show_stack_size = False
                show_is_empty = False
            if length_button.is_over(mouse_pos):
                show_stack_size = not show_stack_size
                show_peek_result = False
                show_is_empty = False
            if is_empty_button.is_over(mouse_pos):
                show_is_empty = not show_is_empty
                show_stack_size = False
                show_peek_result = False

    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, WHITE, (container_x, container_y, container_width, container_height))
    border_thickness = 4
    pygame.draw.rect(screen, BLACK, (
        container_x - border_thickness, container_y - border_thickness, container_width + 2 * border_thickness,
        container_height + 2 * border_thickness), border_thickness)

    # Calculate the spring height based on the stack size
    # max_spring_height = container_height - (height + gap) * stack.size()
    # spring_height = min(max_spring_height, spring_height)
    #
    # # Display the spring at the bottom of the container
    # spring_y = container_y + container_height - spring_height
    spring_image_rect = Rect(Vector2(0, 0),
                             spring_image.get_rect().size)
    spring_image_rect.midbottom = Vector2(container_x + (container_width / 2), container_y + container_height)
    # spring_image_rect = container

    screen.blit(spring_image, spring_image_rect)

    x = container_x
    y = container_y + container_height - height - gap
    width = container_width

    for item in stack.items:
        # pygame.draw.rect(screen, item.container_color, (item.x, item.y, 150, 50))
        pygame.draw.rect(screen, item.container_color, item.rect)

        text_surface = font.render(item.candy, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (item.rect.x + 75, item.rect.y + 25)
        screen.blit(text_surface, text_rect)

    # Draw the buttons
    pop_button.draw(screen)
    push_button.draw(screen)
    length_button.draw(screen)
    peek_button.draw(screen)
    is_empty_button.draw(screen)

    # Display stack size, peek result, and is_empty status if enabled
    if show_stack_size:
        # Display the stack size
        stack_size_text = font.render(f"Stack size: {stack.size()}", True, BLACK)
        screen.blit(stack_size_text, (10, 10))

    if show_peek_result:
        # Display the peek result
        peek_result = font.render(f"Top item: {stack.peek()}" if not stack.is_empty() else "Top item: N/A", True, BLACK)
        screen.blit(peek_result, (10, 50))

    if show_is_empty:
        # Display the is_empty status
        is_empty_text = font.render(f"Is Empty: {'Yes' if stack.is_empty() else 'No'}", True, BLACK)
        screen.blit(is_empty_text, (10, 90))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
