"""Explore Q4 antelope performance against several legal lion steering policies.

Run with: python test.py
Plots are saved outside the project under your system temporary directory.
These are hypothetical opponents, not predictions of other students' submissions.
"""

import math
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import challenge


OUTPUT_DIR = Path(tempfile.gettempdir()) / "mat292_challenge_tests"


def steer_toward(x, target, gain=1.0):
    """Turn the lion toward a target with the Q4 limit |JL| <= 1."""
    error = (target - x[2] + math.pi) % (2 * math.pi) - math.pi
    return float(np.clip(gain * error, -1, 1))


def pure_pursuit(t, x):
    """More aggressive than the assignment's unit-gain clip-wrap lion."""
    return steer_toward(x, math.atan2(x[4] - x[1], x[3] - x[0]), 4)


def lead_pursuit(t, x):
    """Aim at a constant-velocity interception point using current prey velocity."""
    dx, dy = x[3] - x[0], x[4] - x[1]
    speed_a = 1 / (1 + t * t)
    vx, vy = speed_a * math.cos(x[5]), speed_a * math.sin(x[5])
    # |relative position + prey velocity * tau| = lion speed * tau.
    b = dx * vx + dy * vy
    c = dx * dx + dy * dy
    tau = (b + math.sqrt(b * b + (challenge.vL**2 - speed_a**2) * c)) / (
        challenge.vL**2 - speed_a**2
    )
    return steer_toward(x, math.atan2(dy + vy * tau, dx + vx * tau), 4)


def proportional_navigation(t, x):
    """Turn using line-of-sight rotation, plus a small pursuit correction."""
    dx, dy = x[3] - x[0], x[4] - x[1]
    speed_a = 1 / (1 + t * t)
    rvx = speed_a * math.cos(x[5]) - challenge.vL * math.cos(x[2])
    rvy = speed_a * math.sin(x[5]) - challenge.vL * math.sin(x[2])
    los_rate = (dx * rvy - dy * rvx) / max(dx * dx + dy * dy, 0.05**2)
    error = (math.atan2(dy, dx) - x[2] + math.pi) % (2 * math.pi) - math.pi
    return float(np.clip(3 * los_rate + 0.5 * error, -1, 1))


def straight_lion(t, x):
    return 0.0


def left_turn_lion(t, x):
    return 1.0


def right_turn_lion(t, x):
    return -1.0


OPPONENTS = {
    "Benchmark (clip-wrap)": challenge.JL_bench,
    "Fast pure pursuit": pure_pursuit,
    "Lead interception": lead_pursuit,
    "Proportional navigation": proportional_navigation,
    "Straight heading": straight_lion,
    "Always turn left": left_turn_lion,
    "Always turn right": right_turn_lion,
}


def capture_time(solution):
    return float(solution.t_events[0][0]) if len(solution.t_events[0]) else None


def sampled_states(solution):
    times = np.linspace(0, solution.t[-1], 500)
    return times, solution.sol(times)


def plot_results(results, reference):
    # Every opponent gets its own trajectory panel, including the benchmark.
    fig, axes = plt.subplots(3, 3, figsize=(15, 13), constrained_layout=True)
    for ax, (name, solution) in zip(axes.flat, results.items()):
        _, states = sampled_states(solution)
        ax.plot(states[0], states[1], color="#db682a", label="Lion")
        ax.plot(states[3], states[4], color="#d72d79", label="Your antelope")
        ax.scatter([states[0, 0], states[3, 0]], [states[1, 0], states[4, 0]],
                   c=["#db682a", "#d72d79"], marker="o", s=22)
        ax.scatter([states[0, -1], states[3, -1]],
                   [states[1, -1], states[4, -1]],
                   c=["#db682a", "#d72d79"], marker="x", s=45)
        caught = capture_time(solution)
        ax.set_title(f"{name}\n" + (f"Captured: {caught:.3f}" if caught is not None
                                       else "Not captured by 10"))
        ax.set_aspect("equal", adjustable="datalim")
        ax.grid(alpha=0.2)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    for ax in list(axes.flat)[len(results):]:
        ax.set_visible(False)
    axes.flat[0].legend(loc="best", fontsize=8)
    fig.suptitle("Q4: your antelope against hypothetical lion strategies", fontsize=16)
    fig.savefig(OUTPUT_DIR / "trajectories.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5), constrained_layout=True)
    names = list(results)
    scores = [capture_time(sol) or challenge.Tmax for sol in results.values()]
    reference_time = capture_time(reference)
    ax.barh(names, scores, color=["#4477aa" if i == 0 else "#d72d79"
                                  for i in range(len(names))])
    if reference_time is not None:
        ax.axvline(reference_time, color="black", linestyle="--",
                   label=f"Benchmark antelope vs benchmark lion: {reference_time:.3f}")
    for i, (score, solution) in enumerate(zip(scores, results.values())):
        text = f"{score:.3f}" if capture_time(solution) is not None else "10+ (no capture)"
        ax.text(score + 0.05, i, text, va="center", fontsize=9)
    ax.set_xlim(0, challenge.Tmax + 2.3)
    ax.invert_yaxis()
    ax.set_xlabel("Survival score (higher is better; capped at 10)")
    ax.set_title("Capture times against each lion")
    ax.legend(loc="lower right")
    ax.grid(axis="x", alpha=0.2)
    fig.savefig(OUTPUT_DIR / "scores.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 6), constrained_layout=True)
    for name, solution in results.items():
        times, states = sampled_states(solution)
        distance = np.hypot(states[3] - states[0], states[4] - states[1])
        ax.plot(times, distance, label=name)
    ax.axhline(challenge.r_collision, color="black", linestyle="--",
               label="Capture radius")
    ax.set(xlabel="Time", ylabel="Lion–antelope separation",
           title="Separation until capture or t = 10", xlim=(0, challenge.Tmax))
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    fig.savefig(OUTPUT_DIR / "separation.png", dpi=150)
    plt.close(fig)


def main():
    if challenge.TEAM != "antelope":
        raise ValueError("This experiment expects TEAM = 'antelope'.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    reference = challenge.simulator(challenge.JL_bench, challenge.JA_bench)
    results = {}
    for name, lion in OPPONENTS.items():
        solution = challenge.simulator(lion, challenge.J_strategy)
        results[name] = solution
        caught = capture_time(solution)
        print(f"{name:25s}: " + (f"captured at {caught:.6f}" if caught is not None
                                    else f"no capture by {challenge.Tmax:g}"))
    baseline = capture_time(reference)
    print("Benchmark vs benchmark: " + (f"captured at {baseline:.6f}" if baseline is not None
                                          else f"no capture by {challenge.Tmax:g}"))
    plot_results(results, reference)
    print(f"Plots: {OUTPUT_DIR / 'trajectories.png'}")
    print(f"       {OUTPUT_DIR / 'scores.png'}")
    print(f"       {OUTPUT_DIR / 'separation.png'}")


if __name__ == "__main__":
    main()
