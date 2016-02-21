import bottle
import os
import utils


#########################
#                       #
#    Server endpoints   #
#                       #
#########################

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#96034d',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    taunt = get_starting_taunt()

    return {
        'taunt': taunt
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    move = get_next_move(data)
    taunt = get_moving_taunt()

    return {
        'move': move,
        'taunt': taunt
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    taunt = get_ending_taunt()

    return {
        'taunt': taunt
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))

####################
#                  #
#    Snake Info    #
#                  #
####################

def get_starting_taunt():
    return 'We are Sex Bob-Omb!'

def get_moving_taunt():
    # TODO: Tell on closest snake
    return 'Do you know this one girl with hair like this?'

def get_ending_taunt():
    return 'We were lucky to survive the last round, it\'s sudden death now'

#####################
#                   #
#    Snake Stuff    #
#                   #
#####################


TATTLESNAKE_ID = '97d0f99f-8bff-4d53-9e65-9f4d25cc6527'
POSSIBLE_MOVES = ['north', 'south', 'east', 'west']
SAFE_HEALTH_THRESHOLD = 50


def get_next_move(data):
    me = find_snake(data['snakes'])
    head = me['coords'][0]
    blocked_coords = get_blocked_coords(data)
    available_moves = get_available_moves(head, data['width'], data['height'], blocked_coords)

    # next_move = utils.pick_random_direction(available_moves)
    next_move = get_best_move(me, head, available_moves, blocked_coords, data)

    return next_move


def get_best_move(me, head, available_moves, blocked_coords, data):
    closest_food = utils.direction_to_closest_food(head, available_moves, blocked_coords, data)
    print(closest_food)

    return utils.pick_random_direction(available_moves)


def get_blocked_coords(data):
    blocked_coords = []

    for snake in data['snakes']:
        print ('Snake coords', snake['coords'])
        for coord in snake['coords']:
            blocked_coords.append(coord)

    return blocked_coords


def find_snake(snakes):
    for snake in snakes:
        if snake['id'] == TATTLESNAKE_ID:
            return snake


def get_available_moves(head, width, height, blocked_coords):
    # Resetting the moves
    available_moves = POSSIBLE_MOVES[:]

    # Absolutely can't go towards walls
    if head[0] == 0:
        if 'west' in available_moves:
            available_moves.remove('west')
    elif head[0] == width - 1:
        if 'east' in available_moves:
            available_moves.remove('east')
    if head[1] == 0:
        if 'north' in available_moves:
            available_moves.remove('north')
    elif head[1] == height - 1:
        if 'south' in available_moves:
            available_moves.remove('south')

    # Definitely don't wanna run into any bodies
    next_coords = {}
    for direction in available_moves:
        next_coords[direction] = utils.get_adjacent_coord(head, direction)

    for direction in next_coords:
        if next_coords[direction] in blocked_coords and direction in available_moves:
            print('Removing direction:', direction)
            available_moves.remove(direction)

    return available_moves
