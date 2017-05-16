import picamera
import io


class Camera():
    def __init__(self):

        WIDTH = 128
        HEIGHT = 96

        self.cam = picamera.PiCamera()
        self.cam.resolution = (WIDTH, HEIGHT)

        self.cam.rotation = 180
        self.cam.framerate = 30

        self.out = io.BytesIO()
        self.return_type = 'jpeg'


    def capture(self):
        self.cam.capture(self.out, self.return_type, use_video_port=True)
        t = self.out.getvalue()
        self.out.write(b'')
        self.out.seek(0)
        return t


