#! /usr/bin/python


import pyaudio
import wave
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 7
RECORDINGS = os.path.join(os.getcwd(), "recordings")


def record(filename):
	file_location = os.path.join(RECORDINGS, filename)
	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)

	print("Started Recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	print("Done Recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(file_location, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


def play(filename):
	file_location = os.path.join(RECORDINGS, filename)

	if not os.path.isfile(file_location):
		print "Invalid file"
		exit(-1)

	wf = wave.open(file_location, 'rb')

	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
	                channels=wf.getnchannels(),
	                rate=wf.getframerate(),
	                output=True)

	data = wf.readframes(CHUNK)

	while data != '':
	    stream.write(data)
	    data = wf.readframes(CHUNK)

	stream.stop_stream()
	stream.close()

	p.terminate()


if __name__ == "__main__":
	record("record_one")
