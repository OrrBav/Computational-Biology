import tkinter as tk
import random

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
GRID_SIZE = 30
COOLDOWN = 3
NEUTRAL = "dark blue"
SPREADER = "dark red"


def believes_rumor(person, rumor_count):
    current_doubt_level = person.doubt_level if rumor_count < 2 else max(0, person.doubt_level - 1)
    # S3 -> 2
    # [False] * 2 + [True] * 1 = [False, False, True]
    # S2 -> 1
    # [False] * 1 + [True] * 2 = [False, True, True]
    doubt_level_choices = [False] * current_doubt_level + [True] * (3 - current_doubt_level)
    return random.choice(doubt_level_choices)


class Person:
    def __init__(self, doubt, location, color="white"):
        self.doubt_level = doubt
        self.location = location
        self.rumor_cooldown = 0
        # self.is_triggered = False
        self.color = color

class App:
    def __init__(self, master, P=0.6):
        self.master = master
        master.title("Person Interaction GUI")
        self.P = P
        # TODO: convert "P" to global as well
        self.people = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cells = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cell_size = min(SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE)
        self.create_people()
        self.create_gui()

    def create_people(self):
        # create a list of doubt levels with different proportions. multiplying the values controls the distribution.
        # doubt_levels = ["S1"] * 70 + ["S2"] * 10 + ["S3"] * 10 + ["S4"] * 10
        doubt_levels = [0] * 70 + [1] * 10 + [2] * 10 + [3] * 10
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                if random.random() < self.P:
                    doubt_level = random.choice(doubt_levels)
                    # set the default color of the person to NEUTRAL dark blue.
                    # NEUTRAL (blue) means a person is currently not a rumor spreader (didnt believe or haven't heared yet)
                    # create a Person object and add it to the people list in the corresponding cell
                    self.people[row][column] = Person(doubt=doubt_level, location=(row, column), color=NEUTRAL)

    def create_gui(self):
        # creates the GUI for the simulation
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.people[row][col] is not None:
                # if there is a person in the cell, color according to his doubt level
                    cell = tk.Canvas(self.master, width=self.cell_size, height=self.cell_size,
                                     bg=self.people[row][col].color)
                else:
                # If there isn't, color cell with grey
                    cell = tk.Canvas(self.master, width=self.cell_size, height=self.cell_size, bg='light grey')
                cell.grid(row=row, column=col, padx=1, pady=1)
                self.cells[row][col] = cell

    def run_round(self):
        new_spreaders = []

        current_spreaders = [
            self.people[row][col]
            for row in range(GRID_SIZE)
            for col in range(GRID_SIZE)
            if self.people[row][col] is not None and self.people[row][col].color == SPREADER
        ]

        new_spreaders = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                person = self.people[row][col]
                if person is None:
                    continue
                if person.rumor_cooldown > 0:
                    person.rumor_cooldown -= 1
                if person.color == NEUTRAL and person.rumor_cooldown == 0:
                    neighbors = [
                        self.people[i][j]
                        for i in range(max(0, row - 1), min(GRID_SIZE, row + 2))
                        for j in range(max(0, col - 1), min(GRID_SIZE, col + 2))
                        if (i != row or j != col) and self.people[i][j] is not None
                    ]
                    neighbor_spreaders = [neighbor for neighbor in neighbors if neighbor.color == SPREADER]
                    if len(neighbor_spreaders) > 0 and believes_rumor(person, len(neighbor_spreaders)):
                        new_spreaders.append(person)

        for person in new_spreaders:
            person.color = SPREADER

        for person in current_spreaders:
            person.color = NEUTRAL
            person.rumor_cooldown = COOLDOWN

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                person = self.people[row][col]
                if person is None:
                    continue
                self.cells[row][col].configure(bg=person.color)

    def update_grid_colors(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                person = self.people[row][col]
                if person:
                # if there's a Person in that cell
                    self.cells[row][col].configure(bg=person.color)

    def main_loop(self):
        # initialize the rumor starter for the first round
        self.rumor_starter = random.choice([person for row in self.people for person in row if person is not None])
        self.rumor_starter.color = SPREADER
        row_1, col_1 = self.rumor_starter.location
        self.cells[row_1][col_1].configure(bg=self.rumor_starter.color)

        # for i in range(10):
        #     self.master.after(1000, self.run_round)
        #     self.master.after(1000, self.update_grid_colors)

        # add a "Next Round" button
        next_round_button = tk.Button(self.master, text="Next Round", command=self.run_round)
        next_round_button.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE)


root = tk.Tk()
app = App(root)
app.main_loop()
root.mainloop()
