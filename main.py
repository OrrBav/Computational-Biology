import tkinter as tk
import random

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
GRID_SIZE = 10
COOLDOWN = 2
NEUTRAL = "dark blue"
SPREADER = "dark red"

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
        self.current_spreaders = []
        self.people_in_cooldown = []
        self.create_people()
        self.create_gui()

    def create_people(self):
        # create a list of doubt levels with different proportions. multiplying the values controls the distribution.
        doubt_levels = ["S1"] * 70 + ["S2"] * 10 + ["S3"] * 10 + ["S4"] * 10
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
            True if self.people[i][j].color == SPREADER else False
            for i in range(GRID_SIZE)
            for j in range(GRID_SIZE)
        ]

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                person = self.people[row][col]
                if person.rumor_cooldown > 0:
                    person.rumor_cooldown -= 1
                if person.color == NEUTRAL and person.rumor_cooldown == 0:
                    neighbors = [
                        self.people[i][j]
                        for i in range(max(0, row - 1), min(GRID_SIZE, row + 2))
                        for j in range(max(0, col - 1), min(GRID_SIZE, col + 2))
                        if i != row or j != col
                    ]
                    neighbor_spreaders = [neighbor for neighbor in neighbors if neighbor.color == SPREADER]
                    if len(neighbor_spreaders) == 1:
                        person.color = SPREADER

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                person = self.people[row][col]
                if current_spreaders[row * GRID_SIZE + col]:
                    person.color = NEUTRAL
                    person.rumor_cooldown = COOLDOWN
                    """
                    GRID_SIZE=3
                    [[0][1][2]]
                    [[3][4][5]]
                    [[6][7][8]]
                    
                    [[0][1][2][3][4][5][6][7][8]]
                    """

            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    person = self.people[row][col]
                    self.cells[row][col].configure(bg=person.color)

            #
        # for rumor_spreader in current_spreaders:
        #     row, col = rumor_spreader.location
        #     # check the 8 surrounding cells
        #     for i in range(max(0, row - 1), min(GRID_SIZE, row + 2)):
        #         for j in range(max(0, col - 1), min(GRID_SIZE, col + 2)):
        #             if i != row or j != col:
        #                 # TODO: combine ifs
        #             # if current cell being examined is not the spreader cell itself
        #                 if self.people[i][j]:
        #                 # if there's a person in that cell it's a neighbor
        #                     current_neighbor = self.people[i][j]
        #                     if current_neighbor.rumor_cooldown == 0:
        #                     # neighbor can spread the rumor
        #
        #                     # TODO: currently color always changes,but should be changed based on each DL (believes/not)!
        #                     # check_doubt_level(current_neighbor)
        #
        #                         current_neighbor.color = SPREADER
        #                         self.cells[i][j].configure(bg=current_neighbor.color)
        #                         # add that neighbor to the new spreadres list
        #                         new_spreaders.append(current_neighbor)

                    # TODO fix cooldown problem
                    #  1. the starter somehow returns red for no reason after dew rounds + random jumps in infections
                    #  2. cooldown -1 from the start, but should be only from second round
                    #  3.

            #
            # # now current spreader goes back to NUETRAL blue and activate cooldown
            # self.people[row][col].color = NEUTRAL
            # self.cells[row][col].configure(bg=self.people[row][col].color)
            # self.people[row][col].rumor_cooldown = COOLDOWN
            #
            # # a list of the people that are in cd after spreading the rumor
            # self.people_in_cooldown.append(self.people[row][col])

        # # now we finished dealing will all of this round spreaders (finished one generation):
        # # update current spreaders list for next round
        # self.current_spreaders = new_spreaders
        # # reduce rumor_cooldown by 1 for each person with cd>0 right now
        # for person_in_cd in self.people_in_cooldown:
        #     if person_in_cd.rumor_cooldown > 0:
        #         # only decreas person's cd if it's > 0
        #         person_in_cd.rumor_cooldown -= 1
        #     if person_in_cd.rumor_cooldown == 0:
        #     # if cd=0 so person is no longer in cooldown
        #         self.people_in_cooldown.remove(person_in_cd)


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
        self.current_spreaders.append(self.rumor_starter)
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
