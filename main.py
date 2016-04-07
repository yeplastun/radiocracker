import requests
from time import strftime
from multiprocessing import Process
from processing import recognize
from fingerprint import fingerprint
from scipy.io import wavfile


URL = "http://icecast.rmg.cdnvideo.ru/rr.mp3"
EXAMPLE = "records/cutted_example.wav"


def run():
    _, example = wavfile.read(EXAMPLE)
    example_hash = set(x[0] for x in fingerprint(example))
    request_stream = requests.get(URL, stream=True)
    request_stream.raw.decode_content = True
    stream_iter = request_stream.iter_content(2 ** 17)
    for chunk in stream_iter:
        filename = strftime("tmp/%H-%M-%S-%f.mp3")
        f = open(filename, "wb")
        f.write(chunk)
        f.close()
        p = Process(target=recognize, args=(filename, example_hash))
        p.start()

if __name__ == "__main__":
    run()
