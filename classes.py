

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


    def received_rumor(person, rumor_count):

        if person.rumor_cooldown == 0:
            # so person can re-spread this rumor

            if rumor_count == 1:
                # if this person heard this rumor once, act normally
                if person.doubt_level == 'S1':
                    # forward rumor to all 8 neighbors

                if person.doubt_level == 'S2':
                    # forward rumor to all 8 neighbors with prob of 2/3

                if person.doubt_level == 'S3':
                    # forward rumor to all 8 neighbors with prob of 1/3


                if person.doubt_level == 'S4':
                    # don't forward the rumor


            if rumor_count > 1:
                # if this person heard this rumor more than once, doubt_level decreases
                if person.doubt_level == 'S1':
                    # forward rumor to all 8 neighbors

                if person.doubt_level == 'S2':
                    # forward rumor to all 8 neighbors

                if person.doubt_level == 'S3':
                    # forward rumor to all 8 neighbors with prob of 2/3

                if person.doubt_level == 'S4':
            # forward rumor to all 8 neighbors with prob of 1/3

        else:
    # so person.rumor_cooldown>0 and can't re-spread this rumor

