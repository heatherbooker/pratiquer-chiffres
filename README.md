# Practice u some numbres in fremch

## Requirements
- python 3
- vlc
- google cloud account
- gcloud CLI

## Go go gadget

Step 1: Set up some google cloud something something, idk once was enough for me, you're on your own :joy:
I can at least tell you your creds should be in `google-services-key.json`.

Step 2:
```sh
python play.py
```

:heart_eyes:

Reference for Google API: https://cloud.google.com/text-to-speech/docs/voices?hl=en_US

## TODO
- change requests.json to get different voices
- add ability to say "999 done" in the same line
- catch KeyboardInterrupt to exit happily
- track how many numbers you studied
- track which numbers / types of numbers you got wrong
- add levels to offline mode
- check for existing audio files in online mode before making request
