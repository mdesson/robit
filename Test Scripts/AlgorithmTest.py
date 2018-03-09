import csv


def distance_options(input_list):
    dist_results = []  # store each set of 9's direction and shortest distance
    for i in range(0, len(input_list)):
        direction = (i+4)*5  # gets center of current selection, in degrees
        smallest = input_list[i]
        try:
            for j in range(i, i+10):
                if input_list[j] < input_list[j]:
                    smallest = input_list[j]
            dist_results.append([int(smallest), direction])
        except IndexError:
            break
    return dist_results


def select_direction(input_list):
    direction = input_list[0]
    for i in input_list:
        if i[0] >= direction[0]:
            direction = i
    return direction[1]


data = []
results = []

with open("SampleData.csv", "r") as f:
    reader = csv.reader(f, dialect='excel')
    for row in reader:
        data.append(row)

for k in data:
    results.append(distance_options(k))

for i in results:
    print(select_direction(i))
