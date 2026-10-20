"""Make placeholder figure images that describe what each figure will show."""

import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

MM = 1 / 25.4
FIGURES = {
    "overview": {
        "size": (178 * MM, 91 * MM),  # full text width; the teaser draft is 2000 x 1025 px
        "title": "Fig. 1 teaser (full width, 178 x 91 mm)",
        "body": (
            "(a) Perception: monocular video -> event detection (timeline of one stitch, hold window) "
            "and keypoints + needle mask on the frames of the window. "
            "(b) Measurement: Needle Hold Ratio (3D arc, cost over s), Needle Hold Angle (3D angle per frame, median), "
            "Depth of Needle Hold (longest-jaw frame, depth per frame). "
            "(c) Scoring: each value on the EASE scale with its score."
        ),
    },
}


def main(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, fig_def in FIGURES.items():
        w, h = fig_def["size"]
        fig = plt.figure(figsize=(w, h))
        ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor("#eeeeee")
        ax.text(0.5, 0.85, fig_def["title"], ha="center", va="center", fontsize=9, weight="bold")
        wrapped = textwrap.fill(fig_def["body"], width=int(w * 14))
        ax.text(0.5, 0.42, wrapped, ha="center", va="center", fontsize=8)
        fig.savefig(out_dir / f"{name}_placeholder.png", dpi=200)
        plt.close(fig)


if __name__ == "__main__":
    main(sys.argv[1])
