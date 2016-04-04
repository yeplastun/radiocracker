import numpy as np
import os
import telegram
import logging
from subprocess import *
from scipy.io import wavfile
from fingerprint import fingerprint
from time import strftime
from datetime import datetime

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO, filename=u'mylog.log')


PHONE = "84959951057"
KEYS = {"6F746934-B02C-FFFE-18F6-E0BB24A791E3": "79629608747",
        "3F6A479C-1FBA-0810-3B64-A32A4DC97189": "79651055295",
        "E69B08ED-D14C-4695-037F-7ECE6403179D": "79250745534"}
TOKEN = "172147185:AAG0qfWa1eXK64EErXoK-UUAbbPsa8y9R-8"
FNULL = open(os.devnull, 'w')
URL = "http://sms.ru/sms/send"
IDS = set([35787351, 36350301, 44115250, 675729])
BOT = telegram.Bot(token="172147185:AAG0qfWa1eXK64EErXoK-UUAbbPsa8y9R-8")


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def convert(filename, wavname):
    call(["mpg123", "-w", wavname, filename],
         stdout=FNULL, stderr=STDOUT)
    _, record = wavfile.read(wavname)
    record = record[:, 0]
    return record


def get_time_to_summer():
    time = datetime.now()
    return 24 * (62 - time.day) - (time.hour + 1)


def send_message():
    text = "HoursLeft: " + str(get_time_to_summer()) + "\n"
    text += "Call: " + PHONE + "\n"
    text += "Now: " + strftime("%H-%M-%S")
    for id in IDS:
        BOT.sendMessage(chat_id=id, text=text)


def recognize(filename, example_hash):
    wavname = filename[:-3] + "wav"
    record = convert(filename, wavname)
    density = np.array([len(example_hash.intersection(
        set(x[0] for x in fingerprint(chunk))))
        for chunk in chunks(record, 2048)])
    logging.info("Density mean: " + str(np.mean(density)) +
                 " Max Value: " + str(np.max(density)))
    if np.max(density) >= 4:
        logging.warning(
            strftime("%H-%M-%S") + " - SIGNAAAAAAAAAAAAAAAAL!!!!!!!!!!!")
        send_message()
        call(["rm", filename], stdout=FNULL, stderr=STDOUT)
    else:
        call(["rm", filename, wavname], stdout=FNULL, stderr=STDOUT)
