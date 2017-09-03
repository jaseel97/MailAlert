import cv2
import time

camera_port = 0
ramp_frames = 30
camera = cv2.VideoCapture(camera_port)
def get_image():
 retval, im = camera.read()
 return im
for i in xrange(ramp_frames):
 temp = get_image()
print("Taking image...")
time.sleep(0.5)
camera_capture = get_image()
file = "/mnt/e/Sandbox/bashbox/MailAlert/test_image.png"
cv2.imwrite(file, camera_capture)
del(camera)
