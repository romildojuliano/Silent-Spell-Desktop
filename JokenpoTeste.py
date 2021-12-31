import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
from joblib import load
import math
import numpy as np

def subLandmarks(v1,v2):
    return [v1.x-v2.x,v1.y-v2.y,v1.z-v2.z]

def angle(s,c,e):
    Js = subLandmarks(s,c)
    #Jc = subLandmarks(c,c)
    Je = subLandmarks(e,c)
    return math.acos(np.inner(Js,Je)/(math.sqrt(np.inner(Js,Js))*math.sqrt(np.inner(Je,Je))))

# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.2, min_tracking_confidence=0.5,max_num_hands=1)
cap = cv2.VideoCapture(0)

model = load('silentSpellPrototipo.joblib') 

while cap.isOpened():
  success, image = cap.read()
  if not success:
    print("Ignoring empty camera frame.")
    # If loading a video, use 'break' instead of 'continue'.
    continue

  # Flip the image horizontally for a later selfie-view display, and convert
  # the BGR image to RGB.
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  image.flags.writeable = False
  results = hands.process(image)

  # Draw the hand annotations on the image.
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  if results.multi_hand_landmarks:
    points = []
    trincas = [[0,1,2],
               [1,2,3],
               [2,3,4],
               [5,6,7],
               [6,7,8],
               [9,10,11],
               [10,11,12],
               [13,14,15],
               [14,15,16],
               [17,18,19],
               [18,19,20],
               [8,0,20],
               [12,0,20],
               [4,0,16],
               [16,0,20]]
    landmarks = list(results.multi_hand_landmarks[0].landmark)
    for trinca in trincas:
        a = angle(landmarks[trinca[0]],landmarks[trinca[1]],landmarks[trinca[2]])
        points.append(a)
    print(model.predict([points]))
    for hand_landmarks in results.multi_hand_landmarks:
      mp_drawing.draw_landmarks(
          image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
  cv2.imshow('MediaPipe Hands', image)
  if cv2.waitKey(5) & 0xFF == 27:
    break
hands.close()
cap.release()