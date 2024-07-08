from flask import Flask, send_from_directory
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f'{username} has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f'{username} has left the room.', to=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    msg = data['msg']
    send(f'{username}: {msg}', to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
