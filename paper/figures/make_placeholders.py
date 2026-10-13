"""Make placeholder figure images that describe what each figure will show."""

import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIGURES = {
    "overview": {
        "size": (3.4, 2.0),
        "title": "Fig. overview (1 column, ~5 cm)",
        "body": (
            "Timeline of one stitch: previous withdrawal end -> repositions -> "
            "last reposition end -> entry. Reposition window R_i and hold window W_i "
            "marked. Per-frame keypoints/mask in W_i -> geometric quantities "
            "(ratio s_i, angle, depth) -> EASE rules -> scores."
        ),
    },
    "evidence": {
        "size": (7.0, 2.8),
        "title": "Fig. evidence cards (full width, 7-8 cm)",
        "body": (
            "3-4 stitches: a correct one, a near-threshold error, a keypoint error. "
            "Each card: the frame used, keypoints, fitted arc, the value on a scale "
            "with EASE thresholds, our score vs the label."
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
