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
    outfile = open(f'{dirname}/{random_number}.mp3', 'wb')
    outfile.write(bytes)
    outfile.close()

def main():
    random_number = random.randrange(100)
    req_data = get_req_object(random_number)
    auth = get_auth()
    api_response = send_request(req_data, auth)
    audio = process_response(api_response)
    write_file(random_number, audio)
    print("success!")

main()
