# Uncomment the next two lines if you want to save the animation
#import matplotlib
#matplotlib.use("Agg")

import numpy
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation



# Sent for figure
font = {'size'   : 16}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0 = figure(num = 0, figsize = (35, 16))#, dpi = 100)
f0.suptitle("Oscillation decay", fontsize=12)
ax01 = subplot2grid((1, 2), (0, 0))
ax02 = subplot2grid((1, 2), (0, 1))
#tight_layout()

# Set titles of subplots
ax01.set_title('Actual Map')
ax02.set_title('Generated Map')

# set y-limits
ax01.set_xlim(0,50)
ax01.set_ylim(0,50)

# sex x-limits
ax02.set_xlim(0,50)
ax02.set_ylim(0,50)

# Turn on grids
ax01.grid(True)
ax02.grid(True)

# set label names
ax01.set_xlabel("x")
ax01.set_ylabel("py")
ax02.set_xlabel("t")
ax02.set_ylabel("vy")


# Data Placeholders

t=zeros(0)

# set plots
p011, = ax01.plot([],[],'b-', label="yp1")
p012, = ax01.plot([],[],'g-', label="yp2")

p021, = ax02.plot([],[],'b-', label="yv1")
p022, = ax02.plot([],[],'g-', label="yv2")

# set lagends
ax01.legend([p011,p012], [p011.get_label(),p012.get_label()])
ax02.legend([p021,p022], [p021.get_label(),p022.get_label()])

# Data Update
xmin = 0.0
xmax = 5.0
x = 0.0

def update_map(self):
	global x, real_map, est_map, ax01, ax02

	global t

	real_map = np.array([	[10,10],[12,10],[12,12],[14,12],
							[14,14],[16,10],[18,10],[18,14],
							[20,14],[22,14],[22,8],[24,10],
							[24,12],[26,14],[28,10],[30,8],
							[32,8]])
	real_x = real_map[:,0]
	real_y = real_map[:,1]

	reversed_y = real_y[::-1]

	final_x = np.hstack((real_x-10, real_x+12))
	final_y = np.hstack((real_y, reversed_y))

	g = np.arange(-17, 51, 2.0)

	idx = np.argwhere(np.diff(np.sign(final_y - g))).flatten()

	t=append(t,x)

	x += 0.1

	p011.set_data(final_x, final_y)
	p012.set_data(g, g)
	ax01.plot(g[idx], final_y[idx], 'ro')
	# p012.set_data(real_x+12, real_y)

	# p021.set_data(t,yv1)
	# p022.set_data(t,yv2)



	return p011, p012, p021, p022

# interval: draw new frame every 'interval' ms
# frames: number of frames to draw
simulation = animation.FuncAnimation(f0, update_map, blit=False, frames=2000, interval=1, repeat=False)

# Uncomment the next line if you want to save the animation
#simulation.save(filename='sim.mp4',fps=30,dpi=300)

plt.show()
