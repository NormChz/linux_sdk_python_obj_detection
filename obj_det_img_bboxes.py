import os, sys
import cv2
from edge_impulse_linux.image import ImageImpulseRunner

dir_path = os.path.dirname(os.path.realpath(__file__))

# Settings
model_file = "yolo_example_320x320-linux-aarch64-v7.eim" # Trained ML model from Edge Impulse (replace name with your .eim file)
img = 'example.png' # image for object detection (replace example with your image name)
model_path = os.path.join(dir_path, model_file)

img = cv2.imread(os.path.join(dir_path, img), cv2.IMREAD_COLOR)
img = cv2.resize(img, (320, 320)) # resize the image (works best if you resize to the size that the model is trained on)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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
if res is not None:
    if "bounding_boxes" in res["result"].keys():
        print('Found %d bounding boxes (%d ms.)' % (len(res["result"]["bounding_boxes"]), res['timing']['dsp'] + res['timing']['classification']))
        for bb in res["result"]["bounding_boxes"]:
            print('\t%s (%.2f): x=%d y=%d w=%d h=%d' % (bb['label'], bb['value'], bb['x'], bb['y'], bb['width'], bb['height']))
            img = cv2.rectangle(img, (bb['x'], bb['y']), (bb['x'] + bb['width'], bb['y'] + bb['height']), (0, 0, 255), 1)

# Show the frame
cv2.imshow("Frame", img)
cv2.waitKey(0)
cv2.destroyAllWindows()