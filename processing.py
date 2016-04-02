import numpy as np
import os
from subprocess import *
from scipy.io import wavfile
from fingerprint import fingerprint
from time import strftime
from datetime import datetime
from requests import get

PHONE = "84959951057"
KEYS = {"6F746934-B02C-FFFE-18F6-E0BB24A791E3": "79629608747",
        "3F6A479C-1FBA-0810-3B64-A32A4DC97189": "79651055295",
        "E69B08ED-D14C-4695-037F-7ECE6403179D": "79250745534"}
FNULL = open(os.devnull, 'w')
URL = "http://sms.ru/sms/send"


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def convert(filename):
    wavname = filename[:-3] + "wav"
    call(["mpg123", "-w", wavname, filename],
         stdout=FNULL, stderr=STDOUT)
    _, record = wavfile.read(wavname)
    record = record[:, 0]
    call(["rm", filename, wavname], stdout=FNULL, stderr=STDOUT)
    return record


def get_time_to_summer():
    time = datetime.now()
    return 24 * (62 - time.day) - (time.hour + 1)


def send_message():
    text = "HoursLeft:+" + str(get_time_to_summer()) + ";;"
    text += "Call:+" + PHONE
    print strftime("%H-%M-%S") + " - SIGNAAAAAAAAAAAAAAAAL!!!!!!!!!!!"
    for key, number in KEYS:
        params = {"api_id": key,
                  "to": number,
                  "text": text,
                  }
        get(URL, params=params)


def recognize(filename, example_hash):
    record = convert(filename)
    density = np.array([len(example_hash.intersection(
        set(x[0] for x in fingerprint(chunk))))
        for chunk in chunks(record, 2048)])
    if np.max(density) >= 4:
        send_message()
    print (strftime("%H-%M-%S") + " - Density mean:",
           np.mean(density), "Max Value: ", np.max(density))
