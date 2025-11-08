
import cv2
import mediapipe as mp

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

if cap.isOpened():
    ret, frame = cap.read()
else :
    ret = False

while ret:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) # flip camera to mirror
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # colors conversion

    image.flags.writeable = False
    
    points = hands.process(image) # hands points
    
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw hand landmarks
    if points.multi_hand_landmarks:
        thumb_tip = 4
        index_finger_tip = 8
        
    
        for hand_landmarks in points.multi_hand_landmarks: # hand_landmarks contains 21 coords (x,y,z)
            # thumb tip 
            x_thumb = hand_landmarks.landmark[thumb_tip].x
            y_thumb = hand_landmarks.landmark[thumb_tip].y
            z_thumb = hand_landmarks.landmark[thumb_tip].z

            # index tip 
            x_index = hand_landmarks.landmark[index_finger_tip].x
            y_index = hand_landmarks.landmark[index_finger_tip].y
            z_index = hand_landmarks.landmark[index_finger_tip].z

            # print(f"thumb {x_thumb,y_thumb,z_thumb} index {x_index, y_index, z_index}")
            # print(f"x : {x_thumb, x_index}")
            # print(f"x : {round(x_thumb,2), round(x_index,2)}")
            # print(f"y : {y_thumb, y_index}")
            # print(f"z : {z_thumb, z_index}")
            # print()
            # print(round(x_thumb,2) ,round(x_index,2), round(x_index+0.01,2), round(x_index-0.01,2))
            if round(x_thumb,2) in [round(x_index,2), round(x_index+0.01,2), round(x_index-0.01,2)]:
                print("proche")
            
            
           
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
    cv2.imshow('Camera', image)
    key = cv2.waitKey(20)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
