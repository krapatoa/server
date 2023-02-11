from typing import Optional

from flask import Flask, Response, abort
import cv2

app = Flask(__name__)

frame: Optional[bytes] = None


def start_camera():
    print("Camera")
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    while True:
        global frame
        retval, im = camera.read()
        print("read")
        imgencode = cv2.imencode('.jpg', im)[1]
        frame = imgencode.tostring()


def frame_response():
    global frame
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    global frame
    if frame is None:
        abort(404)
    return Response(frame_response(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    start_camera()
