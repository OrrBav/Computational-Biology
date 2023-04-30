import matplotlib.pyplot as plt

def one_vs_three_startes():
    spreaders1 = [1, 5, 10, 19, 29, 43, 51, 61, 74, 92, 107, 125, 142, 159, 178, 198, 226, 251, 281, 312, 350,
                  378, 405, 447, 487, 521, 553, 595, 625, 667, 708, 747, 795, 844, 895, 949, 1002, 1058, 1102,
                  1132, 1160, 1195, 1224, 1247, 1274, 1298, 1326, 1346, 1362, 1386]
    spreaders3 = [3, 13, 31, 56, 83, 110, 145, 193, 252, 322, 402, 482, 564, 628, 699, 778, 844, 897, 944, 982,
                  1034, 1088, 1127, 1172, 1218, 1255, 1283, 1305, 1326, 1345, 1356, 1372, 1384, 1398, 1408, 1416,
                  1429, 1438, 1440, 1441, 1442, 1442, 1444, 1444, 1446, 1446, 1447, 1447, 1447, 1448]
    total_people = 1500
    generations = list(range(1, 51))

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
    spreaders = [1 ,4, 10, 19, 28, 38, 49, 66, 84, 100, 121, 145, 174, 206, 235, 265, 299, 335, 366, 404, 441, 485, 517,
                555, 607, 654, 702, 752, 788, 823, 869, 914, 951, 985, 1018, 1050, 1087, 1120, 1147, 1177,
                1211, 1244, 1278, 1308, 1335,1353, 1369, 1381, 1391, 1395]
    spreaders_ignored = [1, 7, 15, 26, 42, 55, 73, 92, 109, 128, 152, 177, 199, 220, 245, 274, 305, 321, 338, 354, 373, 393,
                         415, 444, 478, 509, 538, 571, 605, 648, 686, 726, 765, 805, 830, 852, 874, 896, 930, 963, 999, 1029,
                         1059, 1090, 1126, 1156, 1194, 1220, 1241, 1257]
    total_people = 1520
    generations = list(range(1, 51))

    spreaders_percent = [(count / total_people) * 100 for count in spreaders]
    spreaders_ignored_percent = [(count / total_people) * 100 for count in spreaders_ignored]

    plt.plot(generations, spreaders_percent, color='green',label='Doubt level can decrease')
    plt.plot(generations, spreaders_ignored_percent, color='red', label='Doubt level remains the same')

    plt.xlabel('Generation')
    plt.ylabel('People heard the rumor by Percentage')
    plt.title("Rumor Spread when doubt level can decrease vs. when it can't")
    plt.legend()
    # Add the percantge to the last point on each line
    plt.text(generations[-1], spreaders_percent[-1], f'{spreaders_percent[-1]:.2f}%', ha='left', va='center')
    plt.text(generations[-1], spreaders_ignored_percent[-1], f'{spreaders_ignored_percent[-1]:.2f}%', ha='left', va='center')
    plt.show()


if __name__ == '__main__':
    one_vs_three_startes()
    ignore_rumor_count()

