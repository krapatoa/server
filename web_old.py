import os
import threading
from datetime import time

import flask
from flask import Flask, Response
import cv2

app = Flask(__name__)

def get_frame():
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    while True:
        retval, im = camera.read()
        imgencode = cv2.imencode('.jpg', im)[1]
        frame = imgencode.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/value')
def value():
    return flask.current_app.__getattribute__('value')

# def camera_thread():
#     while True:
#         print('hej')
#         time.sleep(1)
#
#
# if os.getpid() == 1:
#     t = threading.Thread(target=camera_thread)
#     t.start()
