from picamera2 import Picamera2, Preview
import cv2

def get_camera():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={'size':(640, 480)})
    picam2.configure(config)
    picam2.start()
    return picam2

if __name__ == '__main__':
    camera = get_camera()
    print(camera.global_camera_info())

    # random rectangle coordinates
    x, y = 100, 50
    width, height = 200, 150
    color = (0, 255, 0)
    thickness = 2

    while(True):
        img = camera.capture_array()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.rectangle(img, (x, y), (x + width, y + height), color, thickness) # draw a random rectangle on image

        cv2.imshow('camera output: ', img)

        if cv2.waitKey(1) == ord('q'):
            break
    camera.stop()
    cv2.destroyAllWindows()
