import subprocess
import sys
import requests
import base64

API_URL = 'https://texttospeech.googleapis.com/v1/text:synthesize'

def get_auth():
    command = ['gcloud', 'auth', 'application-default', 'print-access-token']
    command_output = subprocess.run(
            command,
            capture_output=True,
            text=True)
    return command_output.stdout.strip()

def send_request(data, auth):
    headers = {
        'Authorization': f'Bearer {auth}',
        'Content-Type': 'application/json; charset=utf-8',
    }

    return requests.post(API_URL, headers=headers, data=data)

def process_response(response):
    encoded_audio = response.json()['audioContent']
    return base64.b64decode(encoded_audio)

def write_file(bytes):
    outfile = open('result.mp3', 'wb')
    outfile.write(bytes)
    outfile.close()

def main():
    req_data = open('request.json')
    auth = get_auth()
    api_response = send_request(req_data, auth)
    audio = process_response(api_response)
    write_file(audio)

main()
