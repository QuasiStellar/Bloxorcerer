import math
import random
import tkinter
import json
import sys
from collections import defaultdict

import utils
from button import Button
from entrance import Entrance
from level import Level
from platform import Platform
from switch import Switch

TILES = {'exit': 'e', 'red_floor': 'f'}
SWITCH_TYPES = {'h': 'cross', 's': 'circle'}
PLATFORM_TYPES = ('l', 'r')

LEVEL = 5


class Condition:
    def __init__(self, pos_x, pos_y, _holes, _holes_plus, turn, route, done):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.holes = _holes
        self.holes_plus = _holes_plus
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
        for _neighbour in utils.neighbours_block(self.pos_x, self.pos_y):
            if _neighbour not in level_map or _neighbour in self.holes_plus:
                continue
            new_holes = self.holes.copy()
            new_holes_plus = self.holes_plus.copy()
            if _neighbour in switch_map:
                new_holes_plus = set()
                for platform in switch_map[_neighbour]:
                    if platform.mode == 'on' and (platform.x, platform.y) in new_holes:
                        new_holes.remove((platform.x, platform.y))
                    elif platform.mode == 'off' and (platform.x, platform.y) not in new_holes:
                        new_holes.add((platform.x, platform.y))
                    elif platform.mode == 'onoff':
                        if (platform.x, platform.y) in new_holes:
                            new_holes.remove((platform.x, platform.y))
                        else:
                            new_holes.add((platform.x, platform.y))
                for hole in new_holes:
                    new_holes_plus.add(hole)
                    for neighbour in utils.neighbours_button(*hole):
                        if neighbour in level_map:
                            new_holes_plus.add(neighbour)
            condition_hash = hash((_neighbour, tuple(new_holes)))
            if condition_hash in condition_set and condition_set[condition_hash] >= self.turn or \
                    condition_hash not in condition_set:
                condition_set[condition_hash] = self.turn
                conditions.append(Condition(*_neighbour,
                                            new_holes,
                                            new_holes_plus,
                                            self.turn + 1,
                                            self.route + [_neighbour],
                                            False))


def generate_graph():
    level_map_frame1 = {}
    _exit = (-1, -1)
    for i in range(utils.WIDTH):
        for j in range(utils.HEIGHT):
            if level.map[j][i] != ' ':
                level_map_frame1[(i * 2, j * 2)] = []
                if level.map[j][i] == TILES['exit']:
                    _exit = (i * 2, j * 2)
    level_map_frame2 = level_map_frame1.copy()
    for key in level_map_frame2:
        for neighbour in utils.neighbours_cube(*key):
            if neighbour in level_map_frame2:
                level_map_frame1[utils.inbetween(*key, *neighbour)] = []
    for i in range(utils.WIDTH):
        for j in range(utils.HEIGHT):
            if level.map[j][i] == TILES['red_floor']:
                level_map_frame1.pop((i * 2, j * 2))
    _switch_map = defaultdict(list)
    for switch in level.switches:
        if switch.button.type == 'cross':
            for platform in switch.platforms:
                _switch_map[(switch.button.x, switch.button.y)].append(platform)
        elif switch.button.type == 'circle':
            for platform in switch.platforms:
                _switch_map[(switch.button.x, switch.button.y)].append(platform)
                for neighbour in utils.neighbours_button(switch.button.x, switch.button.y):
                    if neighbour in level_map_frame1:
                        _switch_map[neighbour].append(platform)
    for hole in holes:
        holes_plus.add(hole)
        for neighbour in utils.neighbours_button(*hole):
            if neighbour in level_map_frame1:
                holes_plus.add(neighbour)
    level_map_frame2 = level_map_frame1.copy()
    for key in level_map_frame2:
        for neighbour in utils.neighbours_block(*key):
            if neighbour in level_map_frame2 and neighbour not in level_map_frame1[key]:
                level_map_frame1[key].append(neighbour)
    return level_map_frame1, _exit, _switch_map


def draw_graph(_map):
    for dot in _map:
        canvas.create_oval(dot[0] * 20 - 5 + 20,
                           dot[1] * 20 - 5 + 20,
                           dot[0] * 20 + 5 + 20,
                           dot[1] * 20 + 5 + 20,
                           fill='blue' if (dot[1] + dot[0]) % 2 else 'red',
                           outline='blue' if (dot[1] + dot[0]) % 2 else 'red')
        for neighbour in _map[dot]:
            canvas.create_line(dot[0] * 20 + 20,
                               dot[1] * 20 + 20,
                               *utils.inbetween(dot[0] * 20 + 35,
                                                dot[1] * 20 + 35,
                                                neighbour[0] * 20 + 35,
                                                neighbour[1] * 20 + 35),
                               neighbour[0] * 20 + 20,
                               neighbour[1] * 20 + 20,
                               smooth=1,
                               fill='blue' if abs(dot[0] + dot[1] - neighbour[0] - neighbour[1]) == 2 else 'red')


def show_results():
    print("Checked",
          len(conditions),
          "possible condition..." if len(conditions) == 1 else "possible conditions...")
    if len(solutions):
        print("Found",
              len(solutions),
              "solution" if len(solutions) == 1 else "solutions",
              "that takes" if len(solutions) == 1 else "that take",
              solutions[0].turn,
              "turns.")
    for solution in solutions:
        print(solution.route)
    for solution in solutions:
        previous_step = (level.entrance.x, level.entrance.y)
        color = "#" + ("%06x" % random.randint(0, 16777215))
        for step in solution.route:
            canvas.create_line(previous_step[0] * 20 + 20,
                               previous_step[1] * 20 + 20,
                               previous_step[0] * 10 + step[0] * 10 + 20 + random.randint(-10, 10),
                               previous_step[1] * 10 + step[1] * 10 + 20 + random.randint(-10, 10),
                               step[0] * 20 + 20,
                               step[1] * 20 + 20,
                               smooth=1,
                               fill=color,
                               width=3)
            previous_step = step


if __name__ == "__main__":
    with open('maps.json') as map_file:
        maps = json.load(map_file)
        level = Level(maps['level' + str(LEVEL)]['map'],
                      Entrance(maps['level' + str(LEVEL)]['entrance']['x'] * 2,
                               maps['level' + str(LEVEL)]['entrance']['y'] * 2),
                      [Switch(Button(switch['button']['x'],
                                     switch['button']['y'],
                                     SWITCH_TYPES[maps['level' + str(LEVEL)]['map']
                                     [switch['button']['y'] // 2]
                                     [switch['button']['x'] // 2]
                                     ]),
                              [Platform(platform['x'], platform['y'], platform['mode'])
                               for platform in switch['platforms']])
                       for switch in utils.double_coordinates(maps['level' + str(LEVEL)]['switches'])])

    fastest = math.inf
    holes = set([(platform.x, platform.y) for switch in level.switches for platform in switch.platforms
                 if level.map[platform.y // 2][platform.x // 2] in PLATFORM_TYPES])
    holes_plus = set()

    sys.setrecursionlimit(3000)

    root = tkinter.Tk()
    canvas = tkinter.Canvas(root)
    canvas.config(width=600, height=400)
    canvas.pack()

    level_map, level_exit, switch_map = generate_graph()
    draw_graph(level_map)

    conditions = []
    condition_set = {}
    conditions.append(Condition(level.entrance.x, level.entrance.y, holes, holes_plus, 0, [], False))
    solutions = []
    for condition in conditions:
        if condition.done and condition.turn < fastest:
            fastest = condition.turn
            solutions = [condition]
        elif condition.done and condition.turn == fastest:
            solutions.append(condition)
    show_results()

    tkinter.mainloop()
