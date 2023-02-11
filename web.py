from flask import Flask, Response
import cv2

app = Flask(__name__)

def camera():
    global frame

    camera_port = 0
    camera = cv2.VideoCapture(camera_port)

    while True:
        retval, im = camera.read()
        imgencode = cv2.imencode('.jpg', im)[1]
        frame = imgencode.tostring()

def frame_response():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(frame_response(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    camera()
