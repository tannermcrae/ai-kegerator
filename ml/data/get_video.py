import numpy as np
import cv2
from time import sleep

# VideoCapture(0) is typically your computer's built-in webcam. Since I used a usb camera, I had to specify to use that by inputting 1 instead of 0
cap = cv2.VideoCapture(1)


## Example video names: I recommend naming them in this manner cause then you can splice the filename by the '_' and use it to label the image class. 
# 4rack_tysondrumsticksthighswings.mp4
# 7rack_genericchickenbreast.mp4

# Define the codec and create VideoWriter object. For mac mp4v or avi1 is the best option. You can also use: 0x00000021 if this codec doesn't work for you
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

# Create a video writer, specify the codec as well as the image widge and height. cap.get(3) is the width, and cap.get(4) is the heigh of the camera in cap. 
out = cv2.VideoWriter('sideview_8.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret==True:
        # frame = cv2.flip(frame,0)
        # write the flipped frame
        out.write(frame)

    	# Display the resulting frame
        cv2.imshow('frame',frame)
        # Keep recording until someone types q to stop the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()