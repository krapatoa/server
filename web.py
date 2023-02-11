from typing import Optional

from flask import Flask, Response, abort
import cv2

app = Flask(__name__)

camera: Optional[cv2.VideoCapture] = None
frame: Optional[bytes] = None


def setup_camera():
    global camera
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)


def get_frame():
    global camera
    while True:
        retval, im = camera.read()
        imgencode = cv2.imencode('.jpg', im)[1]
        frame = imgencode.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    global camera
    if camera is None:
        abort(503)
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    setup_camera()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
