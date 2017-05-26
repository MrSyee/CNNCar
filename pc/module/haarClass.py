
import cv2

class Haar:
    def __init__(self, thr = 1.2, file='haarcascade_fullbody.xml'):
        self.thr = thr
        self.cascade = cv2.CascadeClassifier('module/'+file)

    def classify(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        body = self.cascade.detectMultiScale(gray, self.thr, 4)

        for (x,y,w,h) in body:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

        img = cv2.resize(img, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
        cv2.imshow("img_body",img)
        cv2.waitKey(1)
        if len(body) > 0:
            flag = True
        else:
            flag = False
        return flag
