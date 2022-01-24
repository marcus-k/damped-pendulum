"""
Damped pendulum in Python. Learning Matplotlib 
animations and SciPy ODE functions.

"""

import numpy as np
from numpy import sin, cos, pi, exp
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

# Constants
g = 9.81            # acceleration in m/s^2
l = 1               # pendulum length in m
m = 1               # pendulum mass in kg
drag = True         # is drag on?
drag_plot = False   # plot the exponential drag curve?
gamma = 0.1         # dampening coefficient
save = False        # Save animation to mp4
maxTime = 10        # Animation length

def derivs(state, t):
    # state : [th, w]
    
    dydx = np.zeros_like(state)
    dydx[0] = state[1]
    dydx[1] = -g / l * sin(state[0])
    # dydx[1] = -g / l * state[0]       # Small angle approximation

    if drag:
        dydx[1] -= 2 * gamma * l * state[1]

    return dydx

def main():
    # Initial conditions
    th = pi / 1.5
    w = 0

    # Define a time range
    dt = 0.01
    t = np.arange(0, maxTime, dt)

    # Integrate function
    out = integrate.odeint(derivs, [th, w], t)

    # Convert angular to Cartesian
    x =  l * sin(out[:, 0])
    y = -l * cos(out[:, 0])

    # Initialize plot 1
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.set_aspect("equal")
    ax1.grid()

    line, = ax1.plot([], [], "o-", lw=2, ms=10)
    time = ax1.text(0.05, 0.925, "", 
        transform=ax1.transAxes, bbox=dict(facecolor="red", alpha=0.5))
    # transAxes follows the window, not the grid plot, (0, 0) is bottom-left

    # Set plot bounds
    ax1.set_xlim([-2, 2])
    ax1.set_ylim([-2, 2])

    # Initialize plot 2
    ax2.set_xlim([0, 1])
    ax2.set_xticks([])          # Unfortunately, no easy way to animate ticks in matplotlib
    ax2.set_ylim([-pi, pi])

    ax2.set_xlabel(r"$t$")
    ax2.set_ylabel(r"$\theta$")

    graph_t = []
    graph_th = []
    line2, = ax2.plot([], [], "-")

    if drag and drag_plot:
        graph_d = []
        drag_curve = th * exp(-gamma * t)
        dline, = ax2.plot([], [], "r-")

    # Define the animation function
    def update(frame):
        # Get pendulum coordinates
        x_data = [0, x[frame]]
        y_data = [0, y[frame]]

        # Set new data on plot 1
        line.set_data(x_data, y_data)
        time.set_text(f"Time (s): {frame * dt:.2f}")

        # Set new data on plot 2
        graph_t.append(t[frame])
        graph_th.append(out[:, 0][frame])
        line2.set_data(graph_t, graph_th)

        if t[frame] > 1:
            ax2.set_xlim([0, t[frame]])

        # Plot drag if enabled
        if drag and drag_plot:
            graph_d.append(drag_curve[frame])
            dline.set_data(graph_t, graph_d)

        # Return altered artist objects (should ALWAYS return an iterable)
        if drag and drag_plot:
            return line, time, line2, dline
        else:
            return line, time, line2

    # Show animation
    ani = animation.FuncAnimation(
        fig, update, len(out), interval=dt*100, blit=True, repeat=False)

    if save:
        ani.save('./animations/animation.mp4', writer="ffmpeg", fps=60)

    # Create a reset button
    # def reset(event):
    #     ani.frame_seq = ani.new_frame_seq()
    #     graph_t = []
    #     graph_th = []
    #     line2.set_data([], [])
    #     plt.draw()

    # ax_reset = plt.axes([0.81, 0.05, 0.1, 0.075])
    # reset_button = Button(ax_reset, "Reset")
    # reset_button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    main()