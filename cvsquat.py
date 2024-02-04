import cv2 
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#Function to find angle between 3 points
def calculate_angle(a,b,c):
    a = np.array(a)
    b = np.array(b) #Vertex
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if(angle >180.0):
        angle = 360-angle
        
    return angle 

squatcounter = 0
squatstage = None

#Setting up video feed and MediaPipe
cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Convert image to RGB for processing
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        results = pose.process(image)
    
        # Convert back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            leftankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            leftknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            lefthip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            leftshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            lefttoe = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x

            rightankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            rightknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            righthip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            rightshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            righttoe = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x
            
            # Calculate angles
            leftlegangle = calculate_angle(leftankle, leftknee, lefthip)
            rightlegangle = calculate_angle(rightankle, rightknee, righthip)
            backangle = calculate_angle(leftankle, lefthip, leftshoulder)
            

            # Visualize angles, green color if within 10% of perfect form, else red
            if(abs(leftlegangle-90) < (90/100)*10):
                llcolor = (0, 255, 0)
            else:
                llcolor = (0, 0, 255)

            if(abs(rightlegangle-90) < (90/100)*10):
                rlcolor = (0, 255, 0)
            else:
                rlcolor = (0, 0, 255)
            
            if(abs(backangle-160) < (90/100)*10):
                bcolor = (0, 255, 0)
            else:
                bcolor = (0, 0, 255)

            #Displaying angle values in real time (green if within 10% of perfect form)
            cv2.putText(image, str(int(leftlegangle)), tuple(np.multiply(leftknee, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, llcolor, 2, cv2.LINE_AA)
                       
            cv2.putText(image, str(int(rightlegangle)), tuple(np.multiply(rightknee, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, rlcolor, 2, cv2.LINE_AA)
            
            cv2.putText(image, str(int(backangle)), tuple(np.multiply(righthip, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, bcolor, 2, cv2.LINE_AA)
            
            #Are the knees past the toes? (that's bad)
            centerline = int(image.shape[1])/2
            kneespasttoes = abs(leftknee[0]-centerline) < abs(lefttoe-centerline) and abs(rightknee[0]-centerline) < abs(righttoe-centerline)  
            if(kneespasttoes):
                #Right status box
                cv2.rectangle(image, (int((3*image.shape[1])/4),0), (int(image.shape[1]),int(image.shape[0]/8)), (0,0,0), -1)
                cv2.putText(image, "KEEP KNEES BEHIND TOES", (int((3*image.shape[1])/4),int((image.shape[0])/20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

            # Squat counter
            if(leftlegangle<120 and rightlegangle<135):
                stage = "down"
            if(leftlegangle>150 and rightlegangle>150 and stage =='down'):
                stage="up"
                squatcounter +=1
                print(squatcounter)
        
        except:
            pass
        
        #Left status box (for reps)
        cv2.rectangle(image, (0,0), (int(image.shape[1]/4),int(image.shape[0]/8)), (0,0,0), -1)
        cv2.putText(image, f'REPS: {squatcounter}', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()