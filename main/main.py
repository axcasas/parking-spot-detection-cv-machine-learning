# Dependencies

import cv2
import matplotlib.pyplot as plt
import numpy as np
from utils import get_parking_spots_bboxes, empty_or_not

mask = 'data/mask_1920_1080.png'
video_path = 'data/parking_1920_1080_loop.mp4'

# Init 

mask = cv2.imread(mask,0)
cap = cv2.VideoCapture(video_path)

connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)

spots = get_parking_spots_bboxes(connected_components)
print(spots[0])

# Main Loop 

ret = True
available_spots = 0

while ret:
    ret, frame = cap.read()

    # reset counter
    available_spots = 0

    # for loop for spots 
    for spot in spots:
        x1,y1,w,h = spot

        spot_crop = frame[y1:y1 + h, x1:x1 + w, :]
        spot_status = empty_or_not(spot_crop)

        if spot_status:
            frame = cv2.rectangle(frame,(x1,y1),(x1 + w, y1 + h), (0,255,0),2)
            available_spots += 1
        else:
            frame = cv2.rectangle(frame,(x1,y1),(x1 + w, y1 + h), (0,0,255),2)

    cv2.rectangle(frame, (80,20), (630, 80), (0,0,0), -1)
    cv2.putText(frame, 'Lugares Disponibles: {} / {}'.format(str(available_spots),str(len(spots))), (100,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)

    cv2.imshow('frame',frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release 
cap.release()
cv2.destroAllWindows()