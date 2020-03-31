
import numpy as np
import matplotlib.pyplot as plt


data02 = np.loadtxt(open("results/alpha02.csv", "rb"), delimiter=",") #, skiprows=1)
data03 = np.loadtxt(open("results/alpha03.csv", "rb"), delimiter=",") #, skiprows=1)
data05 = np.loadtxt(open("results/alpha05.csv", "rb"), delimiter=",") #, skiprows=1)
data09 = np.loadtxt(open("results/alpha09.csv", "rb"), delimiter=",") #, skiprows=1)
data1 = np.loadtxt(open("results/alpha1.csv", "rb"), delimiter=",") #, skiprows=1)

x=range(100)
# Note that even in the OO-style, we use `.pyplot.figure` to create the figure.
fig, ax = plt.subplots()  # Create a figure and an axes.

ax.plot(x, data1[:,1], label='Sem restrição')
ax.plot(x, data09[:,1], label='90% livre')
ax.plot(x, data05[:,1], label='50% livre')
ax.plot(x, data03[:,1], label='30% livre')
ax.plot(x, data02[:,1], label='20% livre')



ax.set_xlabel('Tempo')  # Add an x-label to the axes.
ax.set_ylabel('População')  # Add a y-label to the axes.
ax.set_title("Curva de infecção X Restrição no transporte ")  # Add a title to the axes.
ax.legend()  # Add a legend.




plt.savefig("results/ImpactoNostransportes", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait',  format="png",
        transparent=False, bbox_inches=None, pad_inches=0.1 )