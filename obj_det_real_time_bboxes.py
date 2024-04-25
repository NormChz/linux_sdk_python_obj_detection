import os, sys
import cv2
from picamera2 import Picamera2
from edge_impulse_linux.image import ImageImpulseRunner

dir_path = os.path.dirname(os.path.realpath(__file__))

# Settings
model_file = "yolo_example_320x320-linux-aarch64-v7.eim" # replace with your .eim model
res_width = 640                          # Resolution of camera (width)
res_height = 640                         # Resolution of camera (height)
rotation = 0                            # Camera rotation (0, 90, 180, or 270)
cam_format = "RGB888"                   # Color format

model_path = os.path.join(dir_path, model_file)

# Load the model file
runner = ImageImpulseRunner(model_path)

# Initialize model (and print information if it loads)
try:
    model_info = runner.init()
    print("Model name:", model_info['project']['name'])
    print("Model owner:", model_info['project']['owner'])
    
# Exit if we cannot initialize the model
except Exception as e:
    print("ERROR: Could not initialize model")
    print("Exception:", e)
    if (runner):
            runner.stop()
    sys.exit(1)

# Interface with camera
with Picamera2() as camera:

    
    # Configure camera settings
    config = camera.create_video_configuration(main={"size": (res_width, res_height), "format": cam_format})
    camera.configure(config)

    # Start camera
    camera.start()
    
    # Continuously capture frames
    while True:
        
        # Get array that represents the image (in RGB format)
        img = camera.capture_array()

        # Rotate image
        if rotation == 0:
            pass
        elif rotation == 90:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif rotation == 180:
            img = cv2.rotate(img, cv2.ROTATE_180)
        elif rotation == 270:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            print("ERROR: rotation not supported. Must be 0, 90, 180, or 270.")
            break
        
        # Extract features (e.g. grayscale image as a 2D array)
        features, cropped = runner.get_features_from_image(img)
        
        # Perform inference
        res = None
        try:
            res = runner.classify(features)
        except Exception as e:
            print("ERROR: Could not perform inference")
            print("Exception:", e)
            
        # Display predictions and timing data
        print("-----")
        print(res)
        if res is not None:
            if "bounding_boxes" in res["result"].keys():
                print('Found %d bounding boxes (%d ms.)' % (len(res["result"]["bounding_boxes"]), res['timing']['dsp'] + res['timing']['classification']))
                for bb in res["result"]["bounding_boxes"]:
                    print('\t%s (%.2f): x=%d y=%d w=%d h=%d' % (bb['label'], bb['value'], bb['x'], bb['y'], bb['width'], bb['height']))
                    img = cv2.rectangle(img, (bb['x'], bb['y']), (bb['x'] + bb['width'], bb['y'] + bb['height']), (0, 255, 0), 1)

        # Show the frame
        cv2.imshow("Frame", img)
        
        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break
        
# Clean up
cv2.destroyAllWindows()