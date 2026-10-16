from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import json

ROOT = Path(__file__).resolve().parent
R = json.loads((ROOT / "results/results.json").read_text())
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
    }
)
C = "#204c67"
ACC = "#9a512b"
shares = R["institution_shares_pct"]
names = list(shares)
short = [
    "London, Old Kent Road",
    "Hackney",
    "Jewish Home",
    "Brighton",
    "Exeter",
    "Bristol",
    "Birmingham, Edgbaston",
    "Manchester",
    "Yorkshire, Doncaster",
    "Northern Counties, Newcastle",
    "Cambrian, Swansea",
    "Liverpool",
]
fig, ax = plt.subplots(figsize=(7.1, 4.4))
y = list(range(12))
ax.hlines(y, 0, list(shares.values()), color="#d2dde2")
ax.scatter(list(shares.values()), y, color=C, s=32, zorder=3)
ax.axvline(
    R["pooled_from_birth_pct"], color=ACC, ls="--", lw=1.2, label="Pooled: 63.09%"
)
ax.set_yticks(y, short)
ax.invert_yaxis()
ax.set_xlim(0, 109)
ax.set_xlabel('Recorded as "deaf from birth" (%)')
ax.set_xticks([0, 25, 50, 75, 100])
ax.grid(axis="x", alpha=0.15)
from analyze import load_institutions

for i, r in enumerate(load_institutions()):
    ax.text(
        103, i, f"{r['from_birth']}/{r['total']}", va="center", ha="left", fontsize=8
    )
ax.text(103, -0.9, "Count", fontsize=8, ha="left")
ax.legend(loc="lower left", frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig(ROOT / "figures/institutions.png")
fig.savefig(ROOT / "figures/institutions.pdf")
plt.close(fig)
fig, ax = plt.subplots(figsize=(7.1, 3.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis("off")
boxes = [
    (
        0.2,
        2.3,
        2.7,
        1.3,
        "1861 report (1863)",
        "National onset extraction\nabandoned as incomplete",
    ),
    (
        3.6,
        2.3,
        2.7,
        1.3,
        "1871 report (1873)",
        "Institutional subset\n665 / 1,054 = 63.09%",
    ),
    (
        7,
        2.3,
        2.7,
        1.3,
        "1881 report (1883)",
        "~37% acquired deafness\nin geographical explanation",
    ),
    (
        3.6,
        0.15,
        6.1,
        1.3,
        "1889 commission appendix",
        "Buxton: two-stage inquiry; medical recording of family testimony\nOgle: further particulars distinguished from verification",
    ),
]
for x, y, w, h, head, body in boxes:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.07",
            facecolor="#edf2f4",
            edgecolor="#9aaeb8",
        )
    )
    ax.text(
        x + w / 2, y + h - 0.22, head, ha="center", va="top", weight="bold", fontsize=9
    )
    ax.text(
        x + w / 2,
        y + 0.5,
        body,
        ha="center",
        va="center",
        fontsize=8.4,
        linespacing=1.55,
    )
ax.annotate(
    "", xy=(3.5, 2.95), xytext=(3, 2.95), arrowprops=dict(arrowstyle="->", color=C)
)
ax.annotate(
    "", xy=(6.9, 2.95), xytext=(6.4, 2.95), arrowprops=dict(arrowstyle="->", color=ACC)
)
ax.text(6.65, 3.8, "Explicit citation", ha="center", fontsize=8, color=ACC)
ax.annotate(
    "",
    xy=(6.5, 1.55),
    xytext=(8.3, 2.15),
    arrowprops=dict(arrowstyle="->", color="#888", ls="--"),
)
ax.text(
    0.35,
    0.75,
    "Reading sequence, not influence.\nOrange arrow: explicit citation.",
    fontsize=8,
    color="#555",
)
fig.tight_layout()
fig.savefig(ROOT / "figures/evidence_chain.png")
fig.savefig(ROOT / "figures/evidence_chain.pdf")
plt.close(fig)
fig, (a, b) = plt.subplots(
    1, 2, figsize=(7.1, 3.4), gridspec_kw={"width_ratios": [1, 1.6]}
)
a.bar([0, 1], [13295, 13295], color=C, width=0.6)
a.bar(1, 1579, bottom=13295, color="#d3a587", hatch="///", edgecolor=ACC, width=0.6)
a.set_xticks([0, 1], ["Enumerated", "Corrected"])
a.set_ylim(0, 17000)
a.set_ylabel("Persons, all ages")
a.text(0, 13700, "13,295", ha="center", fontsize=9)
a.text(1, 15300, "14,874", ha="center", fontsize=9)
a.set_title("(a) 1881 published correction", fontsize=10)
ages = ["<5", "5-14", "15-19", "20-24", "25-44", "45-64", "65+"]
a1871 = [x["1871"] for x in R["age_rate_changes_1871_to_1881"]]
a1881 = [x["1881"] for x in R["age_rate_changes_1871_to_1881"]]
b.plot(ages, a1871, "o-", color=C, label="1871")
b.plot(ages, a1881, "s--", color=ACC, label="1881")
b.set_ylim(0, 720)
b.set_ylabel("Enumerated per million at each age")
b.set_xlabel("Age band (years)")
b.set_title("(b) Uncorrected cross-sections", fontsize=10)
b.legend(frameon=False)
b.grid(axis="y", alpha=0.15)
b.tick_params(axis="x", labelsize=8)
fig.tight_layout(w_pad=2)
fig.savefig(ROOT / "figures/correction_age.png")
fig.savefig(ROOT / "figures/correction_age.pdf")
plt.close(fig)
