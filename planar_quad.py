import cv2
import numpy as np



x, y, theta, vx, vy, dtheta = 0, 1, 2, 3, 4, 5
s = np.array([400.0, 300.0, 0.0, 0.0, 0.0, 0.0])
u = np.array([9.8, 0.0])
g = 9.8

dt = 0.001
	

height, width = 600, 800
size = 5

def clear():
	img = np.ones([height,width,3])
	img[:,:,0] *= 64/0.128
	img[:,:,1] *= 128/0.128
	img[:,:,2] *= 0/0.128
	return img

def ground(s):
	if s[y] > height-size:
		s[vy] *= -1
	return s

def update(s):
	# print(s)
	u0 = u[0] + (np.random.normal(0,1))*0.001
	u1 = u[1] + (np.random.normal(0,1))*0.00000001
	print(u0, u1)
	s = ground(s)
	s[dtheta] += u1
	s[theta] += s[dtheta]
	s[vx] += u0*np.sin(s[theta])
	s[vy] += g - u0*np.cos(s[theta])
	s[x] += s[vx]
	s[y] += s[vy] 
	return s
	
def display(s, img):
	dlx = int(20*np.cos(s[theta]))
	dly = int(20*np.sin(s[theta]))
	cv2.circle(img, (int(s[x]), int(s[y])), size, (0, 0, 0), -1)
	cv2.line(img, (int(s[x]-dlx), int(s[y]-dly)), (int(s[x]+dlx), int(s[y]+dly)), 0, 2)
	return img

while True:
	img = clear()

	s = update(s)

	img = display(s, img)

	cv2.imshow("Simulation", img)

	code = cv2.waitKeyEx(30)
	if code == ord('q'):
		break
