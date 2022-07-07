import pygame
import random

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Fire Forest")

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
GREY = (128,128,128)

class Spot: # node
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_forest(self):
        return self.color == GREEN
    
    def is_fire(self):
        return self.color ==  RED

    def is_desert(self):
        return self.color == WHITE

    def setForest(self):
        self.color = GREEN

    def setFire(self):
        self.color = RED

    def setDesert(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # fire logic
        if grid[self.row][self.col].is_forest():
            for i in range(-1,1): # to get left, right, up and down
                if grid[self.row + i][self.col].is_fire():
                    grid[self.row][self.col].setFire()
                if grid[self.row][self.col + i].is_fire():
                    grid[self.row][self.col].setFire()
        elif grid[self.row][self.col].is_fire():
            grid[self.row][self.col].setDesert()
        # do forest logic
        if grid[self.row][self.col].is_desert():
            for i in range(-1, 1):
                if grid[self.row + i][self.col].is_forest() and grid[self.row][self.col + i].is_forest():
                    grid[self.row][self.col].setForest()            
        # do desert logic
        for i in range(-1, 1):
            if grid[self.row + i][self.col].is_desert() and grid[self.row][self.col + i].is_desert():
                grid[self.row][self.col].setDesert()
        # more logic fire -> messed up all the fun, it has to be fixed
        if random.randint(0,98):
            if grid[self.row][self.col].is_forest():
                grid[self.row][self.col].setFire()

def make_grid(rows, width):
    grid = []
    color = [WHITE,GREEN,RED]
    gap = width // rows # integer division
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            spot.color = color[random.randint(0,1)] # 0,1 to just get desert and florest, 0,2 to get fire too
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                
                if event.key == pygame.K_c:
                    grid = make_grid(ROWS, WIDTH)

    pygame.quit()

main(WIN, WIDTH)