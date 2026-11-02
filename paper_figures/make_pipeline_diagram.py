import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family": "serif", "font.size": 6.3})
for f in ["Liberation Serif", "Times New Roman"]:
    from matplotlib import font_manager
    if any(f == x.name for x in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = f; break
fig, ax = plt.subplots(figsize=(3.45, 1.75)); ax.set_xlim(0, 100); ax.set_ylim(0, 52); ax.axis("off")
INK, BLUE, GREY, ORANGE = "#0b0b0b", "#2a78d6", "#f1f0ed", "#eb6834"
def box(x, y, w, h, t, fc=GREY, ec=INK, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.2", fc=fc, ec=ec, lw=0.7))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=6.2, weight="bold" if bold else "normal", color=INK)
def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=6, lw=0.7, color=INK))
box(1, 33, 17, 13, "Reference\nsignature")
box(1, 5, 17, 13, "Questioned\nsignature")
box(26, 33, 24, 13, "CNN encoder\n(shared weights)", fc="#dbe8f8", ec=BLUE)
box(26, 5, 24, 13, "CNN encoder\n(shared weights)", fc="#dbe8f8", ec=BLUE)
box(57, 33, 16, 13, "Embedding\n(128-d)")
box(57, 5, 16, 13, "Embedding\n(128-d)")
box(80, 19, 19, 14, "Distance d\n(Euclidean)", fc="#fde6dc", ec=ORANGE)
box(78, 1, 22, 11, "d ≤ τ: accept\nd > τ: reject", bold=True)
for y in (39.5, 11.5):
    arrow(18.4, y, 25.6, y); arrow(50.4, y, 56.6, y)
arrow(73.4, 39.5, 85, 33.4); arrow(73.4, 11.5, 85, 18.6)
arrow(89.5, 18.6, 89.5, 12.4)
ax.plot([38, 38], [19, 32], ls=":", color=BLUE, lw=0.8); ax.text(39.2, 25.5, "same\nweights", fontsize=5.6, color=BLUE, va="center")
fig.savefig("fig0_pipeline.png", dpi=300, bbox_inches="tight", facecolor="white")
