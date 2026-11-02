"""Merge result CSVs -> data.json + figures. Usage: python make_assets.py run1.csv [run2.csv ...]"""
import sys, json
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

df = pd.concat([pd.read_csv(f) for f in sys.argv[1:]], ignore_index=True)
df = df.drop_duplicates(["variant", "train", "loss", "seed", "test", "condition"])
M = ["EER", "AUC", "FAR", "FRR", "acc_fixed", "acc_best", "threshold"]
g = df.groupby(["variant", "train", "test", "condition", "loss"])
out = {}
for key, sub in g:
    out["|".join(key)] = {m: [float(sub[m].mean()), float(sub[m].std(ddof=0)) if len(sub) > 1 else 0.0] for m in M}
    out["|".join(key)]["n"] = int(sub["seed"].nunique())
json.dump(out, open("data.json", "w"), indent=1)
print("combos:", len(out), "seeds per run:", sorted(df.groupby(["variant", "train", "loss"])["seed"].nunique().unique()))

plt.rcParams.update({"font.family": "serif", "font.size": 7, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": 0.6, "figure.dpi": 300})
for f in ["Liberation Serif", "Times New Roman", "DejaVu Serif"]:
    if any(f == x.name for x in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = f; break
BLUE, ORANGE, AQUA, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e"
NAMES = {"cedar": "CEDAR", "hindi": "Hindi", "bengali": "Bengali"}
ORDER = ["cedar", "hindi", "bengali"]
b = df[df.variant == "baseline"]
mean = lambda **k: b[np.logical_and.reduce([b[c] == v for c, v in k.items()])][["EER", "FAR", "FRR", "AUC", "acc_fixed", "acc_best"]].mean()

# Fig 1: EER heat map, two panels
fig, axes = plt.subplots(1, 2, figsize=(3.45, 1.75))
for ax, loss in zip(axes, ["contrastive", "triplet"]):
    mat = np.array([[mean(train=tr, test=te, condition="clean", loss=loss).EER for te in ORDER] for tr in ORDER])
    im = ax.imshow(mat, cmap="viridis_r", vmin=0, vmax=0.4)
    ax.set_xticks(range(3), [NAMES[x] for x in ORDER], fontsize=6); ax.set_yticks(range(3), [NAMES[x] for x in ORDER] if loss == "contrastive" else [], fontsize=6)
    ax.set_title(loss.capitalize(), fontsize=7); ax.set_xlabel("Test on", fontsize=6.5)
    if loss == "contrastive": ax.set_ylabel("Train on", fontsize=6.5)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{mat[i, j]*100:.1f}", ha="center", va="center", fontsize=6.5, color="white" if mat[i, j] > 0.2 else "black")
    for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout(w_pad=0.4); fig.savefig("fig1_heatmap.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# Fig 2: accuracy at the fixed threshold vs best threshold, cross-dataset pairs (contrastive)
pairs = [(a, c) for a in ORDER for c in ORDER if a != c]
fig, ax = plt.subplots(figsize=(3.45, 2.0))
x = np.arange(len(pairs)); w = 0.38
fx = [mean(train=a, test=c, condition="clean", loss="contrastive").acc_fixed * 100 for a, c in pairs]
bt = [mean(train=a, test=c, condition="clean", loss="contrastive").acc_best * 100 for a, c in pairs]
ax.bar(x - w/2, bt, w - 0.03, color=BLUE, label="Best threshold (per test set)")
ax.bar(x + w/2, fx, w - 0.03, color=ORANGE, hatch="////", edgecolor="white", linewidth=0, label="Fixed threshold (from training data)")
ax.axhline(50, color=MUTED, lw=0.6, ls="--"); ax.text(-0.45, 51, "chance", fontsize=6, color=MUTED, ha="left")
ax.set_xticks(x, [f"{NAMES[a]}\n→{NAMES[c]}" for a, c in pairs], fontsize=6); ax.set_ylim(40, 100)
ax.set_ylabel("Balanced accuracy (%)", fontsize=6.5); ax.legend(fontsize=5.8, frameon=False, loc="upper right", ncol=1)
fig.tight_layout(); fig.savefig("fig2_threshold.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# Fig 3: EER under degradation, own dataset, contrastive
conds = ["clean", "blur", "lines", "stamp", "mix", "noise"]
fig, ax = plt.subplots(figsize=(3.45, 2.0))
w = 0.26
for k, (tr, col, h) in enumerate(zip(ORDER, [BLUE, ORANGE, AQUA], ["", "////", "\\\\\\\\"])):
    vals = [mean(train=tr, test=tr, condition=c, loss="contrastive").EER * 100 for c in conds]
    ax.bar(np.arange(len(conds)) + (k - 1) * w, vals, w - 0.03, color=col, hatch=h, edgecolor="white", linewidth=0, label=NAMES[tr])
ax.axhline(50, color=MUTED, lw=0.6, ls="--"); ax.text(-0.45, 51.2, "chance (50%)", fontsize=6, color=MUTED, ha="left")
ax.set_xticks(range(len(conds)), [c.capitalize() for c in conds], fontsize=6.3); ax.set_ylim(0, 68)
ax.set_ylabel("EER (%)", fontsize=6.5); ax.legend(fontsize=6, frameon=False, ncol=3, loc="upper right", title="Trained and tested on", title_fontsize=6)
fig.tight_layout(); fig.savefig("fig3_degradation.png", dpi=300, bbox_inches="tight"); plt.close(fig)
print("figures written")
