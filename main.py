from flask import Flask, render_template
from flask_socketio import SocketIO,send,emit,join_room, leave_room



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins='*')

@socketio.on('join')
def on_join(data):
    print('joining',data)
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'text': username + ' has entered the room.','type':'info'}, room=room, broadcast=True,include_self=False)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('message')
def handle_message(data):
    print(data)
    room = data['room']
    emit('message', {'text': data['message']}, room=room, broadcast=True,include_self=False)



if __name__ == '__main__':
    socketio.run(app,port=5000)