import picamera
import io
import time

class Camera():
    def __init__(self):

        WIDTH = 128
        HEIGHT = 96

        self.cam = picamera.PiCamera()
        self.cam.resolution = (WIDTH, HEIGHT)

        self.cam.rotation = 180
        self.cam.framerate = 60

        self.out = io.BytesIO()
        self.return_type = 'jpeg'


    def get_camera(self):
        return self.cam

    def capture(self):
        d = time.time()

        self.cam.capture(self.out, 'jpeg', use_video_port=True)

        d2 = time.time()
        t = self.out.getvalue()
        d3 = time.time()
        self.out.seek(0)
        print("camera: %.5f %.5f %.5f" % ( time.time()-d3, d3-d2, d2-d ) )
        return t


