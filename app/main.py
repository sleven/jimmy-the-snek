import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

last_direction = None

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    args = {
        'color': '#00FFFF',
        'headType': 'evil',
        'tailType':'small-rattle'
    }

    return start_response(args)


@bottle.post('/move')
def move():
    global last_direction

    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))

    board = [
        [False] * data['board']['width'],
        [False] * data['board']['height'],
    ]
    print(board)

    for snake in data['board']['snakes']:
        print("snake")
        print(snake)
        board[0][snake['body'][0]['x']] = True
        board[1][snake['body'][0]['y']] = True

    current_x = data['you']['body'][0]['x']
    current_y = data['you']['body'][0]['y']

    board[0][current_x] = True
    board[1][current_y] = True

    if current_x + 1 < len(board[0]) and last_direction != 'left':
        if not board[0][current_x + 1]:
            direction = 'right'
    elif current_x > 1 and last_direction != 'right':
        if not board[0][current_x - 1]:
            direction = 'left'
    elif current_y + 1 < len(board[1]) and last_direction != 'down':
        if not board[1][current_y + 1]:
            direction = 'up'
    else:
        direction = 'down'

    last_direction = direction
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
