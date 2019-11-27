from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import sys
import cv2
import numpy as np
plt.style.use('seaborn-pastel')
np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})

x, y, theta, vx, vy, dtheta = 0, 1, 2, 3, 4, 5
height, width = 600, 800
size = 5
g = 9.8		

class PID():
	def __init__(self, target):
		self.prev = 0
		self.ep = 0
		self.ei = 0
		self.ed = 0
		self.etot = 0
		self.kp = 0.0
		self.ki = 0.0
		self.kd = 0.0
		self.target = target

	def control_update(self, current):
		self.ep = current - self.target
		self.ei += self.ep
		self.ed = self.ep - self.prev
		self.prev = self.ep
		self.etot = self.kp*self.ep + self.ki*self.ei + self.kd*self.ed

	def update_kp(self, val):
		self.kp = val
	def update_ki(self, val):
		self.ki = val
	def update_kd(self, val):
		self.kd = val
	def update_target(self, val):
		self.target = val

class Quad2D():
	def __init__(self, pid):
		self.s = np.array([400.0, 300.0, 0.0, 0.0, 0.0, 0.0])
		self.u = np.array([9.8, 0.0])
		self.y_pid = pid


	def clear(self):
		img = np.ones([height,width,3])
		img[:,:,0] *= 64/0.128
		img[:,:,1] *= 128/0.128
		img[:,:,2] *= 0/0.128
		return img

	def ground(self):
		if self.s[y] > height-size:
			self.s[vy] *= -1

	def clip_theta(self):
		lim = 0.2
		if self.s[theta] > lim:
			self.s[theta] = lim
		if self.s[theta] < -lim:
			self.s[theta] = -lim

	def dynamic_update(self, dt, du):
		self.u[0] = self.u[0]*0.9 + 0.1*du
		u0 = self.u[0] + (np.random.normal(0,1))*0.001
		u1 = self.u[1] + (np.random.normal(0,1))*0.00000001
		# print(u0, u1)
		# self.ground()
		self.s[dtheta] += u1*dt
		self.s[theta] += self.s[dtheta]*dt
		self.clip_theta()
		self.s[vx] += u0*np.sin(self.s[theta])*dt
		self.s[vy] += (g - u0*np.cos(self.s[theta]))*dt
		self.s[x] += self.s[vx]*dt
		self.s[y] += self.s[vy] *dt
		
	def display(self, img):
		dlx = int(20*np.cos(self.s[theta]))
		dly = int(20*np.sin(self.s[theta]))
		cv2.circle(img, (int(self.s[x]), int(self.s[y])), size, (0, 0, 0), -1)
		cv2.line(img, (int(self.s[x]-dlx), int(self.s[y]-dly)), (int(self.s[x]+dlx), int(self.s[y]+dly)), 0, 2)
		cv2.line(img, (0, int(self.y_pid.target)), (width, int(self.y_pid.target)), 0, 1)
		cv2.namedWindow("Simulation", cv2.WINDOW_NORMAL)
		cv2.resizeWindow("Simulation", width*2, height*2)
		cv2.imshow("Simulation", img)





def init():
	return tuple(lines)


def animate(i):
	global Q, yline

	img = Q.clear()

	Q.y_pid.control_update(Q.s[1])
	Q.dynamic_update(0.2, Q.y_pid.etot)
	Q.display(img)

	print(Q.y_pid.kp, "\t", Q.y_pid.ki, "\t", Q.y_pid.kd)

	t = np.linspace(0,4, duration)
	yline[i] = -Q.s[1]*0.001
	lines[0].set_data(t, yline)

	ytarget = -np.ones(duration)*Q.y_pid.target*0.001
	lines[1].set_data(t,ytarget)

	code = cv2.waitKeyEx(10)
	if code == ord('q'):
		sys.exit()

	return tuple(lines)


if __name__ == '__main__':
	Q = Quad2D(PID(200))
	duration = 1000
	yline = np.zeros(duration)


	pidkp = plt.axes([0.25, 0.1, 0.65, 0.1])
	skp = Slider(pidkp, 'Kp', 0.0, 1.0, valinit=Q.y_pid.kp)
	skp.label.set_size(30)
	skp.on_changed(Q.y_pid.update_kp)

	pidki = plt.axes([0.25, 0.3, 0.65, 0.1])
	ski = Slider(pidki, 'Ki', 0.0, 0.1, valinit=Q.y_pid.ki)
	ski.label.set_size(30)
	ski.on_changed(Q.y_pid.update_ki)
	
	pidkd = plt.axes([0.25, 0.5, 0.65, 0.1])
	skd = Slider(pidkd, 'Kd', 0.0, 30.0, valinit=Q.y_pid.kd)
	skd.label.set_size(30)
	skd.on_changed(Q.y_pid.update_kd)

	pidtarget = plt.axes([0.25, 0.7, 0.65, 0.1])
	starget = Slider(pidtarget, 'Target', 0.0, height, valinit=Q.y_pid.target)
	starget.label.set_size(30)
	starget.on_changed(Q.y_pid.update_target)

	fig = plt.figure(figsize=(35,15))
	ax = plt.axes(xlim=(0, 4), ylim=(-2, 2))
	lines = []
	n_lines = 4
	for i in range(n_lines):
		line_i, = ax.plot([], [], lw=3)
		lines.append(line_i)

	anim = FuncAnimation(fig, animate, init_func=init,
                               frames=duration, interval=10, blit=True)

	plt.show()


