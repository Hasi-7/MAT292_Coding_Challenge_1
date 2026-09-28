# Complete the unfinished functions. You may add supporting code; keep signatures.
import numpy as np
from scipy.integrate import solve_ivp

import utils

# Question 1(a)
def JL(t,x):
    """Return the lion's turning rate.

    The state x is unused but is included so that this function
    can be passed to lion_ante_rhs.
    """
    return -t
    raise NotImplementedError()


def JA(t,x):
    """Return the antelope's turning rate 1.
    """
    return 1
    raise NotImplementedError()

# Question 1(b)
def lion_ante_rhs(t,x,vL,vA,JL,JA):
    """Return the derivatives of the lion-antelope state.

    The state is x = [xL,yL,phiL,xA,yA,phiA], where each animal
    has a position and orientation. Orientation is measured in radians.
    The speeds vL and vA are constant. The steering functions
    JL(t,x) and JA(t,x) give the rates of change of the headings.

    Return dx = [dxL,dyL,dphiL,dxA,dyA,dphiA].
    """
    
    return [vL*np.cos(JL(t, x)*t), vL*np.sin(JL(t, x)*t), JL(t, x), vA*np.cos(JA(t, x)*t), vA*np.sin(JA(t, x)*t), JA(t, x)]
    raise NotImplementedError()

if __name__ == "__main__":
    vL    = 2
    vA    = 1
    x0    = [0, 0, np.pi/2, 1, 0, -np.pi/2]
    times = np.linspace(0, 5, 5000)

    solution = solve_ivp(
        lambda t, x: lion_ante_rhs(t, x, vL, vA, JL, JA),
        [times[0], times[-1]], x0, t_eval=times, rtol=1e-8, atol=1e-10
    )
    if not solution.success:
        raise RuntimeError(solution.message)

    x_final = solution.y[:, -1]
    print("Lion position at t = 5: x = {:.6f}, y = {:.6f}".format(
        x_final[0], x_final[1]
    ))

    print("Antelope position at t = 5: x = {:.6f}, y = {:.6f}".format(
        x_final[3], x_final[4]
    ))

    utils.plot_trajectories(solution, "q1_plot.png")
