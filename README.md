# Mandelbrot Set Visualization

This project provides two implementations of the Mandelbrot set visualization using Python and Pygame. The Mandelbrot set is a complex fractal, and this project allows you to zoom in and explore its intricate details interactively.

## Project Structure

- **`.gitignore`**: Specifies the files and directories that should be ignored by Git, including bytecode, build directories, virtual environments, and more.
- **`main.py`**: A basic implementation of the Mandelbrot set visualization.
- **`main2.py`**: An optimized implementation that utilizes multithreading to speed up the computation.

## Requirements

- Python 3.x
- Pygame
- NumPy

You can install the required packages using pip:

```bash
pip install pygame numpy
```

## Running the Project

To run the basic Mandelbrot set visualization:

```bash
python main.py
```

To run the optimized version with multithreading:

```bash
python main2.py
```

## Mandelbrot Set

The Mandelbrot set is a set of complex numbers defined by the iterative equation:

\[ z_{n+1} = z_n^2 + c \]

where z0z0​ is initially zero, and cc is a complex number. The set is defined as the set of all cc values for which the sequence znzn​ does not diverge to infinity. This project visualizes the Mandelbrot set by mapping points in the complex plane to pixels on the screen and using a color gradient to represent the number of iterations required to determine if the point is in the Mandelbrot set.

## Features

- Zooming: Use the left mouse button to zoom in and the right mouse button to zoom out.
- Multithreading (in main2.py): Utilizes multiple threads to accelerate the calculation of the Mandelbrot set.

## Code Explanation

main.py

- mandelbrot(c, max_iter): Computes the number of iterations before the point diverges.
- draw_mandelbrot(surface, xmin, xmax, ymin, ymax, max_iter): Draws the Mandelbrot set on the Pygame surface and updates the display.
- main(): Handles user input and manages the zooming functionality.

main2.py

- mandelbrot(c, max_iter): Computes the Mandelbrot set using NumPy arrays and handles large chunks of data concurrently.
- draw_mandelbrot(surface, xmin, xmax, ymin, ymax, max_iter): Divides the computation into chunks and processes them in parallel using the concurrent.futures module.
- draw_axes(surface, xmin, xmax, ymin, ymax): Draws axes and labels on the Pygame surface.
- main(): Similar to main.py, but optimized with multithreading.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contribution

Feel free to fork this repository, open issues, and submit pull requests.

## Acknowledgments

- Pygame
- NumPy