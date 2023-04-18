from flask_sock import Sock
import json

sock=Sock()

@sock.route('/stream')
def stream(ws):
    """Receive and transcribe audio stream."""
    while True:
        message = ws.receive()
        packet = json.loads(message)
        if packet['event'] == 'start':
            print('Streaming is starting')
        elif packet['event'] == 'stop':
            print('\nStreaming has stopped')
        elif packet['event'] == 'media':
            print("Receving audio...")