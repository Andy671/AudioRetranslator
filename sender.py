import pyaudio
import sys
import socket
import datetime

HOST = sys.argv[1]
PORT = sys.argv[2]

data = bytes() # Stream of audio bytes

CHUNK_SIZE = 2048
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
    if (len(data) > CHUNK_SIZE * CHANNELS * 2):
        sock.sendall(data[:CHUNK_SIZE * CHANNELS * 2])
        data = data[CHUNK_SIZE * CHANNELS * 2:]
        print(f'Sent {str(CHUNK_SIZE * CHANNELS * 2)} bytes of audio. {datetime.datetime.now().time()}')

try:
    while True:
        send_data()
except KeyboardInterrupt:
    print('\nClosing stream...')
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
