from tkinter import *
from random import *
from copy import deepcopy
from time import sleep
from easygui import *

# create the Gui of the menu
# message to be displayed
text = "Please enter the following details:"
# window title
title = "Cellular automatons and coronavirus vaccines MENU"
# list of multiple inputs
input_list = ["Please enter number of healthy people", "Please enter number of sick people",
              "Please enter number of vaccinated people", "Please enter number of Generation",
              "Please enter the probability that a healthy person will be infected from a sick neighbor (PI)",
              "Please enter the probability that a vaccinated person will be infected from a sick neighbor (PV)"]
# list of default text
default_list = ["19500", "400", "100", "20", "0.7", "0.05"]
# creating a integer box
output = multenterbox(text, title, input_list, default_list)

# size of the matrix 250*250
matrix_size = 250
# number of vaccinated - user input
Nv = int(output[2])
# number of sick - user input
Ns = int(output[1])
# number of healthy - user input
Nh = int(output[0])
# number of generation to show - user input
gen_limit = int(output[3])
# probability that a healthy who is near to to a sick will be infected
Pi = float(output[4])
# probability that a vaccinated who is near to to a sick will be infected
Pv = float(output[5])
# number of generations after which a sick person becomes vaccinated
Sick2vaccinated = 4     # CONST
VACCINATED, SICK, EMPTY, HEALTHY = 0, Sick2vaccinated, Sick2vaccinated + 1, Sick2vaccinated + 2
state_list = list(range(Sick2vaccinated + 3))
# white - empty, lime - vaccinated, red - sick, blue - healthy
color = ['lime']
for i in range(Sick2vaccinated):
    color.append('red')
color.append('white')
color.append('blue')
# initialize a global empty matrix
matrix = [[EMPTY for x in range(matrix_size)] for y in range(matrix_size)]
# size of each cell in the matrix
scale = 3


# initialize each state in the matrix
def start_matrix_helper(n, occ, state):
    for i in range(n):
        # get a random number in occ
        loc = choice(occ)
        # get the x location in the matrix
        loc_x = loc % matrix_size
        # get the y location in the matrix
        loc_y = int(loc / matrix_size)
        occ.remove(loc)
        # update the matrix in the given state
        matrix[loc_x][loc_y] = state
    return occ


# initialize the matrix at random
def start_matrix(nv, ns, nh):
    # list of all numbers between 0 and size^2-1
    occupied = list(range(matrix_size ** 2))
    occupied = start_matrix_helper(nv, occupied, VACCINATED)
    occupied = start_matrix_helper(ns, occupied, SICK)
    start_matrix_helper(nh, occupied, HEALTHY)

    # create cells in the matrix and the boundaries
    for y in range(matrix_size):
        row = []
        # paint each cell in black
        for x in range(matrix_size):
            start_x = x * scale + 1
            end_x = x * scale + scale + 3
            start_y = y * scale + 1
            end_y = y * scale + scale + 3
            row.append(
                canvas.create_rectangle(
                    start_x, start_y, end_x, end_y,
                    fill='black',
                )
            )


# paint each cell according to the state
def paint(mat):
    for x in range(matrix_size):
        for y in range(matrix_size):
            loc = boxes[x][y]
            for state in state_list:
                if mat[x][y] == state:
                    canvas.itemconfig(loc, fill=color[state])


# update the matrix after infection according to the neighbors of each cell
def after_infection(mat):
    new_mat = deepcopy(mat)
    for x in range(matrix_size):
        for y in range(matrix_size):
            if mat[x][y] == HEALTHY or mat[x][y] == VACCINATED:
                # check the neighbors
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        # if there are sick neighbors
                        if VACCINATED < mat[i % matrix_size][j % matrix_size] <= Sick2vaccinated:
                            # in case the state is healthy
                            if mat[x][y] == HEALTHY:
                                if random() < Pi:
                                    new_mat[x][y] = SICK
                            # in case the state is vaccinated
                            else:
                                if random() < Pv:
                                    new_mat[x][y] = SICK
            # a sick person infects for T generations and then becomes vaccinated and stops infecting
            if 0 < new_mat[x][y] <= Sick2vaccinated:
                new_mat[x][y] -= 1
    return new_mat


# This function is responsible for making sure that
# two people wont enter the same cell, in the same generation.
# update the matrix after the moves of the cells
def after_move(mat):
    # Create a new matrix
    new_mat = [[EMPTY for x in range(matrix_size)] for y in range(matrix_size)]
    # Going through the cells in the matrix
    for x in range(matrix_size):
        for y in range(matrix_size):
            # if the current cell isn't empty
            if mat[x][y] != EMPTY:
                cell_neighborhood = []
                # pass over the neighbors
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        #   check if there are available cells to move in
                        if new_mat[i % matrix_size][j % matrix_size] == EMPTY:
                            # the connection between the main matrix and the cell neighborhood
                            cell_neighborhood.append((i - x + 1) * 3 + j - y + 1)
                # choose random cell to move
                loc = choice(cell_neighborhood)
                # extract the location of the cell (x,y)
                loc_x = int(loc / 3)
                loc_y = loc % 3
                # update the matrix
                new_mat[(loc_x + x - 1) % matrix_size][(loc_y + y - 1) % matrix_size] = mat[x][y]
    return new_mat


