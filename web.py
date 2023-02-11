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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)
