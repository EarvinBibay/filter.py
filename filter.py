import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)
process_this_frame =True
src1 = cv2.imread("mask.png")
src2 = cv2.imread("png.png")
src3 = cv2.imread("png1.png")

mask = [src1,src2,src3]
x = 0

while True:
	ret,frame = video_capture.read()
	small_frame = cv2.resize(frame, (0,0), fx = 0.25, fy = 0.25 )
	img = small_frame[:,:,::-1]
	if process_this_frame:
		face_locations = face_recognition.face_locations(img)
		face_landmarks = face_recognition.face_landmarks(img)
		if face_landmarks != []:		
			d_land = face_landmarks[0]
			#get lower boundary			
			bridge = d_land["nose_bridge"]
			bot = bridge[3]
			y_bot = bot[1]
			#get upper boundary
			brow_l = d_land["left_eyebrow"]
			top = brow_l[4]
			y_top = top[1]
		else:
			print("SWITCH!")
	process_this_frame = not process_this_frame

	for (top, right, bottom, left) in face_locations:
		top = y_top*4
		right *= 4
		bottom = y_bot*4
		left *= 4

		w = right - left
		h = bottom - top


	if mask[x] is not None:
		mask[x] = cv2.resize(mask[x], (w,h))	
	else:
		print("image not loaded")
	
	w, h, c = mask[x].shape
	
	if face_landmarks != []:
		for i in range(0, w):
			for j in range(0, h):
				if mask[x][i, j][2] != 0:
					frame[top + i, left + j] = mask[x][i, j]
	else:
		
		if x<2:
			x+=1
		else:
			x=0
	
	cv2.imshow('Video', frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_capture.release()
cv2.destroyAllWindows()

	