# Gui of the model
root = Tk()
root.title('Cellular automatons and coronavirus vaccines')
data_frame = Frame(root)
canvas_frame = Frame(root)

boxes = []
for i in range(matrix_size):
    rows = []
    for j in range(1, matrix_size + 1):
        rows.append(i * matrix_size + j)
    boxes.append(rows)

canvas = Canvas(
    root,
    bd=0,
    height=matrix_size * scale,
    width=matrix_size * scale
)
canvas.config(bg='black')
canvas.pack()

# activate the model
start_matrix(Nv, Ns, Nh)
paint(matrix)
root.update()
sleep(1)

gen_counter = 0
# paint the generations until the generation limit
while gen_counter < gen_limit:
    matrix = after_infection(matrix)
    matrix = after_move(matrix)
    paint(matrix)
    root.update()
    sleep(1)
    gen_counter += 1

# count the number of Nh, Nv, Ns after gen_limit generations
H, V, S = 0, 0, 0
for x in range(matrix_size):
    for y in range(matrix_size):
        if matrix[x][y] == HEALTHY:
            H += 1
        if VACCINATED < matrix[x][y] <= Sick2vaccinated:
            S += 1
        if matrix[x][y] == VACCINATED:
            V += 1

# create the gui of the menu
# message to be displayed
text = "The board in the end of the Game:"
# window title
title = "Cellular automatons and coronavirus vaccines FINAL DETAILS"
# list of multiple inputs
input_list = ["FINAL Helthy: ", "FINAL Sick: ",
              "FINAL Vaccinated: ", "gen_limit: ",
              "Pi: ", "Pv: ", "T: "]
# list of default text
default_list = [H, S, V, gen_limit, Pi,Pv, Sick2vaccinated]
# creating a integer box
output = multenterbox(text, title, input_list, default_list)

'''
import tkinter as tk
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
GREED_SIZE = 5

class Person:
    def __init__(self, doubt, l, color="white"):
        self.doubt_level = doubt
        # self.location = location
        self.rumor_cooldown = l
        self.is_triggered = False
        self.color = color


class App:
    def __init__(self, master, P=0.3):
        self.master = master
        master.title("Person Interaction GUI")
        self.P = P
        self.people = [[None for _ in range(GREED_SIZE)] for _ in range(GREED_SIZE)]
        self.cells = [[None for _ in range(GREED_SIZE)] for _ in range(GREED_SIZE)]
        self.cell_size = min(SCREEN_WIDTH // GREED_SIZE, SCREEN_HEIGHT // GREED_SIZE)
        self.create_people()
        self.create_gui()

    def create_people(self):
        # multiplying the values help up control the distribution of doubt levels.
        doubt_levels = ["S1"] * 70 + ["S2"] * 10 + ["S3"] * 10 + ["S4"] * 10
        for row in range(GREED_SIZE):
            for column in range(GREED_SIZE):
                if random.random() < self.P:
                    doubt_level = random.choice(doubt_levels)
                    color = "green"
                    if (doubt_level == "S1"):
                        color = "red"
                    self.people[row][column] = Person(doubt=doubt_level, l=0, color=color)

    def create_gui(self):
        # create the grid of cells
        for row in range(GREED_SIZE):
            for col in range(GREED_SIZE):
                if self.people[row][col] is not None:
                    cell = tk.Canvas(self.master, width=self.cell_size, height=self.cell_size,
                                     bg=self.people[row][col].color)
                else:
                    cell = tk.Canvas(self.master, width=self.cell_size, height=self.cell_size, bg='light grey')
                cell.grid(row=row, column=col, padx=1, pady=1)
                # cell_label = tk.Label(cell, text=self.people[row][col].name, font=('Arial', 8))
                # cell_label.pack(pady=15)
                self.cells[row][col] = cell

        # bind the left click event to the cells
        for row in range(GREED_SIZE):
            for col in range(GREED_SIZE):
                if self.people[row][col] is not None:
                    self.cells[row][col].bind('<Button-1>', lambda event, row=row, col=col: self.cell_clicked(row, col))

    def cell_clicked(self, row, col):
        # set the color of the clicked cell to a random color
        self.people[row][col].color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
        self.cells[row][col].configure(bg=self.people[row][col].color)

        # change the color of the surrounding cells
        for i in range(max(0, row - 1), min(GREED_SIZE, row + 2)):
            for j in range(max(0, col - 1), min(GREED_SIZE, col + 2)):
                if i != row or j != col:
                    # ensures only surrounding cells that contain people will be affected.
                    # TODO:
                    # person who recieved the rumor should spread it in the next turn
                    if self.people[i][j]:
                        self.people[i][j].color = self.people[row][col].color
                        self.cells[i][j].configure(bg=self.people[i][j].color)



root = tk.Tk()
app = App(root)
root.mainloop()

'''