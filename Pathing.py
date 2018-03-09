import easygopigo3 as easy
import time
from sys import exit

robot = easy.EasyGoPiGo3()
s = robot.init_servo()
ds = robot.init_distance_sensor()

# Numbers need to be recalculated when stopping_distance is changed so robot can fit through area in front of it
# Robot is ~15.31cm, requiring a 45 degree width to fit through an area 20cm in front of it
angle = [x*5 for x in range(1, 37)]  # 0 to 180 in increments of 5 degrees
stopping_distance = 20


def read_distance():  # Compensates for faulty sensor readings at >200cm distances causing tiny readings
    a = ds.read()
    b = ds.read()
    if a >= b:
        return a
    else:
        return b


def look_around():
    result = []
    s.rotate_servo(0)
    time.sleep(2)
    result.append(read_distance())

    for i in list(angle):
        s.rotate_servo(i)
        time.sleep(0.1)
        result.append(read_distance())
    s.rotate_servo(84)
    return result


def distance_options(input_list):
    dist_results = []  # store each set of 9's direction and shortest distance
    for i in range(0, len(input_list)):
        direction = (i+4)*5  # gets center of current selection, in degrees
        smallest = input_list[i]
        try:
            for j in range(i, i+10):
                if input_list[j] < input_list[j]:
                    smallest = input_list[j]
            dist_results.append([smallest, direction])
        except IndexError:
            break
    return dist_results


def select_direction(input_list):
    direction = input_list[0]
    for i in input_list:
        if i[0] >= direction[0]:
            direction = i
    return direction


def pathfind():
    options = distance_options(look_around())
    turn_direction = select_direction(options)

    if turn_direction[0] > stopping_distance:
        robot.turn_degrees(90-turn_direction[1])
        robot.drive_cm(turn_direction[0])
        explore()
    elif turn_direction <= stopping_distance:
        robot.turn_degrees(180)
        explore()
    else:
        explore()


def explore():
    robot.forward()
    while True:
        try:
            if read_distance() <= stopping_distance:
                robot.stop()
                pathfind()

        except KeyboardInterrupt:
            robot.stop()
            s.rotate_servo(84)
            exit()


if __name__ == "__main__":
    explore()
