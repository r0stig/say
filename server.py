import sys, os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../SoCo'))
print path
if not path in sys.path:
    sys.path.insert(1, path)
del path
from soco import SoCo
from flask import Flask
from say import text2mp3
import time, threading
from threading import Timer
app = Flask(__name__)

PATH = './static/'

#Constants of your choice
LANGUAGE = 'en' # language for speech (en = English)
IP = "192.168.101.178"             #Sonos player to use


@app.route('/say/<text>', methods=['GET'])
def say(text):
    ok, file_name =  text2mp3(text, PATH, LANGUAGE)
    if ok:
        print "Created file.."
        # Play the URL...
        zp = SoCo(IP)
        cur_info = zp.get_current_track_info()
        zp.play_uri("http://192.168.100.123:5000/static/speech.mp3")
        speech_info = zp.get_current_track_info()
        duration = speech_info['duration']
        Timer(duration, resume_queue, (zp, cur_info)).start()

def resume_queue(zp, info):
    position = info['position']
    pl_position = info['playlist_position']
    zp.play_from_queue(pl_position)
    zp.play()
    zp.seek(position)
    print "resumes queue"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)