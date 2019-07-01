# AudioRetranslator 

I've done this to watch films on the laptop while hearing audio from the computer speakers :D 

Made with python, sockets & love.

## Requirements

### Mac OS
- Installed [Soundflower](https://github.com/mattingalls/Soundflower/releases) driver on the sender device. For other platforms, it would also work, if you route your computer output to the "emulated input device".
- Installed [PyAudio](https://pypi.org/project/PyAudio/) package on both (sender & receiver) devices.

### Usage
1. [receiver.py](receiver.py) works as the server. Launch it on the receiver machine first:
```
python3 receiver.py YOUR_SERVER_IP YOUR_PORT
```
2. [sender.py](sender.py) works as the client that sends audio. Launch it on the sender machine:
```
python3 sender.py YOUR_SERVER_IP YOUR_PORT
```
3. (Optional) You can try set `CHANNELS` to **1** if you want better performance. (Do it in both `sender.py` and `receiver.py`). Also, play with the `BUFFER_SIZE` (`receiver.py`) to see what latency is good for you. I prefer **16384** or **8192**.

### Sound Check
If everything is OK -> you should hear the audio from the sender device on the receiver device.

## How it works
It simply sends stream of audio bytes with the sockets. The wireless connection is by definition weeker than wired, therefore sometimes you would hear the lags in audio, because the algorithm just skips bytes, if it lost some and buffer started overflowing.

Hope you enjoy it) *Have Fun*!
