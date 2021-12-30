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

def apllyMediaPipe(cap,hands,model):
    image = None
    choosenLetter = None
    if(cap.isOpened()):
        success, image = cap.read()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            points = []
            trincas = [[0,1,2],[1,2,3],[2,3,4],[5,6,7],[6,7,8],[9,10,11],[10,11,12],[13,14,15],[14,15,16],[17,18,19],[18,19,20],[8,0,20],[12,0,20],[4,0,16],[16,0,20]]
            landmarks = list(results.multi_hand_landmarks[0].landmark)
            for trinca in trincas:
                a = angle(landmarks[trinca[0]],landmarks[trinca[1]],landmarks[trinca[2]])
                points.append(a)
            choosenLetter = model.predict([points])[0]
            
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image=np.rot90(image)
    
    return image, choosenLetter