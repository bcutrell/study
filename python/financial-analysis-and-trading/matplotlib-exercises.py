

import matplotlib.pyplot as plt
# %matplotlib inline

# Data
import numpy as np
x = np.arange(0,100)
y = x*2
z = x**2



# Exercise 1
# Follow along with these steps:

# Create a figure object called fig using plt.figure()
# Use add_axes to add an axis to the figure canvas at [0,0,1,1]. Call this new axis ax.
# Plot (x,y) on that axes and set the labels and titles to match the plot below:

# Exercise 2
# Create a figure object and put two axes on it, ax1 and ax2. Located at [0,0,1,1] and [0.2,0.5,.2,.2] respectively.

# Now plot (x,y) on both axes. And call your figure object to show it.


# Exercise 3
# Create the plot below by adding two axes to a figure object at [0,0,1,1] and [0.2,0.5,.4,.4]


# Now use x,y, and z arrays to recreate the plot below. Notice the xlimits and y limits on the inserted plot:


# Exercise 4
# Use plt.subplots(nrows=1, ncols=2) to create the plot below.

# Now plot (x,y) and (x,z) on the axes. Play around with the linewidth and style

# See if you can resize the plot by adding the figsize() argument in plt.subplots() are copying and pasting your previous code.







exit()

# NOTES
x = np.linspace(0,5,11)
y = x ** 2

# Functional
plt.plot(x,y)
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('Title')

plt.subplot(1,2,1)
plt.plot(x,y, 'r')
plt.subplot(1,2,2)
plt.plot(y,x,'b')

# OO
fig = plt.figure()
# left, bottom, width, height
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
axes.plot(x,y)
axes.set_xlabel('X Label')
axes.set_ylabel('Y Label')
axes.set_title('Title')

fig = plt.figure()
axes1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
axes1.plot(x,y)
axes2 = fig.add_axes([0.2, 0.5, 0.4, 0.3])
axes2.plot(x,y)
plt.show()

fig, axes = plt.subplots(nrows=1,ncols=2)
for current_ax in axes:
    current_ax.plot(x,y)
axes[0].plot(x,y)
axes[0].set_title('First Plot')
axes[1].set_title('Second Plot')
plt.tight_layout() # saves space

# Figure Size and DPI
fig.plt.figure(figsize=(3,2), dpi=100)
ax = fig.add_axes([0,0,1,1])
ax.plot(x,y)

fig.savefig('my_picture.png') #jpg, pdf, etc.

fig = plt.figure()
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# plot multiple lines
ax.plot(x,y, label='X')
ax.plot(y,x, label='Y')
ax.lengend(loc=0) # finds 'best' location

# Colors + Line Types
ax.plot(x,y, color="purple", linewidth=3, alpha=0.5, linestyle='--', marker='*', markersize=10) # alpha changes transparency
ax.set_xlim([0,1]) # upper and lower bounds
ax.set_ylim([0,1])
