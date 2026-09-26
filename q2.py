# Complete the unfinished functions. You may add supporting code; keep signatures.
import numpy as np
from scipy.integrate import solve_ivp

from q1 import lion_ante_rhs # reuse your rhs function from Question 1
import utils


# Turning limits (radians/time).
JLmax = 1
JAmax = 2
# Initial state: [xL, yL, phiL, xA, yA, phiA], angles in radians.
x0    = [0, 0, 0, 3, 0, np.pi/2]

# Values specified in Question 2.
vL    = 1.5
vA    = 1
Tmax  = 6

# Numerical settings: sample count controls the plot, not solver accuracy.
times = np.linspace(0, Tmax, 1000)
rtol  = 1e-8
atol  = 1e-10


# Question 2(a)
def J_cw_lion(t,x):
    """Turn the lion toward the antelope using clip-wrap steering.
    JLmax the maximum turning rate is defined globally in this file, so it can
    be accessed without passing it as an input.
    """
    # YOUR CODE HERE
    raise NotImplementedError()


# Question 2(b)
def J_cw_ante(t,x):
    """Use clip-wrap steering to turn the antelope counter-clockwise
    perpendicular to vector from lion to antelope."""
    # YOUR CODE HERE
    raise NotImplementedError()

# Question 2(c)
if __name__ == "__main__":
    solution = solve_ivp(
        lambda t, x: lion_ante_rhs(t, x, vL, vA, J_cw_lion, J_cw_ante),
        [0, Tmax], x0, t_eval=times, rtol=rtol, atol=atol
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    x_final = solution.y[:, -1]
    print("Lion position at t = {:g}: x = {:.6f}, y = {:.6f}".format(
        solution.t[-1], x_final[0], x_final[1]
    ))
    print("Antelope position at t = {:g}: x = {:.6f}, y = {:.6f}".format(
        solution.t[-1], x_final[3], x_final[4]
    ))

    utils.plot_trajectories(solution, "q2_plot.png")
