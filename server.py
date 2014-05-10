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


@app.route('/say/<text>', methods=['GET'])
def say(text):
    ok, file_name =  text2mp3(text, PATH, LANGUAGE)
    if ok:
        print "Created file.."
        # Play the URL...
        #info = zp.get_current_track_info()
        Timer(3, resume_queue, ()).start()
        # Sleep for info.duration (shedelue)
        # after sleep

    return ""

def resume_queue():
    print "resumes queue"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)