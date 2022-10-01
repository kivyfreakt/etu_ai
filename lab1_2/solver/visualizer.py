'''
    Визуализация головоломки
'''

import sys
from tkinter import Tk, Canvas

GUI_FONT = ("Arial", 32)
GUI_BOX_SIZE = 100
GUI_BOX_SPACING = 10
GUI_BOX_BORDER_WIDTH = 3
GUI_DELAY = 200
PUZZLE_SIZE = 3

GUI_COLOR_1 = "#f5f5dc"
GUI_COLOR_2 = "#e9e9af"
GUI_COLOR_3 = "#dddd88"

GUI_OUTLINE_1 = "#ff0000"
GUI_OUTLINE_2 = "#00ff00"
GUI_OUTLINE_3 = "#0000ff"

GUI_COLOR_GREEN = "#00bb00"
GUI_COLOR_RED = "#bb0000"
GUI_COLOR_BLACK = "#000000"

GUI_DASH = (5, 4, 5, 3)

def gui_replay(master, frame, canvas, item_matrix, solution):
    ''' Проигрывание анимации'''
    numbers = solution[frame]
    next_zero = None
    color_this = None
    if frame + 1 < len(solution):
        next_zero = solution[frame + 1].index(0)
        color_this = solution[frame][next_zero]

    for row in range(PUZZLE_SIZE):
        for col in range(PUZZLE_SIZE):
            num = numbers[row + PUZZLE_SIZE * col]
            border_color = None
            if num == solution[-1][row + PUZZLE_SIZE * col]:
                border_color = GUI_COLOR_GREEN
            else:
                border_color = GUI_COLOR_RED

            if num == 0:
                canvas.itemconfig(
                    item_matrix[row][col][0],
                    fill=GUI_COLOR_2,
                    outline=GUI_COLOR_2,
                    width=GUI_BOX_BORDER_WIDTH,
                )
            elif num == color_this:
                canvas.itemconfig(
                    item_matrix[row][col][0],
                    fill=GUI_COLOR_1,
                    outline=border_color,
                    width=GUI_BOX_BORDER_WIDTH,
                )
            else:
                canvas.itemconfig(
                    item_matrix[row][col][0],
                    fill=GUI_COLOR_1,
                    outline=border_color,
                    width=GUI_BOX_BORDER_WIDTH,
                )

            num_string = str(num)
            if not num:
                num_string = ""
            canvas.itemconfig(item_matrix[row][col][1], text=num_string)

    frame += 1
    if frame >= len(solution):
        frame = 0
    canvas.update()

    if frame != 0:
        master.after(
            GUI_DELAY, gui_replay, master, frame, canvas, item_matrix, solution)


def gui_close(_event):
    ''' Закрытие приложения '''
    sys.exit(0)


def gui_item_matrix(canvas):
    ''' Составление матрицы '''
    item_matrix = [
        [[None, None] for col in range(PUZZLE_SIZE)] for row in range(PUZZLE_SIZE)
    ]
    for row in range(PUZZLE_SIZE):
        for col in range(PUZZLE_SIZE):

            row0 = row * GUI_BOX_SIZE + GUI_BOX_SPACING
            col0 = col * GUI_BOX_SIZE + GUI_BOX_SPACING
            row1 = row0 + GUI_BOX_SIZE - GUI_BOX_SPACING
            col1 = col0 + GUI_BOX_SIZE - GUI_BOX_SPACING
            item_matrix[row][col][0] = canvas.create_rectangle(
                row0, col0, row1, col1, dash=GUI_DASH, fill=GUI_COLOR_1
            )

            row_t = row0 + ((GUI_BOX_SIZE - GUI_BOX_SPACING) / 2)
            col_t = col0 + ((GUI_BOX_SIZE - GUI_BOX_SPACING) / 2)
            item_matrix[row][col][1] = canvas.create_text(
                (row_t, col_t), font=GUI_FONT, text="")

    return item_matrix


def visualizer(solution):
    ''' Функция визуализации решения '''
    master = Tk()
    canvas_width = (GUI_BOX_SIZE * PUZZLE_SIZE) + GUI_BOX_SPACING
    canvas_height = (GUI_BOX_SIZE * PUZZLE_SIZE) + GUI_BOX_SPACING
    canvas = Canvas(
        master,
        width=canvas_width + 1,
        height=canvas_height + 1,
        bg=GUI_COLOR_2,
        borderwidth=0,
        highlightthickness=0,
    )
    canvas.pack()
    # MANUAL_MODE = manual_mode
    item_matrix = gui_item_matrix(canvas)
    master.bind("<Escape>", gui_close)
    master.after(0, gui_replay, master, 0, canvas,
                 item_matrix, solution)
    master.mainloop()
