from routes.twilio import app as routes
from twilio.rest import Client
from dotenv import load_dotenv
from pyngrok import ngrok
from flask import Flask
import argparse
import time
import os

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
app.register_blueprint(routes)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--to', type=int, default=923350591654, help='Receiver phone number. Start from country code')
    parser.add_argument('--port', type=int, default=5000, help='By default port number is 5000')
    return parser.parse_args()

def console_loading():
    for i in range(3):
        print('.',end="",flush=True)
        time.sleep(0.5)
    print("\033[4D \033[K", end="", flush=True)

def call_status(status):
    i=0
    while twilio_client.calls(call.sid).fetch().status==status:
        i+=1
        if i==1:
            print(f"\033[93m { 'Connecting '  if status=='queued' else 'Ringing '} \033[0m",end="",flush=True)
        console_loading()
    print("\r   \r", end="", flush=True)
    

if __name__ == "__main__":
    args = parse_args()

    # Start ngrok and get the public URL
    ngrok_tunnel = ngrok.connect(args.port, bind_tls=True)
    public_url = ngrok_tunnel.public_url

    # Wait for Ngrok to connect
    i=0
    while "https" not in public_url:
        i+=1
        if i==1:
            print("\033[93m Waiting for Ngrok to connect \033[0m",end="",flush=True)
        console_loading()
        time.sleep(1)
        ngrok_tunnel = ngrok.connect(args.port, bind_tls=True)
        public_url = ngrok_tunnel.public_url

    print("\r   \r", end="", flush=True)  # remove the text from the console
    print("\n\033[92m Ngrok Server is running. \033[0m", flush=True)
    print(f"\033[96m {public_url} \033[0m", flush=True)
    time.sleep(20)
    twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_ID'),os.environ.get('TWILIO_AUTH_TOKEN'))

    call = twilio_client.calls.create(
    to=f"{args.to}",
    url=f'{public_url}/twiml',
    from_='+12029000087',
    )

    # Monitor call status 
    while True:
        call=twilio_client.calls(call.sid).fetch()
        if call.status=='queued':
            call_status("queued")
            print("\033[92m Call is connected. \033[0m",flush=True)
            
        elif call.status=='ringing':
            call_status(call.status)
            app.run()
        elif call.status=='in-progress':
            print("\033[95m Call is in progress. \033[0m",flush=True)
            
        else:
            print(f"\033[91m Call status: {call.status} \033[0m\n")
            break


# Twilio Call Status
# queued: The call is queued and waiting to be executed by the Twilio platform.
# ringing: The call is being initiated and is ringing on the destination number.
# in-progress: The call has been answered and is currently in progress.
# completed: The call has been completed and has ended normally.
# busy: The destination number is busy and the call could not be completed.
# failed: The call has failed for some reason, such as an invalid destination number or network error.
# no-answer: The call was not answered and has been terminated.
# canceled: The call has been canceled by the caller or the Twilio platform.