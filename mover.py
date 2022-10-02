import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(1)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
old_index_x = 0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for landmark_number, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if landmark_number == 8:
                    cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 0))
                    index_y = screen_height / frame_height * y
                    new_index_x = screen_width / frame_width * x
                    moved = new_index_x - old_index_x
                    if new_index_x > old_index_x and moved > 15:
                        pyautogui.press('right')
                    elif new_index_x < old_index_x and moved < -15:
                        pyautogui.press('left')
                    else:
                        continue
                    old_index_x = new_index_x
                if landmark_number == 4:
                    cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 0))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    if abs(index_y - thumb_y) < 20:
                        print("Sleep!")
                        time.sleep(3)
                        print("Wake!")
                    
    cv2.imshow('Mover', frame)
    cv2.waitKey(1)
