from flask import Flask, render_template
from flask_socketio import SocketIO,send,emit,join_room, leave_room
from flask_cors import CORS, cross_origin



app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('join')
@cross_origin()
def on_join(data):
    print('joining',data)
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'text': username + ' has entered the room.','type':'info'}, room=room, broadcast=True,include_self=False)

@socketio.on('leave')
@cross_origin()
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


@socketio.on('message')
@cross_origin()
def handle_message(data):
    print(data)
    room = data['room']
    emit('message', {'text': data['message'],'user':data['username']}, room=room, broadcast=True,include_self=False)



if __name__ == '__main__':
    socketio.run(app)
