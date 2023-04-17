from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return ""

@app.route("/twiml", methods=['GET'])
def twiml_response():
    return ""

