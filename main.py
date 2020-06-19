from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from decode_json import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

########################################
#      Server-side event handlers      #
########################################
# receiving string message
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

# receiving json
@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    decode(json)


if __name__ == '__main__':
    socketio.run(app)