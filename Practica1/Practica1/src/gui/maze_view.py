import tkinter as tk

CELL_SIZE = 30

def animate_maze(grid, exploration, path):

    n = len(grid)

    window = tk.Tk()
    window.title("BFS Animado - Laberinto")

    canvas = tk.Canvas(window,
                       width=n * CELL_SIZE,
                       height=n * CELL_SIZE)
    canvas.pack()

    rectangles = {}

    for r in range(n):
        for c in range(n):

            x1 = c * CELL_SIZE
            y1 = r * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            color = "black" if grid[r][c] == 1 else "white"

            rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
            rectangles[(r, c)] = rect

    def animate_exploration(index=0):

        if index < len(exploration):

            r, c = exploration[index]

            if grid[r][c] == 0:
                canvas.itemconfig(rectangles[(r, c)], fill="lightblue")

            window.after(20, animate_exploration, index + 1)

        else:
            animate_path()

    def animate_path(index=0):

        if index < len(path):

            r, c = path[index]
            canvas.itemconfig(rectangles[(r, c)], fill="green")

            window.after(50, animate_path, index + 1)

    animate_exploration()

    window.mainloop()