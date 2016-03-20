import logging
import threading
import time
import datetime
import requests
from io import BytesIO
import constants

"""
This is an example of cutting an audio stream to 5 sec. pieces.
"""
def run():
    request_stream = requests.get(constants.URL, stream=True)
    request_stream.raw.decode_content = True
    stream_iter = request_stream.iter_content(10240)

    streams = [BytesIO() for o in range(5)]

    for i in range(5):
        chunk = stream_iter.next()
        for j in range(i + 1):
            streams[j].write(chunk)
    # print
        print [(p, streams[p].tell()) for p in range(len(streams)) ]
        print

    for o in range(50):  # TODO: while True:
        # print
        print [(p, streams[p].tell()) for p in range(len(streams)) ]
        print

        # worker
        streams = streams[-5:]
        streams.append(BytesIO())

        for i in range(5):
            streams[i].write(stream_iter.next())

run()