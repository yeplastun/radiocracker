import logging
import threading
import time
import datetime
import requests
from io import BytesIO
import constants

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


def check_audio(piece):
    if piece:  # TODO: compare audios, if it returns true it should exit
        send_message()
        exit()


def get_time_to_the_summer():
    logging.debug('Time to the summer' )
    # TODO: it should return datetime to the summer


def send_message():
    date = get_time_to_the_summer()


def run():
    r = requests.get(constants.URL, stream=True)
    r.raw.decode_content = True
    iter = r.iter_content(1024)  # it's about 1 sec of the audio

    # it should create 5 items about 5 seconds each with offset (1 sec).

