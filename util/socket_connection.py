from flask_socketio import SocketIO

socketio=SocketIO()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('stream')
def handle_stream(data):
    print('Received data:', data)