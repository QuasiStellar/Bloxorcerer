WIDTH = 15
HEIGHT = 10

width = WIDTH * 2 - 1
height = HEIGHT * 2 - 1


def neighbours_button(x, y):
    neighbours = []
    if (x + y) % 2:
        return neighbours
    if y >= 1:
        neighbours.append((x, y - 1))
    if y <= height - 2:
        neighbours.append((x, y + 1))
    if x >= 1:
        neighbours.append((x - 1, y))
    if x <= width - 2:
        neighbours.append((x + 1, y))
    return neighbours


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


def double_coordinates(switches):
    for switch in switches:
        switch['x'], switch['y'] = switch['x'] * 2, switch['y'] * 2
        for platform in switch['platforms']:
            platform['x'], platform['y'] = platform['x'] * 2, platform['y'] * 2
    return switches
