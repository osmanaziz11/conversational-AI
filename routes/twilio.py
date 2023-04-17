from twilio.twiml.voice_response import VoiceResponse, Start
from flask import Blueprint

app = Blueprint('app', __name__)

@app.route("/twiml", methods=['POST'])
def twiml_response():
    response = VoiceResponse()
    start = Start()
    # start.stream(url=f'wss://{request.host}/stream')
    response.append(start)
    response.say('Please leave a message')
    response.pause(length=60)
    return str(response)

@app.route("/", methods=['GET'])
def index():
    
    return ""

