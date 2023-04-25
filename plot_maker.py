import matplotlib.pyplot as plt

def one_vs_three_startes():
    spreaders1 = [1, 5, 9, 16, 22, 27, 34, 41, 51, 63, 76, 91, 109, 134, 159]
    spreaders3 = [3, 13, 29, 51, 76, 105, 129, 162, 196, 235, 281, 333, 385, 452, 527]
    total_people = 1520
    generations = list(range(1, 16))

    spreaders1_percent = [(count / total_people)*100 for count in spreaders1]
    spreaders3_percent = [(count/total_people)*100 for count in spreaders3]

    plt.plot(generations, spreaders3_percent, label='3 starters')
    plt.plot(generations, spreaders1_percent, label='1 starter')

    plt.xlabel('Generation')
    plt.ylabel('People heard the rumor by Percentage')
    plt.title('Comparison of Rumor Spread 1 Starter vs. 3 Starters')
    plt.legend()
    # Add the percantge to the last point on each line
    plt.text(generations[-1], spreaders1_percent[-1], f'{spreaders1_percent[-1]:.2f}%', ha='left', va='center')
    plt.text(generations[-1], spreaders3_percent[-1], f'{spreaders3_percent[-1]:.2f}%', ha='left', va='center')
    plt.show()

def ignore_rumor_count():
    #1463
    spreaders = [1, 4, 8, 14, 26, 37, 45, 58, 68, 78, 91, 107, 119, 133, 144]
    # 1456
    spreaders_ignored = [1, 4, 9, 12, 16, 21, 25, 31, 41, 49, 61, 75, 82, 94, 113]
    total_people = 1520
    generations = list(range(1, 16))

    spreaders_percent = [(count / total_people) * 100 for count in spreaders]
    spreaders_ignored_percent = [(count / total_people) * 100 for count in spreaders_ignored]

    plt.plot(generations, spreaders_ignored_percent, color='red', label='Doubt level remains the same')
    plt.plot(generations, spreaders_percent, color='green',label='Doubt level can change')

    plt.xlabel('Generation')
    plt.ylabel('People heard the rumor by Percentage')
    plt.title("Rumor Spread when doubt level can decrease vs. when it can't")
    plt.legend()
    # Add the percantge to the last point on each line
    plt.text(generations[-1], spreaders_percent[-1], f'{spreaders_percent[-1]:.2f}%', ha='left', va='center')
    plt.text(generations[-1], spreaders_ignored_percent[-1], f'{spreaders_ignored_percent[-1]:.2f}%', ha='left', va='center')
    plt.show()


if __name__ == '__main__':
    # one_vs_three_startes()
    ignore_rumor_count()

