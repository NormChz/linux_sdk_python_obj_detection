# INSTRUCTIONS

## General
- Download the model (.eim file) from Edge Impulse and 
- The test images and .eim files should be placed inside the work directory, next to the programs.

## obj_det_img_bboxes.py
- Detect the objects on single images.
- Change the model name (line 8) to match the name of the model that you want to use.
- Change the imagename inside (line 9) to match the image that you want to run inference on.
- Resize image to the size that you need (line 13)

## obj_det_real_time_bboxes.py
- Detect the objects on a video stream.
- Change the model name (line 9) to match the name of the model that you want to use.
- Change resolution width and height as needed (line 10 and 11)
- Change color format as needed (line 12)

## test_camera.py
- tests that the camera is working, and that the array format of the frames can be used by cv2 to display the video and draw a rectangle on it.