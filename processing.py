import numpy as np
import os
from subprocess import *
from scipy.io import wavfile
from fingerprint import fingerprint
from time import strftime

NUMBERS = []
FNULL = open(os.devnull, 'w')


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
    pass


def send_message():
    print strftime("%H-%M-%S") + " - SIGNAAAAAAAAAAAAAAAAL!!!!!!!!!!!"


def recognize(filename, example_hash):
    record = convert(filename)
    density = np.array([len(example_hash.intersection(
        set(x[0] for x in fingerprint(chunk))))
        for chunk in chunks(record, 2048)])
    if np.max(density) >= 4:
        send_message()
    print (strftime("%H-%M-%S") + " - Density mean:",
           np.mean(density), "Max Value: ", np.max(density))
