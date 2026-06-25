import cv2 as cv
import mediapipe as mp
from pynput.keyboard import Key, Controller


keyboard = Controller()


mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
hands = mp_hand.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

fingerTipIds = [8, 12, 16, 20]


video = cv.VideoCapture(0)


gas_pressed = False
brake_pressed = False
current_input = "RELEASED"

print("Starting Hill Climb FULL SPEED Gesture Controller...")

while True:
    success, image = video.read()
    if not success:
        continue

    
    image = cv.flip(image, 1)
    h, w, c = image.shape

    
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    landmarks_list = []

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[-1]

       
        for index, lm in enumerate(hand_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            landmarks_list.append([index, cx, cy])

        mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)

    
    if len(landmarks_list) != 0:
        fingers_open = []

        
        for tipId in fingerTipIds:
            if landmarks_list[tipId][2] < landmarks_list[tipId - 2][2]:
                fingers_open.append(1) 
            else:
                fingers_open.append(0)  

        count_fingers = fingers_open.count(1)

        
        if count_fingers >= 3:
            current_input = "MAX SPEED GAS"
            if brake_pressed:
                keyboard.release(Key.left)
                brake_pressed = False
            if not gas_pressed:
                keyboard.press(Key.right) 
                gas_pressed = True

       
        elif count_fingers <= 1:
            current_input = "HARD BRAKE"
            if gas_pressed:
                keyboard.release(Key.right)
                gas_pressed = False
            if not brake_pressed:
                keyboard.press(Key.left) 
                brake_pressed = True
        
       
        else:
            current_input = "COASTING"
            if gas_pressed:
                keyboard.release(Key.right)
                gas_pressed = False
            if brake_pressed:
                keyboard.release(Key.left)
                brake_pressed = False
            
    else:
        
        current_input = "RELEASED"
        if gas_pressed:
            keyboard.release(Key.right)
            gas_pressed = False
        if brake_pressed:
            keyboard.release(Key.left)
            brake_pressed = False

    
    cv.rectangle(image, (10, 15), (420, 75), (0, 0, 0), cv.FILLED)
    cv.putText(image, f"CONTROL: {current_input}", (20, 55), 
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

   
    cv.imshow("Hill Climb Gestures", image)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


keyboard.release(Key.left)
keyboard.release(Key.right)
video.release()
cv.destroyAllWindows()
