import pyaudio
import sys
import socket
import datetime
from time import sleep, time

HOST = sys.argv[1]
PORT = sys.argv[2]

data = bytes() # Stream of audio bytes

CHUNK_SIZE = 4096
BROADCAST_SIZE = 8192
CHANNELS = 2
FORMAT = pyaudio.paInt16 # 2 bytes size
RATE = 44100

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def pyaudio_callback(in_data, frame_count, time_info, status):
    global data
    data += in_data
    return (None, pyaudio.paContinue)

# open stream (3)
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                stream_callback=pyaudio_callback)

# start the stream (4)
stream.start_stream()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, int(PORT)))

def send_data():
    global data
    if (len(data) > BROADCAST_SIZE):
        sock.sendall(data[:BROADCAST_SIZE])
        data = data[BROADCAST_SIZE:]
        print(f'Sending {str(BROADCAST_SIZE)} bytes of audio. {datetime.datetime.now().time()}', end='\r')

try:
    print(f'Sending {str(round(RATE / BROADCAST_SIZE))} packets per second.')
    sleeptime = 1 / (RATE / BROADCAST_SIZE) / CHANNELS / 2
    while True:
        send_data()
        sleep(sleeptime - (time() % sleeptime))
except KeyboardInterrupt:
    print('\nClosing stream...')
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
