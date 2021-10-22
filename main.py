import math
import random
import tkinter
import maps

WIDTH = 15
HEIGHT = 10
MAP = maps.MAPS[0]
ENTRANCE = (3, 3)
SWITCHES = {}

width = WIDTH * 2 - 1
height = HEIGHT * 2 - 1
level_entrance = tuple(map(lambda a: a * 2, ENTRANCE))
fastest = math.inf


def neighbours_cube(x, y):
    neighbours = []
    if (x + y) % 2:
        return neighbours
    if y >= 2:
        neighbours.append((x, y - 2))
    if y <= height - 3:
        neighbours.append((x, y + 2))
    if x >= 2:
        neighbours.append((x - 2, y))
    if x <= width - 3:
        neighbours.append((x + 2, y))
    return neighbours


def neighbours_block(x, y):
    neighbours = []
    if (x + y) % 2:
        if x % 2:  # lying horizontal
            if y >= 2:
                neighbours.append((x, y - 2))
            if y <= height - 3:
                neighbours.append((x, y + 2))
            if x >= 3:
                neighbours.append((x - 3, y))
            if x <= width - 4:
                neighbours.append((x + 3, y))
        else:  # lying vertical
            if y >= 3:
                neighbours.append((x, y - 3))
            if y <= height - 4:
                neighbours.append((x, y + 3))
            if x >= 2:
                neighbours.append((x - 2, y))
            if x <= width - 3:
                neighbours.append((x + 2, y))
    else:  # standing
        if y >= 3:
            neighbours.append((x, y - 3))
        if y <= height - 4:
            neighbours.append((x, y + 3))
        if x >= 3:
            neighbours.append((x - 3, y))
        if x <= width - 4:
            neighbours.append((x + 3, y))
    return neighbours


def inbetween(x1, y1, x2, y2):
    return (x1 + x2) // 2, (y1 + y2) // 2


def generate_graph():
    level_map_frame1 = {}
    _exit = (-1, -1)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if MAP[i][j] != ' ':
                level_map_frame1[(i * 2, j * 2)] = []
                if MAP[i][j] == 'e':
                    _exit = (i * 2, j * 2)
    level_map_frame2 = level_map_frame1.copy()
    for key in level_map_frame2:
        for neighbour in neighbours_cube(*key):
            if neighbour in level_map_frame2:
                level_map_frame1[inbetween(*key, *neighbour)] = []
    level_map_frame2 = level_map_frame1.copy()
    for key in level_map_frame2:
        for neighbour in neighbours_block(*key):
            if neighbour in level_map_frame2 and neighbour not in level_map_frame1[key]:
                level_map_frame1[key].append(neighbour)
    return level_map_frame1, _exit


def draw_graph(_map):
    for dot in _map:
        canvas.create_oval(dot[1] * 20 - 5 + 20,
                           dot[0] * 20 - 5 + 20,
                           dot[1] * 20 + 5 + 20,
                           dot[0] * 20 + 5 + 20,
                           fill='blue' if (dot[1] + dot[0]) % 2 else 'red',
                           outline='blue' if (dot[1] + dot[0]) % 2 else 'red')
        for neighbour in _map[dot]:
            canvas.create_line(dot[1] * 20 + 20,
                               dot[0] * 20 + 20,
                               *inbetween(dot[1] * 20 + 35,
                                          dot[0] * 20 + 35,
                                          neighbour[1] * 20 + 35,
                                          neighbour[0] * 20 + 35),
                               neighbour[1] * 20 + 20,
                               neighbour[0] * 20 + 20,
                               smooth=1,
                               fill='blue' if abs(dot[1] + dot[0] - neighbour[1] - neighbour[0]) == 2 else 'red')


class Condition:
    def __init__(self, pos_x, pos_y, turn, route, done):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.turn = turn
        self.route = route
        self.done = done
        if (pos_x, pos_y) == level_exit:
            self.done = True
        if turn > fastest:
            pass
        else:
            self.generate_new()

    def generate_new(self):
        for _neighbour in neighbours_block(self.pos_x, self.pos_y):
            if _neighbour not in level_map:
                continue
            condition_hash = hash(_neighbour)
            if condition_hash in condition_set and condition_set[condition_hash] >= self.turn or \
                    condition_hash not in condition_set:
                condition_set[condition_hash] = self.turn
                conditions.append(Condition(*_neighbour,
                                            self.turn + 1,
                                            self.route + [_neighbour],
                                            False))


root = tkinter.Tk()
canvas = tkinter.Canvas(root)
canvas.config(width=600, height=400)
canvas.pack()

level_map, level_exit = generate_graph()
draw_graph(level_map)

conditions = []
condition_set = {}
conditions.append(Condition(*level_entrance, 0, [], False))
solutions = []
for condition in conditions:
    if condition.done and condition.turn < fastest:
        fastest = condition.turn
        solutions = [condition]
    elif condition.done and condition.turn == fastest:
        solutions.append(condition)
print("Checked",
      len(conditions),
      "possible condition..." if len(conditions) == 1 else "possible conditions...")
print("Found",
      len(solutions),
      "solution" if len(solutions) == 1 else "solutions",
      "that take",
      solutions[0].turn,
      "turns.")
# for solution in solutions:
#     print(solution.route)
for solution in solutions:
    previous_step = level_entrance
    color = "#"+("%06x" % random.randint(0, 16777215))
    for step in solution.route:
        canvas.create_line(previous_step[1] * 20 + 20,
                           previous_step[0] * 20 + 20,
                           previous_step[1] * 10 + step[1] * 10 + 20 + random.randint(-10, 10),
                           previous_step[0] * 10 + step[0] * 10 + 20 + random.randint(-10, 10),
                           step[1] * 20 + 20,
                           step[0] * 20 + 20,
                           smooth=1,
                           fill=color,
                           width=3)
        previous_step = step

tkinter.mainloop()
