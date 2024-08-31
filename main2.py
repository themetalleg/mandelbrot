import pygame
import numpy as np
import concurrent.futures
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

def mandelbrot(c: np.ndarray, max_iter: int) -> np.ndarray:
    """
    Compute the Mandelbrot set for an array of complex numbers.

    Parameters:
        c (np.ndarray): A NumPy array of complex numbers representing points in the complex plane.
        max_iter (int): The maximum number of iterations to perform.

    Returns:
        np.ndarray: An array of integers representing the iteration count before escape for each point.
    """
    z: np.ndarray = np.zeros(c.shape, dtype=np.complex128)  # Initialize z to 0
    divtime: np.ndarray = np.zeros(c.shape, dtype=int) + max_iter  # Array to hold iteration counts
    mask: np.ndarray = np.ones(c.shape, dtype=bool)  # Mask to track points that have not escaped
    
    for i in range(max_iter):
        z[mask] = z[mask] * z[mask] + c[mask]  # Update z for points that have not escaped
        mask, old_mask = np.abs(z) <= 2, mask  # Update mask to include only points that haven't escaped
        divtime[mask ^ old_mask] = i  # Set the iteration count for points that just escaped
    
    return divtime

def draw_mandelbrot(surface: pygame.Surface, xmin: float, xmax: float, ymin: float, ymax: float, max_iter: int) -> None:
    """
    Draw the Mandelbrot set on the Pygame surface using multithreading.

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
    X: np.ndarray = np.linspace(xmin, xmax, width)  # Real axis values
    Y: np.ndarray = np.linspace(ymin, ymax, height)  # Imaginary axis values
    X, Y = np.meshgrid(X, Y)  # Create a grid of complex numbers
    C: np.ndarray = X + 1j * Y  # Combine X and Y to form the complex plane

    # Parallel computation of the Mandelbrot set using multiple threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        chunk_size: int = height // 4  # Divide the height into chunks
        futures = [executor.submit(mandelbrot, C[i:i + chunk_size], max_iter) 
                   for i in range(0, height, chunk_size)]
        results = [f.result() for f in futures]
    
    # Combine the results and update the surface
    for i, result in enumerate(results):
        for x in range(width):
            for y in range(result.shape[0]):
                color: int = result[y, x]
                if color >= len(colors):
                    color = len(colors) - 1  # Ensure color is within bounds
                surface.set_at((x, y + i * chunk_size), colors[color])

        # Update the display after each chunk is drawn
        pygame.display.flip()

        # Draw the progress bar
        pygame.draw.rect(surface, (255, 255, 255), [0, height - 20, width, 20])
        progress: float = (i + 1) / len(results)
        pygame.draw.rect(surface, (0, 255, 0), [0, height - 20, int(progress * width), 20])
        pygame.display.flip()

    # Draw axes and labels on the display
    draw_axes(surface, xmin, xmax, ymin, ymax)
    pygame.display.flip()

def draw_axes(surface: pygame.Surface, xmin: float, xmax: float, ymin: float, ymax: float) -> None:
    """
    Draw the axes and labels on the Pygame surface.

    Parameters:
        surface (pygame.Surface): The surface to draw the axes and labels on.
        xmin (float): The minimum bound on the real axis.
        xmax (float): The maximum bound on the real axis.
        ymin (float): The minimum bound on the imaginary axis.
        ymax (float): The maximum bound on the imaginary axis.

    Returns:
        None
    """
    font: pygame.font.Font = pygame.font.SysFont('Arial', 15)  # Font for axis labels
    
    # Draw the axes
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

                screen.fill((0, 0, 0))  # Clear the screen

                is_drawing = True  # Set drawing flag
                draw_mandelbrot(screen, xmin, xmax, ymin, ymax, max_iter)  # Redraw Mandelbrot set
                is_drawing = False  # Drawing is done

    pygame.quit()  # Quit Pygame
    sys.exit()  # Exit the program

if __name__ == "__main__":
    main()  # Execute the main function
