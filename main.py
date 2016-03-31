import logging
import threading
import time
import datetime
import requests
from io import BytesIO
import constants
from cutting_example import run

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


def check_audio(piece):
    if piece:  # TODO: compare audios, if it returns true it should exit
        send_message()
        exit()


def get_time_to_the_summer():
    logging.debug('Time to the summer')
    # TODO: it should return datetime to the summer


def send_message():
    date = get_time_to_the_summer()

    # it should create 5 items about 5 seconds each with offset (1 sec).

if __name__ == "__main__":
    run()
