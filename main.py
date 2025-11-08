
import cv2

cv2.namedWindow("Camera")
cap = cv2.VideoCapture(0)  # 0 = webcam
if cap.isOpened():
    ret, frame = cap.read()
else :
    ret = False

while ret:
    cv2.imshow('Camera', frame)
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    key = cv2.waitKey(20)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
