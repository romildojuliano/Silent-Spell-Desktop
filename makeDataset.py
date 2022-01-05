import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
import numpy as np
import os
import string
import time


cap = cv2.VideoCapture(0)#'videos/1.mp4')

mpDraw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.2, min_tracking_confidence=0.5,max_num_hands=1)



# Path for exported data, numpy arrays
DATA_PATH = os.path.join('MP_Data') 

# Actions that we try to detect
actions = np.array(list(string.ascii_uppercase))
for action in actions:
    try:
        os.mkdir(os.path.join(DATA_PATH,action))
    except:
        pass

start = time.time()
# Thirty videos worth of data
no_sequences = 30

# Videos are going to be 30 frames in length
sequence_length = 30

# Folder start
#start_folder = 30

for action in actions: 
    try:
        dirmax = np.max(np.array(os.listdir(os.path.join(DATA_PATH, action))).astype(int))
    except:
        dirmax = 0
    for sequence in range(0,no_sequences+1):
        try: 
            os.makedirs(os.path.join(DATA_PATH, action, str(dirmax+sequence)))
        except:
            pass

start_folder = dirmax

for action in actions:
    # Loop through sequences aka videos
    for sequence in range(start_folder, start_folder+no_sequences):
        # Loop through video length aka sequence length
        for frame_num in range(sequence_length):

            # Read feed
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(
                        img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Draw landmarks
            #draw_styled_landmarks(imgRGB, results)
            
            # NEW Apply wait logic
            if frame_num == 0: 
                cv2.putText(img, 'STARTING COLLECTION', (120,200), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
                cv2.putText(img, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15,12), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                # Show to screen
                cv2.imshow('OpenCV Feed', img)
                cv2.waitKey(500)
            else: 
                cv2.putText(img, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15,12), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                # Show to screen
                cv2.imshow('OpenCV Feed', img)
            
            # NEW Export keypoints
            keypoints = np.array([[res.x, res.y, res.z] for res in results.multi_hand_landmarks[0].landmark]).flatten() if results.multi_hand_landmarks else np.zeros(21*3)
            npy_path = os.path.join(DATA_PATH, action, str(sequence), str(frame_num))
            np.save(npy_path, keypoints)

            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
print(time.time()-start)
cap.release()
cv2.destroyAllWindows()

    
