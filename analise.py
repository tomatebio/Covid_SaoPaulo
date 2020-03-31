import numpy as np
import matplotlib.pyplot as plt




data = np.loadtxt(open("results/alpha1.csv", "rb"), delimiter=",") #, skiprows=1)

x=range(100)
# Note that even in the OO-style, we use `.pyplot.figure` to create the figure.
fig, ax = plt.subplots()  # Create a figure and an axes.
ax.plot(x, data[:,0], label='Suscetivel')  # Plot some data on the axes.
ax.plot(x, data[:,1], label='Infectado')  # Plot more data on the axes...
ax.plot(x, data[:,2], label='Recuperado')  # ... and some more.
ax.set_xlabel('tempo')  # Add an x-label to the axes.
ax.set_ylabel('Populacao')  # Add a y-label to the axes.
ax.set_title("Evolucao alpha=0.1")  # Add a title to the axes.
ax.legend()  # Add a legend.

plt.savefig("results/alpha1", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait',  format="png",
        transparent=False, bbox_inches=None, pad_inches=0.1 )




