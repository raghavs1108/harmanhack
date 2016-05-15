from bottle import route, run, static_file, redirect, hook, request, response
from bottle import *
from audio import record, play
import requests
import os

PI_IP = "192.168.2.3"

recordings_dir = os.path.join(os.getcwd(), "recordings")
if not os.path.exists(recordings_dir):
	os.makedirs(recordings_dir)

@route("/")
def index():
	redirect("/static/index.html")

@route("/static/<filename:path>")
def serve_static(filename):
	return static_file(filename, root="./static")

@route("/record")
def record_audio():
	record("record_one")
	f = open("./recordings/record_one", "rb")
	requests.post("http://" + PI_IP + ":8000/upload", files={'upload': open("./recordings/record_one", "rb")})

@hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@route("/upload", method="POST")
def upload_audio():
	audio_file = request.files.get('upload')
	save_path = os.getcwd() + "recordings"
	audio_file.save(save_path)
	return 'OK'

@route("/play")
def play_audio():
	play("record_one")

if __name__ == "__main__":
	run(host="0.0.0.0", port=8000, debug=True)