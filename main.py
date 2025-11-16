
import cv2
import mediapipe as mp
import numpy as np

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
            # thumb tip 
            x_thumb = hand_landmarks.landmark[thumb_tip].x
            y_thumb = hand_landmarks.landmark[thumb_tip].y
            z_thumb = hand_landmarks.landmark[thumb_tip].z

            # index tip 
            x_index_tip = hand_landmarks.landmark[index_finger_tip].x
            y_index_tip = hand_landmarks.landmark[index_finger_tip].y
            z_index_tip = hand_landmarks.landmark[index_finger_tip].z

            # middle tip 
            x_middle_tip = hand_landmarks.landmark[middle_finger_tip].x
            y_middle_tip = hand_landmarks.landmark[middle_finger_tip].y
            z_middle_tip = hand_landmarks.landmark[middle_finger_tip].z

            # ring tip 
            x_ring_tip = hand_landmarks.landmark[ring_finger_tip].x
            y_ring_tip = hand_landmarks.landmark[ring_finger_tip].y
            z_ring_tip = hand_landmarks.landmark[ring_finger_tip].z

            # pinky tip 
            x_pinky_tip = hand_landmarks.landmark[pinky_finger_tip].x
            y_pinky_tip = hand_landmarks.landmark[pinky_finger_tip].y
            z_pinky_tip = hand_landmarks.landmark[pinky_finger_tip].z

            # index mcp 
            x_index_mcp = hand_landmarks.landmark[index_finger_mcp].x
            y_index_mcp = hand_landmarks.landmark[index_finger_mcp].y
            z_index_mcp = hand_landmarks.landmark[index_finger_mcp].z

            # middle mcp 
            x_middle_mcp = hand_landmarks.landmark[middle_finger_mcp].x
            y_middle_mcp = hand_landmarks.landmark[middle_finger_mcp].y
            z_middle_mcp = hand_landmarks.landmark[middle_finger_mcp].z

            # ring mcp 
            x_ring_mcp = hand_landmarks.landmark[ring_finger_mcp].x
            y_ring_mcp = hand_landmarks.landmark[ring_finger_mcp].y
            z_ring_mcp = hand_landmarks.landmark[ring_finger_mcp].z

            # pinky mcp 
            x_pinky_mcp = hand_landmarks.landmark[pinky_finger_mcp].x
            y_pinky_mcp = hand_landmarks.landmark[pinky_finger_mcp].y
            z_pinky_mcp = hand_landmarks.landmark[pinky_finger_mcp].z

            if round(x_thumb,2) in [round(x_index_tip,2), round(x_index_tip+0.01,2), round(x_index_tip-0.01,2)]:
                print("écriture")
                
                # convert 0-1 coords in pixels coords
                height, width = image.shape[:2]
                x_pixel = int(x_thumb * width)
                y_pixel = int(y_thumb * height)
                cv2.circle(img=overlay, center=(x_pixel,y_pixel), radius=5, color=(255,0,0), thickness=-1)
            
            if round(x_index_tip,2) in [round(x_index_mcp,2), round(x_index_mcp+0.01,2), round(x_index_mcp-0.01,2)] and round(x_middle_tip,2) in [round(x_middle_mcp,2), round(x_middle_mcp+0.01,2), round(x_middle_mcp-0.01,2)]:
                print("effacer")

                # erase all points
                overlay = np.zeros_like(image, dtype=np.uint8)
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
