import cv2
from flask import Flask
from flask import make_response
import threading

img = []
cap = None
app = Flask(__name__)
app_not_done = True

@app.route('/image')
def get_image():
    retval, buffer = cv2.imencode('.jpg', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'
    return response


class CameraThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global img
        global app_not_done

        print("+++++++++ SETTING UP CAMERA ++++++++")
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cnt = 0
        while(app_not_done):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:
                img = frame
            else:
                cnt += 1
                if cnt < 4:
                    print("Could not read camera")

        # When everything done, release the capture
        print("RELEASING CAMERA *******************")
        cap.release()


if __name__ == '__main__':
    thrd = CameraThread('camera_thread')
    thrd.daemon = True
    thrd.start()

    app.run(port=5000)

    app_not_done = False
    thrd.join()
