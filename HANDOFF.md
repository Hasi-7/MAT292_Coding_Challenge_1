# MAT292 challenge testing handoff

## Goal

Help evaluate successive antelope strategies for MAT292 Coding Challenge 1. The student edits `challenge.py` themselves. After each change, run the existing `test.py`, explain the results, and show the updated plots.

## Project and assignment

- Project directory: `C:\Personal\VSCode\MAT292_Coding_Challenge_1` (Windows).
- Read `cc1.pdf` for the rules, especially Q4, and `submission-guideline.txt` for submission requirements.
- `challenge.simulator(JL, JA)` uses the Q4 setup: lion speed 2, antelope speed `1 / (1 + t**2)`, initial state `[0, 0, pi/6, 2.25, 0, 0]`, capture radius 0.05, and horizon `Tmax = 10`. Lion steering is limited to ±1 and antelope steering to ±2.
- The student's submitted function is `challenge.J_strategy(t, x)`; `TEAM` is `"antelope"`.
- The submission guideline says not to use AI to generate assignment solutions. Help with testing, interpretation, and visualization rather than writing the submitted antelope strategy.

## Testing workflow

1. Read the **current** `J_strategy` before each run. The user changes it between messages; don't assume it is the version from the previous run.
2. From the project directory, run `.\.venv\Scripts\python.exe -B test.py`. The harness calls `challenge.simulator` against benchmark clip-wrap, fast pure pursuit, lead interception, proportional navigation, straight-heading, constant-left-turn, and constant-right-turn lions. It also runs benchmark antelope versus benchmark lion.
3. Compare the three pursuing opponents' capture times with the **best-so-far complete strategy**, not merely the previous run. Higher survival time is better. Use their three-time average as the working comparison metric; also state whether the benchmark lion captures the antelope by `t = 10`.
4. Link the regenerated plots:
   - [Trajectories](file:///C:/Users/Admin/AppData/Local/Temp/mat292_challenge_tests/trajectories.png)
   - [Capture-time scores](file:///C:/Users/Admin/AppData/Local/Temp/mat292_challenge_tests/scores.png)
   - [Separation over time](file:///C:/Users/Admin/AppData/Local/Temp/mat292_challenge_tests/separation.png)

The figures are written under `C:\Users\Admin\AppData\Local\Temp\mat292_challenge_tests\`, outside the project. Do not edit `challenge.py` or other existing project files when simply rerunning tests. Edit `test.py` only if the user requests a change to the testing harness.

## Best-so-far reference

The original antelope strategy aimed along the line from lion to antelope, using clip-wrap steering with the ±2 limit and no angle offset. Its verified results were:

| Lion opponent | Capture time |
| --- | ---: |
| Fast pure pursuit | 1.648347 |
| Lead interception | 1.652058 |
| Proportional navigation | 1.650852 |
| **Mean of these three** | **1.650419** |

The benchmark lion did not catch the original strategy by `t = 10`. As a reference, benchmark antelope versus benchmark lion was captured at `1.569669`. The original remains the best-so-far strategy **by the three-opponent average**; a later version did better against fast pure pursuit alone but worse on average.

## Last tested version

At the last run, the student added `+pi/4` to the antelope's target angle when lion heading `x[2] <= 0`, and `-pi/4` when `x[2] > 0`. The results were:

| Lion opponent | Last tested | Difference from best-so-far |
| --- | ---: | ---: |
| Fast pure pursuit | 1.649172 | +0.000825 |
| Lead interception | 1.643873 | -0.008185 |
| Proportional navigation | 1.643629 | -0.007223 |
| **Mean of these three** | **1.645558** | **-0.004861** |

The benchmark lion did not catch this version by `t = 10`. The student may have changed `challenge.py` again since this run, so inspect it before using these numbers as the current result.

## Pitfall from earlier runs

During earlier iterations, `challenge.py` changed between tests, leading to apparently inconsistent capture times for what looked like the original strategy. A direct rerun with the original steering formula reproduced the original three times exactly. Never label a result as a controlled before-and-after comparison unless the tested versions are identified accurately.
