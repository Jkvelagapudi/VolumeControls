import cv2
import math
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

(screen_width, screen_height) = pyautogui.size()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

pinch=False

# Define a function to count fingers
def countFingers(image, hand_landmarks, handNo=0):

	global pinch

	if hand_landmarks:
		
		landmarks = hand_landmarks[handNo].landmark

		       
		fingers = []

		for lm_index in tipIds:
			# Get Finger Tip and Bottom y Position Value
			finger_tip_y = landmarks[lm_index].y 
			finger_bottom_y = landmarks[lm_index - 2].y

			# Check if ANY FINGER is OPEN or CLOSED
			if lm_index !=4:
				if finger_tip_y < finger_bottom_y:
					fingers.append(1)


				if finger_tip_y > finger_bottom_y:
					fingers.append(0)

		totalFingers = fingers.count(1)

		# PINCH

		# Draw a LINE between FINGER TIP and THUMB TIP
		finger_tip_x = int((landmarks[8].x)*width)
		finger_tip_y = int((landmarks[8].y)*height)

		thumb_tip_x = int((landmarks[4].x)*width)
		thumb_tip_y = int((landmarks[4].y)*height)

		cv2.line(image, (finger_tip_x, finger_tip_y),(thumb_tip_x, thumb_tip_y),(255,0,0),2)

		
		center_x = int((finger_tip_x + thumb_tip_x )/2)
		center_y = int((finger_tip_y + thumb_tip_y )/2)

		cv2.circle(image, (center_x, center_y), 2, (0,0,255), 2)

		# Pythagorean Theoram
		# Who said we would never use this
		distance = math.sqrt(((finger_tip_x - thumb_tip_x)**2) + ((finger_tip_y - thumb_tip_y)**2))

		# print("Distance: ", distance)
		
		# print("Computer Screen Size :",screen_width, screen_height, "Output Window size: ", width, height)
		# print("Mouse Position: ", mouse.position, "Tips Line Centre Position: ", center_x, center_y)

		
		if totalFingers == 0:
			pyautogui.press('volumemute')
		if distance > 150:
			pyautogui.press('volumeup')
		if distance < 100:
			pyautogui.press('volumedown')
		


# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Darw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
	success, image = cap.read()
	
	image = cv2.flip(image, 1)

	
	results = hands.process(image)

	
	hand_landmarks = results.multi_hand_landmarks

	
	drawHandLanmarks(image, hand_landmarks)

	       
	countFingers(image, hand_landmarks)

	cv2.imshow("Media Controller", image)

	
	key = cv2.waitKey(1)
	if key == 27:
		break


cv2.destroyAllWindows()
