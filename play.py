import random
import json
import subprocess
import sys
import os
import pathlib
import requests
import base64

API_URL = 'https://texttospeech.googleapis.com/v1/text:synthesize'
AUDIO_DIRECTORY = 'audio'
AUDIO_EXTENSION = 'mp3'
SCRIPT_DIR = pathlib.Path(__file__).parent

def get_req_object(random_number):
    request_filepath = SCRIPT_DIR / 'request.json'
    with open(request_filepath) as req_data:
        request = json.load(req_data)
        request['input']['text'] = str(random_number)
    return json.dumps(request)

def get_auth():
    credentials_file = SCRIPT_DIR / 'google-services-key.json'
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

def get_filepath(number):
    return SCRIPT_DIR / f'{AUDIO_DIRECTORY}/{number}.{AUDIO_EXTENSION}'

def write_file(random_number, bytes):
    filename = get_filepath(random_number)
    with open(filename, 'wb') as outfile:
        outfile.write(bytes)

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
        print('houlà, pas la bonne réponse :( essayez à nouveau !')
        return False

def convert_int_or_quit(user_input):
    try:
        return int(user_input.strip())
    except ValueError:
        print('on a fini !')
        raise SystemExit

def choose_level():
    levels = {'p': 100, 'm': 2000, 'g': 11111, 'tg': 1000000000}
    selected = input('choisir un niveau: (p)etit, (m)oyenne, (g)rand, (tg)très grand: ')
    return levels[selected]

def play_online(level):
    random_number = random.randrange(level)
    audio = get_audio(random_number)
    write_file(random_number, audio)
    play(random_number)

def play_offline():
    available_audio_files = os.listdir(AUDIO_DIRECTORY)
    filename = random.choice(available_audio_files)
    number = pathlib.Path(filename).stem
    play(int(number))

def play(number):
    filepath = get_filepath(number)
    question = "écrivez le chiffre que vous avez entendu: "
    listen(filepath)
    user_input = input(question)
    while not mark_correct(number, convert_int_or_quit(user_input)):
        listen(filepath)
        user_input = input(question)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--offline':
        print('jouer hors ligne')
        while True:
            play_offline()
    else:
        # Premake audio files directory for saving audio.
        pathlib.Path(AUDIO_DIRECTORY).mkdir(exist_ok=True)
        print('jouer en ligne')
        level = choose_level()
        while True:
            play_online(level)

main()
