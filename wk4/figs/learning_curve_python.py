"""Python version of the "learning curves" joke chart (R vs. SAS/SPSS/Minitab), xkcd style."""
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("learning_curve_python")
PY_BLUE, PY_YELLOW = "#3776AB", "#FFD43B"


def stick(ax, x, y, s=0.35, angle=0, arms="up", lw=1.6, mirror=False):
    """Draws a stick figure with its feet at (x, y), rotated by angle (degrees)."""
    a = math.radians(angle)
    def P(px, py):  # local -> data coordinates
        px = -px if mirror else px
        return x + s * (px * math.cos(a) - py * math.sin(a)), y + s * (px * math.sin(a) + py * math.cos(a))
    def seg(p, q):
        (x1, y1), (x2, y2) = P(*p), P(*q)
        ax.plot([x1, x2], [y1, y2], color="black", lw=lw, solid_capstyle="round", zorder=5)
    seg((0, 1.0), (0, 2.0))                         # body
    seg((0, 1.0), (-0.35, 0)); seg((0, 1.0), (0.35, 0))   # legs
    if arms == "up":
        seg((0, 1.7), (-0.45, 2.4)); seg((0, 1.7), (0.45, 2.4))
    elif arms == "climb":
        seg((0, 1.7), (0.45, 2.3)); seg((0, 1.7), (0.5, 1.6))
    else:  # flailing
        seg((0, 1.7), (-0.55, 1.4)); seg((0, 1.7), (0.55, 2.2))
    hx, hy = P(0, 2.3)
    ax.add_patch(Circle((hx, hy), 0.3 * s, fill=False, lw=lw, zorder=5))


def main():
    with plt.xkcd(scale=1.2, length=120, randomness=2):
        plt.rcParams["font.family"] = ["Comic Sans MS", "Chalkboard", "DejaVu Sans"]
        fig, ax = plt.subplots(figsize=(10, 7.5))

        # --- the boring, safe options
        xs = [0, 1.5, 3, 4.5, 6, 7.5, 9, 10]
        ax.plot(xs, [0.75, 0.9, 1.15, 1.55, 1.85, 2.05, 2.25, 2.35], color="#d62728", lw=2.5)  # Minitab
        ax.plot(xs, [0.3, 0.4, 0.75, 1.75, 2.45, 2.85, 3.1, 3.2], color="#2ca02c", lw=2.5)     # SAS
        ax.plot(xs, [0.15, 0.25, 0.55, 1.35, 2.1, 2.55, 2.75, 2.8], color="#7b7bd6", lw=2.5)    # SPSS

        # --- the Python cliff (with an overhang, as in the original)
        cliff = [(0, 3.0), (0.8, 3.3), (1.6, 3.7), (2.2, 4.3), (2.7, 5.3), (3.0, 6.6), (3.05, 7.8),
                 (3.0, 8.5), (2.85, 8.85), (2.6, 9.05), (2.5, 9.25), (2.8, 9.3), (3.5, 9.25),
                 (5.5, 9.35), (7.5, 9.3), (10, 9.4)]
        ax.plot(*zip(*cliff), color="black", lw=2.5)

        # hurdles on the way up
        hurdles = [((0.35, 3.13), 'print("Hello world!")', (0.25, 2.2)),
                   ((2.15, 4.25), "Object Types", (3.45, 3.75)),
                   ((2.45, 4.75), "Operators", (3.55, 4.4)),
                   ((2.7, 5.3), "Loops", (3.6, 5.05)),
                   ((2.88, 5.9), "IndentationError", (3.65, 5.7)),
                   ((3.0, 6.6), "List Comprehension", (3.7, 6.35)),
                   ((3.05, 7.4), "Functions", (3.75, 7.0)),
                   ((3.0, 8.45), "Object Orientation", (3.75, 7.75))]
        for (px, py), label, (tx, ty) in hurdles:
            ax.annotate(label, xy=(px, py), xytext=(tx, ty), fontsize=12,
                        arrowprops=dict(arrowstyle="->", lw=1.2, color="0.25"))

        # climbers, fallers, and the lucky ones at the top
        stick(ax, 2.47, 4.8, s=0.3, angle=-10, arms="climb", mirror=True)   # climbing the slope
        stick(ax, 3.12, 6.75, s=0.3, angle=0, arms="climb", mirror=True)    # hanging on the wall
        stick(ax, 2.05, 6.6, s=0.3, angle=150, arms="flail")                # falling ...
        stick(ax, 1.25, 5.0, s=0.3, angle=200, arms="flail")
        stick(ax, 0.95, 3.52, s=0.3, angle=-95, arms="flail")               # ... and landed
        stick(ax, 4.6, 9.3, s=0.33, arms="up")
        stick(ax, 6.2, 9.32, s=0.33, arms="up")

        # the train of productivity
        tx = 7.4
        for i, w in enumerate((0.75, 0.55, 0.55)):
            x0 = tx + sum((0.75, 0.55, 0.55)[:i]) + 0.08 * i
            ax.add_patch(Rectangle((x0, 9.45), w, 0.35, fill=False, lw=1.5, zorder=5))
            for wx in (x0 + 0.15, x0 + w - 0.15):
                ax.add_patch(Circle((wx, 9.42), 0.07, fill=False, lw=1.3, zorder=5))
        ax.plot([tx + 0.15, tx + 0.15], [9.8, 10.05], color="black", lw=1.5)  # chimney
        ax.text(tx + 0.45, 10.25, "pip install everything", fontsize=11, ha="left")
        ax.text(4.0, 8.65, "automate, scrape, analyse, ...", fontsize=12, color=PY_BLUE)

        ax.set_xlim(0, 10); ax.set_ylim(0, 10.8)
        ax.set_xticks([]); ax.set_yticks([])
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.set_xlabel("Time spent", fontsize=16)
        ax.set_ylabel("Skill", fontsize=16)

        # legend squares, like the original
        handles = [Rectangle((0, 0), 1, 1, color=c) for c in ("#d62728", "#2ca02c", "#7b7bd6", "black")]
        ax.legend(handles, ["Minitab", "SAS", "SPSS", "Python"], loc="upper center",
                  bbox_to_anchor=(0.5, -0.09), ncol=4, frameon=False, fontsize=14)
        fig.tight_layout()
        for ext in ("png", "pdf"):
            fig.savefig(OUT.with_suffix("." + ext), dpi=200, bbox_inches="tight")
    print("wrote", OUT.with_suffix(".png"), OUT.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
