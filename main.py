import pygame
import numpy as np
import sys

# Configuration variables
width: int = 800  # Window width in pixels
height: int = 800  # Window height in pixels
max_iter: int = 256  # Maximum number of iterations for the Mandelbrot calculation

# Initial Mandelbrot boundaries (in the complex plane)
xmin: float = -2.5  # Minimum value on the real axis
xmax: float = 1.5  # Maximum value on the real axis
ymin: float = -2.0  # Minimum value on the imaginary axis
ymax: float = 2.0  # Maximum value on the imaginary axis

# Colors for the Mandelbrot set visualization
colors: list[pygame.Color] = [pygame.Color(0, 0, 0)]  # Initialize color list with black
for i in range(1, max_iter):
    # Append a color based on a simple gradient
    colors.append(pygame.Color(i % 256, i % 128, i % 64))

def mandelbrot(c: complex, max_iter: int) -> int:
    """
    Compute the number of iterations for the Mandelbrot set.

    Parameters:
        c (complex): The complex number representing a point in the complex plane.
        max_iter (int): The maximum number of iterations to perform.

    Returns:
        int: The number of iterations before the sequence escapes to infinity.
             If the sequence does not escape, returns max_iter - 1.
    """
    z: complex = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n  # Return the number of iterations before escape
        z = z * z + c
    return max_iter - 1  # Return max_iter - 1 if the point does not escape

def draw_mandelbrot(surface: pygame.Surface, xmin: float, xmax: float, ymin: float, ymax: float, max_iter: int) -> None:
    """
    Draw the Mandelbrot set on the Pygame surface.

    Parameters:
        surface (pygame.Surface): The surface to draw the Mandelbrot set on.
        xmin (float): The minimum bound on the real axis.
        xmax (float): The maximum bound on the real axis.
        ymin (float): The minimum bound on the imaginary axis.
        ymax (float): The maximum bound on the imaginary axis.
        max_iter (int): The maximum number of iterations for Mandelbrot calculation.

    Returns:
        None
    """
    font: pygame.font.Font = pygame.font.SysFont('Arial', 15)  # Font for axis labels

    for x in range(width):
        for y in range(height):
            # Map pixel position to a point in the complex plane
            re: float = xmin + (x / width) * (xmax - xmin)
            im: float = ymin + (y / height) * (ymax - ymin)
            c: complex = complex(re, im)
            color: int = mandelbrot(c, max_iter)  # Get color based on iteration count
            surface.set_at((x, y), colors[color])
        
        # Update the display after each column is drawn
        pygame.display.flip()

        # Draw the progress bar
        pygame.draw.rect(surface, (255, 255, 255), [0, height - 20, width, 20])
        progress: float = (x + 1) / width
        pygame.draw.rect(surface, (0, 255, 0), [0, height - 20, int(progress * width), 20])
        pygame.display.flip()

    # Draw axes and labels on the display
    pygame.draw.line(surface, (255, 255, 255), (0, height//2), (width, height//2), 1)
    pygame.draw.line(surface, (255, 255, 255), (width//2, 0), (width//2, height), 1)

    # Draw axis labels
    x_ticks: np.ndarray = np.linspace(xmin, xmax, 9)  # Generate ticks for the real axis
    y_ticks: np.ndarray = np.linspace(ymin, ymax, 9)  # Generate ticks for the imaginary axis
    
    for i, xt in enumerate(x_ticks):
        label: pygame.Surface = font.render(f"{xt:.2f}", True, (255, 255, 255))
        surface.blit(label, (i * (width // 8), height // 2 + 5))
        
    for i, yt in enumerate(y_ticks):
        label: pygame.Surface = font.render(f"{yt:.2f}", True, (255, 255, 255))
        surface.blit(label, (width // 2 + 5, height - i * (height // 8)))

    pygame.display.flip()

def main() -> None:
    """
    The main function that initializes the Pygame window, handles events,
    and allows the user to interact with the Mandelbrot set visualization.

    Returns:
        None
    """
    global xmin, xmax, ymin, ymax  # Access global variables for zooming
    pygame.init()  # Initialize Pygame
    screen: pygame.Surface = pygame.display.set_mode((width, height))  # Set up the display window
    pygame.display.set_caption("Mandelbrot Set")  # Set the window title

    is_drawing: bool = True  # Flag to control drawing state
    draw_mandelbrot(screen, xmin, xmax, ymin, ymax, max_iter)  # Draw the initial Mandelbrot set
    is_drawing = False  # Drawing is done

    zoom_factor: float = 0.1  # Factor by which to zoom in/out
    running: bool = True  # Main loop flag
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the main loop if the window is closed
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_drawing:
                x_click, y_click = event.pos  # Get the position of the mouse click

                # Map the click position to the complex plane
                re_center: float = xmin + (x_click / width) * (xmax - xmin)
                im_center: float = ymin + (y_click / height) * (ymax - ymin)

                if event.button == 1:  # Left-click to zoom in
                    zoom_width: float = (xmax - xmin) * zoom_factor
                    zoom_height: float = (ymax - ymin) * zoom_factor
                elif event.button == 3:  # Right-click to zoom out
                    zoom_width = (xmax - xmin) / zoom_factor
                    zoom_height = (ymax - ymin) / zoom_factor
                else:
                    continue  # Ignore other mouse buttons

                # Update the boundaries for the zoomed area
                xmin = re_center - zoom_width / 2
                xmax = re_center + zoom_width / 2
                ymin = im_center - zoom_height / 2
                ymax = im_center + zoom_height / 2

                screen.fill((0, 0, 0))  # Clear the screen before redrawing

                is_drawing = True  # Set drawing flag
                draw_mandelbrot(screen, xmin, xmax, ymin, ymax, max_iter)  # Redraw Mandelbrot set
                is_drawing = False  # Drawing is done

    pygame.quit()  # Quit Pygame
    sys.exit()  # Exit the program

if __name__ == "__main__":
    main()  # Execute the main function
