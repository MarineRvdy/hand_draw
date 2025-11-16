
import cv2
import mediapipe as mp
import numpy as np
import random as rd

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands # deetect an follow hands
mp_drawing = mp.solutions.drawing_utils # drawn landmarks

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


cv2.namedWindow("Camera")
cap = cv2.VideoCapture(0)  # 0 = webcam

overlay = None
pen_color = (255,0,0)

def euclidean_dist(pts1,pts2):
    p1 = np.array([pts1.x,pts1.y,pts1.z])
    p2 = np.array([pts2.x, pts2.y, pts2.z])
    return np.linalg.norm(p1 - p2)

if cap.isOpened():
    ret, frame = cap.read()
else :
    ret = False

while ret:
    ret, frame = cap.read()
    old_image = None
    frame = cv2.flip(frame, 1) # flip camera to mirror
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # colors conversion

    image.flags.writeable = False
    
    points = hands.process(image) # hands points
    
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if overlay is None:
        overlay = np.zeros_like(image, dtype=np.uint8)

    height, width = image.shape[:2]

    # Draw hand landmarks
    if points.multi_hand_landmarks:
        # tip finger
        thumb_tip = 4
        index_finger_tip = 8
        middle_finger_tip = 12
        ring_finger_tip = 16
        pinky_finger_tip = 20
        
        # mcp finger
        index_finger_mcp = 5
        middle_finger_mcp = 9
        ring_finger_mcp = 13
        pinky_finger_mcp = 17
               
    
        for hand_landmarks in points.multi_hand_landmarks: # hand_landmarks contains 21 coords (x,y,z)
            landmarks = hand_landmarks.landmark
            
            # recover (x,y,z)
            thumb = landmarks[thumb_tip]
            index_tip = landmarks[index_finger_tip]
            middle_tip = landmarks[middle_finger_tip]
            ring_tip = landmarks[ring_finger_tip]
            pinky_tip = landmarks[pinky_finger_tip]
            index_mcp = landmarks[index_finger_mcp]
            middle_mcp = landmarks[middle_finger_mcp]
            ring_mcp = landmarks[ring_finger_mcp]
            pinky_mcp = landmarks[pinky_finger_mcp]

            # write (index_tip near thumb)
            if euclidean_dist(thumb, index_tip) < 0.07:
                print("write")
                
                # convert 0-1 coords in pixels coords
                x_pixel = int(index_tip.x * width)
                y_pixel = int(index_tip.y * height)


                cv2.circle(img=overlay, center=(x_pixel,y_pixel),radius=5, color=pen_color, thickness=-1)

            # erase (tip near mcp)
            if euclidean_dist(index_mcp, index_tip) < 0.09 and euclidean_dist(middle_mcp, middle_tip) < 0.09 and euclidean_dist(ring_mcp, ring_tip) < 0.09 and euclidean_dist(pinky_mcp, pinky_tip) < 0.09:
                print("erase")

                # erase all points
                overlay = np.zeros_like(image, dtype=np.uint8)

            # change color (middle near thul)
            if euclidean_dist(thumb, middle_tip) < 0.07:
                print("change color")

                pen_color = (rd.randint(0,255),rd.randint(0,255),rd.randint(0,255))


            # mp_drawing.draw_landmarks(
            #     image,
            #     hand_landmarks,
            #     mp_hands.HAND_CONNECTIONS
            # )
    combined = cv2.addWeighted(image, 1, overlay, 1, 0)
    cv2.imshow('Camera', combined)
    
    key = cv2.waitKey(20)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
