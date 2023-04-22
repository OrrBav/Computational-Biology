

class Person:
    # TODO: add color?
    def __int__(self, doubt, l, color = "white"):
        self.doubt_level = doubt
        # self.location = location
        self.rumor_cooldown = l
        self.is_triggered = False
        self.color = color


    def spread_rumor(self, matrix, row, col):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if 0 <= row + i < self.num_rows and 0 <= col + j < self.num_cols:
                    neighbor = self.persons[row + i][col + j]
                    neighbor.color = "green"
                    self.person_refs[(row + i, col + j)].config(bg=neighbor.color)


    def believes_rumor(person, rumor_count):
        current_doubt_level = person.doubt_level if rumor_count < 2 else max(0, person.doubt_level - 1)
        # S3 -> 2
        # [False] * 2 + [True] * 1 = [False, False, True]
        # S2 -> 1
        # [False] * 1 + [True] * 2 = [False, True, True]
        doubt_level_choices = [False] * current_doubt_level + [True] * (3 - current_doubt_level)
        return random.choice(doubt_level_choices)
