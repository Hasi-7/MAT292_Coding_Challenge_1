import matplotlib.pyplot as plt


def plot_trajectories(solution, filename=None):
    """Plot the lion and antelope paths, fading earlier times.

    Takes a solve_ivp solution and returns fig, ax.
    If filename is given, also save the plot and close its window.
    """
    # get the positions
    t  = solution.t
    xL = solution.y[0]
    yL = solution.y[1]
    xA = solution.y[3]
    yA = solution.y[4]

    colorL = "#EE7733"
    colorA = "#EE3377"
    fig, ax = plt.subplots()

    # plot the paths
    # Flat caps keep adjacent segments from overlapping and hiding the fade.
    for i in range(len(t)-1):
        alpha = 0.2 + 0.8*(t[i]-t[0])/(t[-1]-t[0])
        ax.plot(xL[i:i+2], yL[i:i+2], color=colorL, alpha=alpha,
                linewidth=2.5, solid_capstyle="butt")
        ax.plot(xA[i:i+2], yA[i:i+2], color=colorA, alpha=alpha,
                linewidth=2.5, solid_capstyle="butt")

    # mark the endpoints
    ax.scatter(xL[0], yL[0], color=colorL, edgecolor="black", marker="o", zorder=3)
    ax.scatter(xA[0], yA[0], color=colorA, edgecolor="black", marker="o", zorder=3)
    ax.scatter(xL[-1], yL[-1], color=colorL, marker="x", s=70, linewidths=2, zorder=4)
    ax.scatter(xA[-1], yA[-1], color=colorA, marker="x", s=70, linewidths=2, zorder=4)

    # label the plot
    ax.plot([], [], color=colorL, linewidth=2.5, label="Lion")
    ax.plot([], [], color=colorA, linewidth=2.5, label="Antelope")
    ax.plot([], [], color="black", marker="o", linestyle="none", label="Start")
    ax.plot([], [], color="black", marker="x", linestyle="none", label="End")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x position")
    ax.set_ylabel("y position")
    ax.set_title("Lion-antelope trajectories\nLighter paths indicate earlier times")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    fig.tight_layout()

    # save the plot
    if filename is not None:
        fig.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close(fig)

    return fig, ax
