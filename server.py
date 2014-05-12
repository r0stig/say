import sys, os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../soco-test/SoCo'))
print path
if not path in sys.path:
    sys.path.insert(1, path)
del path
from soco import SoCo
from flask import Flask
from say import text2mp3
import time, threading
import soco
from threading import Timer
from mutagen.mp3 import MP3
app = Flask(__name__)

PATH = './static/'

#Constants of your choice
LANGUAGE = 'en' # language for speech (en = English)
IP = "192.168.1.90"             #Sonos player to use
LAN_IP = "192.168.1.29"         # Local area ip that sonos can reach
PORT = 5000


@app.route('/say/<text>', methods=['GET'])
def say(text):
    ok, file_name =  text2mp3(text, PATH, LANGUAGE)
    if ok:
        zp = SoCo(IP)
        cur_info = zp.get_current_track_info()
        state = zp.get_current_transport_info()
        zp.play_uri("http://{0}:5000/static/speech.mp3".format(LAN_IP))
        if (state['current_transport_state'] == 'PLAYING'):
            audio = MP3("./static/speech.mp3")
            speech_info = zp.get_current_track_info()
            duration = speech_info['duration']
            Timer(audio.info.length, resume_queue, (zp, cur_info)).start()
    return "OK!"

def resume_queue(zp, info):
    position = info['position']
    pl_position = info['playlist_position']
    zp.play_from_queue(int(pl_position) - 1 ) #Until newest version applied -1 is needed
    zp.play()
    zp.seek(position)


if __name__ == "__main__":
   #for zone in soco.discover():
   #     print zone

    app.run(host='0.0.0.0', debug=True)
