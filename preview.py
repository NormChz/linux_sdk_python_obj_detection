from picamera2 import Picamera2, Preview
import time
import sys

if __name__ == '__main__':
  if len(sys.argv) == 2:
    duration = int(sys.argv[1])
  else:
    duration = 10

  picam2 = Picamera2()
  camera_config = picam2.create_preview_configuration()
  picam2.configure(camera_config)
  picam2.start_preview(Preview.QTGL)
  picam2.start()
  time.sleep(duration)