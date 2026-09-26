"""Q4 starter: complete J_strategy(t, x) below.

TEAM is "lion" or "antelope" based on your student ID.
JL_bench and JA_bench are the benchmark controls described in the assignment.

Completeness grade
    To receive the completeness credit, your strategy needs to pass the
    benchmark for your assigned team. The local simulator takes the lion steering
    function first and the antelope steering function second:

        lion_benchmark = simulator(J_strategy, JA_bench)
        antelope_benchmark = simulator(JL_bench, J_strategy)

Competition
    The competition evaluator imports TEAM and J_strategy from this file. It
    then uses its own simulator compare your strategy against all the other
    submitted strategies.

    The competition score is capture time, or Tmax when there is no capture.
    Winning the competition has no effect on your grade.
"""
import numpy as np
from scipy.integrate import solve_ivp
from q1 import lion_ante_rhs # reuse your rhs function from Question 1
from q2 import J_cw_lion, J_cw_ante # reuse steering functions from Question 2
from q3 import collision_event as q3_collision_event, r_collision as q3_r_collision # reuse collision detection from Question 3
import utils


TEAM = "" # Enter "lion" or "antelope". This is based on your student ID, see assignment PDF.
TEAMNAME = "" # Enter a nickname for your team. The leaderboard will show this nickname, not your real name(s).
max_step    = 0.0005
Tmax        = 10
x0          = [0, 0, np.pi / 6, 2.25, 0, 0]
vL          = 2
r_collision = 0.05

JL_bench = J_cw_lion
JA_bench = J_cw_ante

if TEAM not in ("lion", "antelope"):
    raise ValueError('TEAM must be "lion" or "antelope"')

def lion_ante_rhs_variable_speed(t, x, vL, vA, JL, JA):
    """Reuse the previous lion_ante_rhs function, but with variable speed"""
    return lion_ante_rhs(t, x, vL(t), vA(t), JL, JA)

def collision_event(t, x):
    """Reuse the Q3 event function with the challenge capture radius."""
    return q3_collision_event(t, x) + q3_r_collision - r_collision

collision_event.terminal = True

def J_strategy(t, x):
    """Your strategy must be a valid steering rate, implement it here.

    As usual, the inputs are:
        x = [xL, yL, phiL, xA, yA, phiA], with angles in radians
        t = time,
    Remember to obey the steering constraints from the assignment instructions.
    """
    # YOUR CODE HERE
    raise NotImplementedError()

def simulator(JL, JA):
    """simulate until capture or Tmax"""
    solution = solve_ivp(
        lambda t, x: lion_ante_rhs_variable_speed(
            t, x, vL=lambda t: vL, vA=lambda t: 1 / (1 + t**2), JL=JL, JA=JA
        ),
        (0, Tmax), x0, events=collision_event, max_step=max_step,
        dense_output=True, rtol=1e-8, atol=1e-10,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution

if __name__ == "__main__":

    solution_benchmark = simulator(JL_bench, JA_bench)

    if TEAM == "lion":
        solution_your_strategy = simulator(J_strategy, JA_bench)
    else:
        solution_your_strategy = simulator(JL_bench, J_strategy)
    
    if len(solution_benchmark.t_events[0]) > 0:
        survival_time_benchmark = solution_benchmark.t_events[0][0]
        print("Benchmark: Antelope caught at t = {:.6f}".format(survival_time_benchmark))
    else:
        survival_time_benchmark = None
        print("Benchmark: No capture by t = {:g}; survival time exceeds this horizon.".format(
            solution_benchmark.t[-1]
        ))

    if len(solution_your_strategy.t_events[0]) > 0:
        survival_time_your_strategy = solution_your_strategy.t_events[0][0]
        print("Your strategy: Antelope caught at t = {:.6f}".format(survival_time_your_strategy))
    else:
        survival_time_your_strategy = None
        print("Your strategy: No capture by t = {:g}; survival time exceeds this horizon.".format(
            solution_your_strategy.t[-1]
        ))

    score_benchmark = Tmax if survival_time_benchmark is None else survival_time_benchmark
    score_your_strategy = Tmax if survival_time_your_strategy is None else survival_time_your_strategy

    if TEAM == "lion":
        if score_benchmark <= score_your_strategy:
            print("Your lion performs worse or the same as the benchmark lion")
        else:
            print("Your lion performs better than the benchmark lion")
    else:
        if score_benchmark >= score_your_strategy:
            print("Your antelope performs worse or the same as the benchmark antelope")
        else:
            print("Your antelope performs better than the benchmark antelope")
                
    utils.plot_trajectories(solution_benchmark, "challenge_benchmark_plot.png")

    utils.plot_trajectories(solution_your_strategy, "challenge_your_strategy_plot.png")
