import cv2
import numpy as np
 

cap = cv2.VideoCapture(0)
if (not cap.isOpened()):
   print("Error in opening")
while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    cv2.imshow('Home',frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
  else: 
    break

cap.release()
cv2.destroyAllWindows()