from twilio.rest import Client
from dotenv import load_dotenv
from pyngrok import ngrok
from flask import Flask
import argparse
import os
import time

load_dotenv() # Load environment variables from .env file
app = Flask(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--to', type=int, default=923350591654, help='Receiver phone number. Start from country code')
    parser.add_argument('--port', type=int, default=5000, help='By default port number is 5000')
    return parser.parse_args()

def console_loading():
    for i in range(3):
        print(".",end="",flush=True)
        time.sleep(0.5)
    print("\r   \r", end="", flush=True)

def call_queued(call):
    i=0
    while call.status == 'queued':
        i+=1
        if i==1:
            print("Call is connecting ",end="",flush=True)
        for i in range(3):
            print('.',end="",flush=True)
            time.sleep(0.5)
        print("\033[4D \033[K", end="", flush=True)
    
        
def call_ringing(call):
    i=0
    while call.status == 'ringing':
        i+=1
        if i==1:
            print("Call is connecting ",end="",flush=True)
        for i in range(3):
            print('.',end="",flush=True)
            time.sleep(0.5)
        print("\033[4D \033[K", end="", flush=True)
    
        

@app.route("/", methods=['GET'])
def index():
    return ""

if __name__ == "__main__":
    args = parse_args()

    # Start ngrok and get the public URL
    ngrok_tunnel = ngrok.connect(args.port, bind_tls=True)
    public_url = ngrok_tunnel.public_url

    # Wait for Ngrok to connect
    i=0
    while "https" not in public_url:
        i=i+1
        if i==1:
            print("Waiting for Ngrok to connect ",end="",flush=True)
        for i in range(3):
            print('.',end="",flush=True)
            time.sleep(0.5)
        print("\033[4D \033[K", end="", flush=True)
        time.sleep(1)
        ngrok_tunnel = ngrok.connect(args.port, bind_tls=True)
        public_url = ngrok_tunnel.public_url

    print("\r   \r", end="", flush=True)  # remove the text from the console
    print("Ngrok Server is running.", flush=True)

    twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_ID'),os.environ.get('TWILIO_AUTH_TOKEN'))

    call = twilio_client.calls.create(
    to=f"{args.to}",
    url=f'{public_url}/twiml',
    from_='+12029000087',
    )

    # Monitor call status until it is no longer "queued" or "ringing"
    i=0
    while True:
        i+=1
        call = twilio_client.calls(call.sid).fetch()
        if call.status == "queued":
            call_queued(call)
        elif call.status == "ringing":
            print("\r   \r", end="", flush=True)
            print("Call is connected. ",flush=True)
            print("\n\nCall is ringing ",end="",flush=True)
            call_ringing(call)
        elif call.status == "in-progress":
            print("Call is in progress...")
        elif call.status == "completed":
            print("Call has completed.")
            break
        else:
            print("Call status: ", call.status)
    
        time.sleep(1)
        print(".", end="", flush=True)

    # Run the Flask app
    app.run()


# Twilio Call Status
# queued: The call is queued and waiting to be executed by the Twilio platform.
# ringing: The call is being initiated and is ringing on the destination number.
# in-progress: The call has been answered and is currently in progress.
# completed: The call has been completed and has ended normally.
# busy: The destination number is busy and the call could not be completed.
# failed: The call has failed for some reason, such as an invalid destination number or network error.
# no-answer: The call was not answered and has been terminated.
# canceled: The call has been canceled by the caller or the Twilio platform.