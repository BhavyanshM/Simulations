import cv2
import numpy as np
import time
import keyboard as keys

class Quad():
	def __init__(self):
		self.radius = 20
		self.thickness = -1
		self.color = (192,128,64)
		self.reset()

	def reset(self):
		self.position = np.array([500.0,980.0])
		self.velocity = np.array([-5.0,-5.0])
		self.accel = np.array([0.1,0])
		self.reward = 0
		self.passed = [0,0,0,0]

	def update(self):
		self.velocity += self.accel
		self.position += self.velocity

class Track2D():
	def __init__(self, delay=0.05, time_scale=15):
		self.dim = (1000, 1000)
		self.quad = Quad()
		self.delay = time_scale
		self.time_scale = delay
		self.gates = [	(200, 200),
						(600, 400), 
						(800, 600), 
						(600, 800)]

	def clear(self):
		img = np.ones([self.dim[0],self.dim[1],3])
		img[:,:,0] *= 64/255.0
		img[:,:,1] *= 128/255.0
		img[:,:,2] *= 192/255.0
		return img

	def terminate(self):
		pos, r = self.quad.position, self.quad.radius
		if pos[0] + r > 1000 or pos[0] - r < 0 or pos[1] - r < 0 or pos[1] + r > 1000:
			return True

	def evaluate(self):
		for g in range(len(self.gates)):
			if self.quad.passed[g] == 0:
				norm = np.linalg.norm(self.quad.position - np.asarray(self.gates[g]))
				if  norm < 5:
					self.quad.passed[g] = 1
					print('Passed:', g, norm, self.quad.position)
					return 100
		return -1

	def display(self):
		img = self.clear()
		pos = self.quad.position
		cv2.circle(img, (int(pos[0]), int(pos[1])), self.quad.radius, self.quad.color, self.quad.thickness)
		for g in range(len(self.gates)):
			color = (255,255,255)
			if self.quad.passed[g] == 1:
				color = (0,128,255)
			cv2.line(img, (self.gates[g][0] - 20, self.gates[g][1]), (self.gates[g][0] + 20, self.gates[g][1]), color, 4)
			# cv2.line(img, (0, self.gates[g][1]), (1000, self.gates[g][1]), (0,0,0), 2)
		cv2.imshow("Gray", img)
		return cv2.waitKeyEx(self.delay)

	def act(self, action):
		self.quad.accel

	def loop(self):
		i = 0
		while True:
			i += 1
			t = i*self.time_scale

			self.quad.update()
			
			self.quad.reward += self.evaluate()

			if self.terminate():
				self.quad.reset()

			code = self.display()
			# print(code)
			if code == ord('q'):
				cv2.destroyAllWindows()
				break



track = Track2D(0.02,10)
track.loop()
