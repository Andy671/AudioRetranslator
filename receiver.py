import pyaudio
import sys
import socket

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

    try:
        # Cut the data, if it started to bufferize 
        # TODO: improve this behavior to skip only the amount we missed
        if len(data) > frame_count * CHANNELS * 4:
            print('Cutting the audio..')
            data = data[-frame_count * CHANNELS * 2:]

        avail_data_count = min(frame_count * CHANNELS * 2, len(data))
        return_data =  data[:avail_data_count]
        data = data[avail_data_count:]
        
        # Inflate end of the array with zeros, if there is not enough audio.
        for i in range(avail_data_count, frame_count * CHANNELS * 2):
            return_data += bytes([0])
        
        return (return_data, pyaudio.paContinue)
    except:
        print('Exception in pyaudio_callback...')


# open stream (3)
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK_SIZE,
                stream_callback=pyaudio_callback)

# start the stream (4)
stream.start_stream()
print('Stream started.')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, int(PORT)))
sock.listen(1)
connection, client_address = sock.accept()
print('Socket bind succeed.')

try:
    while True:
        new_data = connection.recv(CHUNK_SIZE * CHANNELS * 2)
        data += new_data
except KeyboardInterrupt:
    print('\nClosing socket and stream...')
    sock.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
