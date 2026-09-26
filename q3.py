# Complete the unfinished functions. You may add supporting code; keep signatures.
import numpy as np
from scipy.integrate import solve_ivp

from q1 import lion_ante_rhs # reuse your rhs function from Question 1
from q2 import J_cw_lion, J_cw_ante # reuse parameters from Question 2
import utils


# Q2 steering and agility, with a faster lion and slower antelope.
vL   = 2
vA   = 0.75
Tmax = 6

# Start 2.25 units apart on y = 0. The antelope runs upward;
# the lion initially heads diagonally toward its path.
x0 = [0.75, 0, np.pi/4, 3, 0, np.pi/2]

# Resolve the collision region without tightening solver tolerances.
r_collision = 0.05
max_step = 0.0005


# Question 3(a)
def collision_event(t,x):
    """Return separation minus the capture radius."""
    # YOUR CODE HERE
    raise NotImplementedError()
    
collision_event.terminal  = True


# Question 3(b)
if __name__ == "__main__":

    # solve_ivp stops at the decreasing zero crossing of collision_event
    solution = solve_ivp(
        lambda t, x: lion_ante_rhs(t, x, vL, vA, J_cw_lion, J_cw_ante),
        [0, Tmax], x0, events=collision_event,
        max_step=max_step
    )
    if not solution.success:
        raise RuntimeError(solution.message)

    if len(solution.t_events[0]) > 0:
        survival_time = solution.t_events[0][0]
        print("Antelope caught at t = {:.6f}".format(survival_time))
    else:
        survival_time = None
        print("No capture by t = {:g}; survival time exceeds this horizon.".format(
            solution.t[-1]
        ))

    utils.plot_trajectories(solution, "q3_plot.png")
