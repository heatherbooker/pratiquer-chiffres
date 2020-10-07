import subprocess
import sys
import requests
import base64

auth = subprocess.run(['gcloud', 'auth', 'application-default', 'print-access-token'], capture_output=True, text=True).stdout.strip()
headers = {
    'Authorization': f'Bearer {auth}',
    'Content-Type': 'application/json; charset=utf-8',
}
url = 'https://texttospeech.googleapis.com/v1/text:synthesize'
req_data = open('request.json')

response = requests.post(url, headers=headers, data=req_data)
print(response.json())

encoded_audio = response.json()['audioContent']

audio = base64.b64decode(encoded_audio)

outfile = open('result.mp3', 'wb')
outfile.write(audio)
outfile.close()
