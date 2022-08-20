import pygame
import requests
import numpy

WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
buffer = 5
dimension = 9
grid = [[0]*dimension for i in range(dimension)]
grid_original = [[0]*dimension for i in range(dimension)]

def init_sudoku(difficulty):
    global grid_original
    result = ""
    init_string = "https://sugoku.herokuapp.com/board?difficulty=" + difficulty

    response = requests.get(init_string)
    grid_original = response.json()['board']
    for i in range(0, dimension):
        for j in range(0, dimension):
            if grid_original[i][j] == 0:
                result += "."
            else:
                result += str(grid_original[i][j])
    return result

def insert_value(win, position, value):
    i, j = position[0], position[1]
    font = pygame.font.SysFont('Comic San MS', 35)
    global grid_original
    while True:
        if grid_original[i-1][j-1] != 0:
            return
        if value == 0: 
            pygame.draw.rect(win, background_color, (position[1]*50 + buffer, position[0]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
            pygame.display.update()
            return
        if (0 < value < 10):
            pygame.draw.rect(win, background_color, (position[1]*50 + buffer, position[0]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
            temp = font.render(str(value), True, (0, 0, 0))
            win.blit(temp, (position[1]*50 + 19, position[0]*50 + 15))
            pygame.display.update()
            return
        return

def caculate_position_in_grid(index):
    mode_row = 0
    if index >= 27:
        mode_row = int(index/27)
        index = index % 27

    mode_col = 0
    if index >= 9:
        mode_col = int(index/9)
        index = index % 9

    col = index % 3
    row = int(index/3)

    if mode_col != 0:
        col += mode_col * 3

    if mode_row != 0:
        row += mode_row * 3
    return (row+1, col+1)

def draw_sudoku(assignment):
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    font = pygame.font.SysFont('Comic San MS', 35)

    for i in range(0, 10):
        if i%3 == 0:
            pygame.draw.line(win, (220, 20, 60), (50 + 50*i, 50), (50 + 50*i, 500), 4)  #(surface, color, start_pos, end_pos, width)
            pygame.draw.line(win, (220, 20, 60), (50, 50 + 50*i), (500, 50 + 50*i), 4)

        pygame.draw.line(win, (0, 0, 0), (50 + 50*i, 50), (50 + 50*i, 500), 2)  
        pygame.draw.line(win, (0, 0, 0), (50, 50 + 50*i), (500, 50 + 50*i), 2)
    pygame.display.update()

    i_grid = 0
    j_grid = 0
    for i in assignment:
        if i != ".":
            value = i
            value = font.render(value, True, original_grid_element_color)
            win.blit(value, ((i_grid+1)*50 + 19, (j_grid+1)*50 + 15))
        i_grid += 1
        if i_grid == dimension:
            i_grid = 0
            j_grid += 1

    pygame.display.update()
    return win
