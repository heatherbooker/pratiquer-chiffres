import random
import json
import subprocess
import sys
import pathlib
import requests
import base64

API_URL = 'https://texttospeech.googleapis.com/v1/text:synthesize'

def get_req_object(random_number):
    req_data = json.load(open('request.json'))
    req_data['input']['text'] = str(random_number)
    return json.dumps(req_data)

def get_auth():
    credentials_file = 'google-services-key.json'
    command = ['gcloud', 'auth', 'application-default', 'print-access-token']
    command_output = subprocess.run(
            command,
            capture_output=True,
            text=True,
            env={'GOOGLE_APPLICATION_CREDENTIALS': credentials_file})
    return command_output.stdout.strip()

def send_request(data, auth):
    headers = {
        'Authorization': f'Bearer {auth}',
        'Content-Type': 'application/json; charset=utf-8',
    }
    return requests.post(API_URL, headers=headers, data=data)

def process_response(response):
    try:
        encoded_audio = response.json()['audioContent']
        return base64.b64decode(encoded_audio)
    except KeyError:
        print('oopies, got a key error while parsing response; we sent:')
        print(response.request)
        print('and the response was:')
        print(response.json())
        raise

def write_file(random_number, bytes):
    dirname = 'audio'
    pathlib.Path(dirname).mkdir(exist_ok=True)
    filename = f'{dirname}/{random_number}.mp3'
    outfile = open(filename, 'wb')
    outfile.write(bytes)
    outfile.close()
    return filename

def get_audio(random_number):
    req_data = get_req_object(random_number)
    auth = get_auth()
    api_response = send_request(req_data, auth)
    audio = process_response(api_response)
    return audio

def listen(filename):
    command = ['cvlc', '--play-and-exit', filename]
    subprocess.Popen(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def mark_correct(number, guess):
    if number == guess:
        print('très bien !')
        return True
    else:
        print('uh oh, pas la bonne réponse :( essayez à nouveau !')
        return False

def convert_int_or_quit(user_input):
    try:
        return int(user_input.strip())
    except ValueError:
        print('on a fini !')
        raise SystemExit

def play_the_game():
    random_number = random.randrange(100)
    audio = get_audio(random_number)
    filename = write_file(random_number, audio)
    listen(filename)
    question = "écrivez le chiffre que vous avez entendu: "
    user_input = input(question)
    while not mark_correct(random_number, convert_int_or_quit(user_input)):
        user_input = input(question)

while True:
    play_the_game()
