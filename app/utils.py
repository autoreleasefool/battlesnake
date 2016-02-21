import random


def direction_to_closest_food(head, available_moves, blocked_coords, data):
    available_nodes = []
    visited_nodes = []
    for direction in available_moves:
        available_nodes.append(get_adjacent_coord(head, direction))
    print(blocked_coords)

    while len(available_nodes) > 0:
        next_node = available_nodes.pop(0)
        visited_nodes.append(next_node)

        print('Next:', next_node)

        if next_node in data['food']:
            return next_node

        new_nodes = get_all_adjacent(next_node, data['width'], data['height'])
        for node in new_nodes:
            if node not in blocked_coords and node not in visited_nodes and node not in available_nodes:
                available_nodes.append(node)

    return None


def get_all_adjacent(coord, width, height):
    all = []
    if coord[0] + 1 < width and coord[1] + 1 < height:
        all.append([coord[0] + 1, coord[1] + 1])
    if coord[0] - 1 >= 0 and coord[1] + 1 < height:
        all.append([coord[0] - 1, coord[1] + 1])
    if coord[0] + 1 < width and coord[1] - 1 >= 0:
        all.append([coord[0] + 1, coord[1] - 1])
    if coord[0] - 1 >= 0 and coord[1] - 1 >= 0:
        all.append([coord[0] - 1, coord[1] - 1])
    return all


def get_adjacent_coord(coord, direction):
    if direction == 'north':
        return [coord[0], coord[1] - 1]
    elif direction == 'south':
        return [coord[0], coord[1] + 1]
    elif direction == 'east':
        return [coord[0] + 1, coord[1]]
    elif direction == 'west':
        return [coord[0] - 1, coord[1]]
    else:
        return coord


def get_direction_to_coord(start, target):
    if start[0] == target[0]:
        if start[1] == target[1] - 1:
            return 'south'
        elif start[1] == target[1] + 1:
            return 'north'
    elif start[1] == target[1]:
        if start[0] == target[0] - 1:
            return 'east'
        elif start[0] == target[0] + 1:
            return 'west'

    return None


def pick_random_direction(available_moves):
    # Pick a random direction for now
    if len(available_moves) == 0:
        # Can't go anywhere, fuck it
        next_move = 'north'
    else:
        next_move = available_moves[random.randrange(0, len(available_moves))]

    return next_move