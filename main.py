import tkinter as tk
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
GRID_SIZE = 5

class Person:
    def __init__(self, doubt, l, location, color="white"):
        self.doubt_level = doubt
        self.location = location
        self.rumor_cooldown = l
        self.is_triggered = False
        self.color = color


class App:
    def __init__(self, master, P=0.3):
        self.master = master
        master.title("Person Interaction GUI")
        self.P = P
        self.people = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cells = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cell_size = min(SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE)
        self.current_rumors = []
        self.create_people()
        self.create_gui()

    def create_people(self):
        # multiplying the values help up control the distribution of doubt levels.
        doubt_levels = ["S1"] * 70 + ["S2"] * 10 + ["S3"] * 10 + ["S4"] * 10
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                if random.random() < self.P:
                    doubt_level = random.choice(doubt_levels)
                    color = "green"
                    # if (doubt_level == "S1"):
                    #     color = "red"
                    self.people[row][column] = Person(doubt=doubt_level, l=0, location=(row, column), color=color)

    def create_gui(self):
        # create the grid of cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.people[row][col] is not None:
                    cell = tk.Canvas(self.master, width=self.cell_size, height=self.cell_size,
                                     bg=self.people[row][col].color)
                else:
                    cell = tk.Canvas(self.master, width=self.cell_size, height=self.cell_size, bg='light grey')
                cell.grid(row=row, column=col, padx=1, pady=1)
                self.cells[row][col] = cell

        # initialize the rumor starter for the first round
        self.rumor_starter = random.choice([person for row in self.people for person in row if person is not None])
        self.current_rumors.append(self.rumor_starter)
        self.rumor_starter.color = "yellow"
        row_1, col_1 = self.rumor_starter.location
        self.cells[row_1][col_1].configure(bg=self.rumor_starter.color)
        self.master.after(1000, self.run_round)
        # # add a "Next Round" button
        # next_round_button = tk.Button(self.master, text="Next Round", command=self.run_round)
        # next_round_button.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE)

    def run_round(self):
        """
        # select the rumor starter for this round
        self.rumor_starter = random.choice([person for row in self.people for person in row if person is not None])
        """
        # set the rumor starter's color to red
        # self.rumor_starter.color = "red"
        row, col = self.rumor_starter.location
        # self.cells[row][col].configure(bg=self.rumor_starter.color)
        new_rumors = []
        for rumor_spreader in self.current_rumors:
            row, col = rumor_spreader.location
            # spread the rumor to surrounding cells
            for i in range(max(0, row - 1), min(GRID_SIZE, row + 2)):
                for j in range(max(0, col - 1), min(GRID_SIZE, col + 2)):
                    if i != row or j != col:
                        if self.people[i][j]:
                            self.people[i][j].color = self.rumor_starter.color
                            self.cells[i][j].configure(bg=self.people[i][j].color)
                            new_rumors.append(self.people[i][j])

        # TODO: remove current spreaders from self.current_rumors and add the new ones
        for old_rumor in self.current_rumors:
            old_rumor.color = "blue"
        self.current_rumors = new_rumors
        # TODO: add support for complicated rumor behaviour: doubt level, rumor cooldown, rumor level, etc.

        # # update the rumor cooldown for all people
        # for row in range(GRID_SIZE):
        #     for col in range(GRID_SIZE):
        #         person = self.people[row][col]
        #         if person:
        #             if person.color == "red":
        #                 person.rumor_cooldown = 3
        #             elif person.rumor_cooldown > 0:
        #                 person.rumor_cooldown -= 1
        # self.master.after(1000)
        self.master.after(1000, self.run_round)

root = tk.Tk()
app = App(root)
root.mainloop()
