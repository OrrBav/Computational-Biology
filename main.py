import tkinter as tk
import random

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 100
GRID_SIZE = 50
COOLDOWN = 2
PROB = 0.6
NEUTRAL = "dark blue"
SPREADER = "dark red"
POPULATION = 0
GENERATION = 1
HEARD_RUMOR = set()
DOUBT_TRACKER = {'s1': 0, 's2': 0, 's3': 0, 's4': 0, 's1*': 0, 's2*': 0, 's3*': 0, 's4*': 0}
# TODO: remove s*



class Person:
    def __init__(self, doubt, location, color="white"):
        self.doubt_level = doubt
        self.location = location
        self.rumor_cooldown = 0
        self.color = color

class App:
    def __init__(self, master):
        self.master = master
        master.title("Person Interaction GUI")
        self.P = PROB
        self.people = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cells = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cell_size = min(SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE)
        self.create_people()
        self.create_gui()
        # create a label for displaying statistics
        self.stats_label = tk.Label(self.master)
        # stats_label.grid(row=3, column=0, padx=10, pady=10)
        self.stats_label.grid(row=GRID_SIZE + 2, column=0, columnspan=GRID_SIZE, pady=10)

    def create_people(self):
        # create a list of doubt levels with different proportions. multiplying the values controls the distribution.
        # doubt levels: 0="S1", 1="S2", 2="S3", 3="S4"]
        doubt_levels = [0] * 70 + [1] * 10 + [2] * 10 + [3] * 10
        global POPULATION, DOUBT_TRACKER
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                if random.random() < self.P:
                    doubt_level = random.choice(doubt_levels)
                    # initiate new Person with NEUTRAL color and randomly chosen doubt level
                    self.people[row][column] = Person(doubt=doubt_level, location=(row, column), color=NEUTRAL)
                    # NEUTRAL (blue) means a person is currently not a spreader - didn't believe or haven't heard yet
                    POPULATION += 1
                    if doubt_level == 0:
                        DOUBT_TRACKER['s1'] += 1
                    elif doubt_level == 1:
                        DOUBT_TRACKER['s2'] += 1
                    elif doubt_level == 2:
                        DOUBT_TRACKER['s3'] += 1
                    elif doubt_level == 3:
                        DOUBT_TRACKER['s4'] += 1
                    self.people[row][column] = Person(doubt=doubt_level, location=(row, column), color=NEUTRAL)
                    # NEUTRAL (blue) means a person is currently not a rumor spreade- didn't believe or haven't heared yet

    def believes_rumor(self, person, rumor_count):
        """
        the function determines whether a person believes a rumor or not,
        based on the person's doubt level and the number of times he heard this rumor before.
        """

        # determines current doubt level,
        # if rumor_count < 2 so the doubt level remains the same, else the doubt level will decreas by 1
        current_doubt_level = person.doubt_level if rumor_count < 2 else max(0, person.doubt_level - 1)

        doubt_level_choices = [False] * current_doubt_level + [True] * (3 - current_doubt_level)
        # examples:
        # if doubt level is 3 (=S4) we get 0/3 chance to believe
        # [False] * 3 + [True] * 0 = [False, False, False]
        # if doubt level is 2 (=S3) we get 1/3 chance to believe
        # [False] * 2 + [True] * 1 = [False, False, True]
        # if doubt level is 1 (=S2) we get 2/3 chance to believe
        # [False] * 1 + [True] * 2 = [False, True, True]
        # if doubt level is 0 (=S1) we get 3/3 chance to believe
        # [False] * 1 + [True] * 2 = [True, True, True]
        return random.choice(doubt_level_choices)

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
        global HEARD_RUMOR, GENERATION
        GENERATION +=1
        # a list of all the people in the grid that are currently spreaders of the rumor
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
                # the person is a potential spreader, so extract all their neighbors
                    neighbors = [
                        self.people[i][j]
                        for i in range(max(0, row - 1), min(GRID_SIZE, row + 2))
                        for j in range(max(0, col - 1), min(GRID_SIZE, col + 2))
                        if (i != row or j != col) and self.people[i][j] is not None
                    ]
                    # extract only the spreaders from their list of neighbors
                    neighbor_spreaders = [neighbor for neighbor in neighbors if neighbor.color == SPREADER]

                    if len(neighbor_spreaders) > 0 and self.believes_rumor(person, len(neighbor_spreaders)):
                    # If the person has spreader neighbors and he believes the rumor, add person to next round spreaders
                        new_spreaders.append(person)
                        # add current person to set() of unique people that heard the rumor so far (for statistics)
                        HEARD_RUMOR.add(person.location)

            # init count for doubt levels of active spreaders (for statistics)
            active_s1, active_s2, active_s3, active_s4 = [0 for _ in range(4)]

        # Set the color of all new spreaders to SPREADER red
        for person in new_spreaders:
            person.color = SPREADER
            # update doubt levels count of active spreaders (for statistics)
            if person.doubt_level == 0:
                active_s1 += 1
            elif person.doubt_level == 1:
                active_s2 += 1
            elif person.doubt_level == 2:
                active_s3 += 1
            elif person.doubt_level == 3:
                active_s4 += 1

        # color current spreaders back to NEUTRAL and reset their rumor cooldown
        for person in current_spreaders:
            person.color = NEUTRAL
            person.rumor_cooldown = COOLDOWN


        # Update the GUI to reflect the new colors of all cells
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                person = self.people[row][col]
                if person is None:
                    continue
                self.cells[row][col].configure(bg=person.color)

        # stats for second round and after
        self.stats_label.config(
            text=f"Generation: {GENERATION}\n"
                 f"Total population: {POPULATION}\n"
                 f"Doubt Level distribution: S1:{DOUBT_TRACKER['s1']}, S2:{DOUBT_TRACKER['s2']},"
                 f" S3:{DOUBT_TRACKER['s3']}, S4:{DOUBT_TRACKER['s4']}\n"
                 f"Out of {len(HEARD_RUMOR)} people who heard the rumor so far, {len(new_spreaders)} are active spreaders\n "
                 f"Doubt Level distribution of active spreaders:"
                 f" S1:{active_s1}, S2:{active_s2}, S3:{active_s3}, S4:{active_s4}"
        )

    # TODO: delete this??
    def update_grid_colors(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                person = self.people[row][col]
                if person:
                # if there's a Person in that cell
                    self.cells[row][col].configure(bg=person.color)

    def main_loop(self):
        global HEARD_RUMOR
        # initialize the rumor starter for the first round
        self.rumor_starter = random.choice([person for row in self.people for person in row if person is not None])
        self.rumor_starter.color = SPREADER
        row_1, col_1 = self.rumor_starter.location
        self.cells[row_1][col_1].configure(bg=self.rumor_starter.color)
        HEARD_RUMOR.add((row_1, col_1))

        # self.rumor_starter2 = random.choice([person for row in self.people for person in row if person is not None])
        # self.rumor_starter2.color = SPREADER
        # row_2, col_2 = self.rumor_starter2.location
        # self.cells[row_2][col_2].configure(bg=self.rumor_starter2.color)
        # HEARD_RUMOR.add((row_2, col_2))
        #
        # self.rumor_starter3 = random.choice([person for row in self.people for person in row if person is not None])
        # self.rumor_starter3.color = SPREADER
        # row_3, col_3 = self.rumor_starter3.location
        # self.cells[row_3][col_3].configure(bg=self.rumor_starter3.color)
        # HEARD_RUMOR.add((row_3, col_3))

        # get doubt level of rumor_starter (for statistics)
        starter_s1, starter_s2, starter_s3, starter_s4 = [0 for _ in range(4)]
        if self.rumor_starter.doubt_level == 0:
            starter_s1 += 1
        elif self.rumor_starter.doubt_level == 1:
            starter_s2 += 1
        elif self.rumor_starter.doubt_level == 2:
            starter_s3 += 1
        elif self.rumor_starter.doubt_level == 3:
            starter_s4 += 1
        #
        # if self.rumor_starter2.doubt_level == 0:
        #     starter_s1 += 1
        # elif self.rumor_starter2.doubt_level == 1:
        #     starter_s2 += 1
        # elif self.rumor_starter2.doubt_level == 2:
        #     starter_s3 += 1
        # elif self.rumor_starter2.doubt_level == 3:
        #     starter_s4 += 1
        #
        # if self.rumor_starter3.doubt_level == 0:
        #     starter_s1 += 1
        # elif self.rumor_starter3.doubt_level == 1:
        #     starter_s2 += 1
        # elif self.rumor_starter3.doubt_level == 2:
        #     starter_s3 += 1
        # elif self.rumor_starter3.doubt_level == 3:
        #     starter_s4 += 1

        # stats for first round only
        # update the statistics label with data from variables
        self.stats_label.config(
            text=f"Generation: {GENERATION}\n"
                 f"Total population: {POPULATION}\n"
                 f"Doubt Level distribution: S1:{DOUBT_TRACKER['s1']}, S2:{DOUBT_TRACKER['s2']},"
                 f" S3:{DOUBT_TRACKER['s3']}, S4:{DOUBT_TRACKER['s4']}\n"
                 f"Out of {len(HEARD_RUMOR)} people who heard the rumor so far, 1 are active spreaders\n "
                 f"Doubt Level distribution of active spreaders:"
                 f" S1:{starter_s1}, S2:{starter_s2}, S3:{starter_s3}, S4:{starter_s4}"
        )

        # for i in range(10):
        #     self.master.after(1000, self.run_round)
        #     self.master.after(1000, self.update_grid_colors)

        # add the "Next Round" button
        next_round_button = tk.Button(self.master, text="Next Generation", command=self.run_round)
        next_round_button.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE)



root = tk.Tk()
app = App(root)
app.main_loop()
root.mainloop()
