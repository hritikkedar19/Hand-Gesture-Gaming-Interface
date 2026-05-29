import cv2 as cv
import mediapipe as mp
from pynput.keyboard import Key, Controller

# Initialize Keyboard Controller
keyboard = Controller()

# Initialize MediaPipe Hand Tracking
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
hands = mp_hand.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# The 4 main finger tip IDs to check open/closed states
fingerTipIds = [8, 12, 16, 20]

# Capture Video
video = cv.VideoCapture(0)

# Track the exact state of the physical keys to prevent stuttering
gas_pressed = False
brake_pressed = False
current_input = "RELEASED"

print("Starting Hill Climb FULL SPEED Gesture Controller...")

while True:
    success, image = video.read()
    if not success:
        continue

    # Mirror the image horizontally
    image = cv.flip(image, 1)
    h, w, c = image.shape

    # Convert to RGB for MediaPipe processing
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    landmarks_list = []

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[-1]

        # Extract coordinates of all joints
        for index, lm in enumerate(hand_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            landmarks_list.append([index, cx, cy])

        # Draw lines over your hand skeleton
        mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)

    # Process driving states if a hand is detected
    if len(landmarks_list) != 0:
        fingers_open = []

        # Check if Index, Middle, Ring, and Pinky fingers are extended upward
        for tipId in fingerTipIds:
            if landmarks_list[tipId][2] < landmarks_list[tipId - 2][2]:
                fingers_open.append(1)  # Finger is open
            else:
                fingers_open.append(0)  # Finger is curled down

        count_fingers = fingers_open.count(1)

        # --- CONTROLLER DRIVING LOGIC (FIXED FOR MAXIMUM GAS SPEED) ---
        
        # If 3 or more fingers are up -> FLOOD THE GAS PEDAL
        if count_fingers >= 3:
            current_input = "MAX SPEED GAS"
            if brake_pressed:
                keyboard.release(Key.left)
                brake_pressed = False
            if not gas_pressed:
                keyboard.press(Key.right)  # Holds the key down perfectly flat
                gas_pressed = True

        # If 1 or fewer fingers are up -> HARD BRAKE
        elif count_fingers <= 1:
            current_input = "HARD BRAKE"
            if gas_pressed:
                keyboard.release(Key.right)
                gas_pressed = False
            if not brake_pressed:
                keyboard.press(Key.left)  # Holds the brake down perfectly flat
                brake_pressed = True
        
        # Coasting Zone (2 fingers up)
        else:
            current_input = "COASTING"
            if gas_pressed:
                keyboard.release(Key.right)
                gas_pressed = False
            if brake_pressed:
                keyboard.release(Key.left)
                brake_pressed = False
            
    else:
        # Safety fallback: if hand drops, release everything instantly
        current_input = "RELEASED"
        if gas_pressed:
            keyboard.release(Key.right)
            gas_pressed = False
        if brake_pressed:
            keyboard.release(Key.left)
            brake_pressed = False

    # Display HUD status overlay directly on the screen
    cv.rectangle(image, (10, 15), (420, 75), (0, 0, 0), cv.FILLED)
    cv.putText(image, f"CONTROL: {current_input}", (20, 55), 
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show video layout window
    cv.imshow("Hill Climb Gestures", image)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up keys on exit
keyboard.release(Key.left)
keyboard.release(Key.right)
video.release()
cv.destroyAllWindows()