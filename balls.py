import cv2
import numpy as np

def clear(h,w):

	img = np.ones([h,w,3])

	img[:,:,0] *= 64/255.0
	img[:,:,1] *= 128/255.0
	img[:,:,2] *= 192/255.0

	return img

radius = 50
color = (192,128,64)
thickness = -1
delay = 1

vel = np.array([0,0])
pos = np.array([500,500])

for i in range(100000):
	t = i*0.03

	img = clear(1000, 1000)

	circle_x, circle_y = int(500 + 200*np.sin(t*5)), int(500 + 200*np.cos(t*3))
	cv2.circle(img, (circle_x, circle_y), radius, color, thickness)

	cv2.imshow("Gray", img)
	code = cv2.waitKeyEx(delay)
	# print(code)
	if code == ord('q'):
		cv2.destroyAllWindows()
		break

cv2.destroyAllWindows()