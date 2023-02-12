import cv2
from flask import Flask, Response
from flask import make_response
import threading

img = []
cap = None
app = Flask(__name__)

def get_frame():
    while True:
        imgencode = cv2.imencode('.jpg', img)[1]
        frame = imgencode.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/image')
def image():
    retval, buffer = cv2.imencode('.jpg', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'
    return response

@app.route('/video')
def video():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


class CameraThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global img
        global cap
        cap = cv2.VideoCapture(0)

        while True:
            retval, img = cap.read()


if __name__ == '__main__':
    thrd = CameraThread('camera_thread')
    thrd.daemon = True
    thrd.start()

    app.run(host="0.0.0.0", port=5000)

    app_not_done = False
    thrd.join()
