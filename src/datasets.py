"""Dataset loaders, image preprocessing, degradations and PyTorch datasets.

Loaders turn a folder of images into the dictionary that src/pairs.py expects:

    {"writer_id": {"genuine": [paths], "forged": [paths]}, ...}

Folder layouts differ between download sources, so the loaders recognise
files by NAME, not by folder. Expected file names:

    CEDAR      original_<writer>_<n>.png      (genuine)
               forgeries_<writer>_<n>.png     (forged)
    BHSig260   H-S-<writer>-G-<nn>.tif         (Hindi genuine)   H-S-<writer>-F-<nn>.tif (forged)
               B-S-<writer>-G-<nn>.tif         (Bengali genuine) B-S-<writer>-F-<nn>.tif (forged)

If your copy uses other names, the loader stops with a clear message showing
what it found, and you can adapt the regular expression below.
"""

import os
import re
from typing import Dict, List

import cv2
import numpy as np
import torch
from torch.utils.data import Dataset

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}
Data = Dict[str, Dict[str, List[str]]]


# ----------------------------------------------------------------- loaders
def _walk_images(root: str):
    for folder, _, files in os.walk(root):
        for name in sorted(files):
            if os.path.splitext(name)[1].lower() in IMAGE_EXTENSIONS:
                yield os.path.join(folder, name), name


def _finish(data: Data, label: str, root: str) -> Data:
    usable = {w: v for w, v in data.items() if len(v["genuine"]) >= 2}
    if len(usable) < 2:
        found = [n for _, n in _walk_images(root)][:5]
        raise ValueError(
            f"{label}: found {len(usable)} usable writers under '{root}'. "
            f"Example file names seen: {found}. Check the folder path and the "
            f"file-name pattern in src/datasets.py."
        )
    return usable


def load_cedar(root: str) -> Data:
    genuine = re.compile(r"original_(\d+)_(\d+)", re.I)
    forged = re.compile(r"forg\w*_(\d+)_(\d+)", re.I)
    data: Data = {}
    for path, name in _walk_images(root):
        m = genuine.search(name)
        kind = "genuine"
        if not m:
            m = forged.search(name)
            kind = "forged"
        if m:
            writer = f"cedar_{int(m.group(1)):03d}"
            data.setdefault(writer, {"genuine": [], "forged": []})[kind].append(path)
    return _finish(data, "CEDAR", root)


def _load_bhsig(root: str, letter: str, label: str) -> Data:
    pattern = re.compile(rf"^{letter}-S-(\d+)-([GF])-(\d+)", re.I)
    data: Data = {}
    for path, name in _walk_images(root):
        m = pattern.match(name)
        if m:
            writer = f"{label.lower()}_{int(m.group(1)):03d}"
            kind = "genuine" if m.group(2).upper() == "G" else "forged"
            data.setdefault(writer, {"genuine": [], "forged": []})[kind].append(path)
    return _finish(data, label, root)


def load_hindi(root: str) -> Data:
    return _load_bhsig(root, "H", "Hindi")


def load_bengali(root: str) -> Data:
    return _load_bhsig(root, "B", "Bengali")


LOADERS = {"cedar": load_cedar, "hindi": load_hindi, "bengali": load_bengali}


# ----------------------------------------------------------- preprocessing
def load_signature(path: str, size=(128, 192)) -> np.ndarray:
    """Read, fit into a fixed canvas and return a uint8 image with ink = bright.

    Steps: grayscale, flip if the background is dark, resize keeping the aspect
    ratio, centre on a blank canvas. (OpenCV + NumPy)
    """
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise IOError(f"Could not read image: {path}")
    if img.mean() < 127:  # dark background: flip so the page is light
        img = 255 - img
    h, w = size
    ih, iw = img.shape
    scale = min(h / ih, w / iw)
    nh, nw = max(1, int(ih * scale)), max(1, int(iw * scale))
    img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)
    canvas = np.full((h, w), 255, np.uint8)
    y, x = (h - nh) // 2, (w - nw) // 2
    canvas[y:y + nh, x:x + nw] = img
    return 255 - canvas  # ink bright, background 0


class ImageCache:
    """Keeps preprocessed images in memory so each file is read only once."""

    def __init__(self, size=(128, 192)):
        self.size = size
        self._store: Dict[str, np.ndarray] = {}

    def get(self, path: str) -> np.ndarray:
        arr = self._store.get(path)
        if arr is None:
            arr = load_signature(path, self.size)
            self._store[path] = arr
        return arr


# -------------------------------------------------- augmentation / degrade
def augment(img: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Small random shift, scale and rotation, so the model is not fooled by position."""
    h, w = img.shape
    angle = rng.uniform(-5, 5)
    scale = rng.uniform(0.92, 1.08)
    tx, ty = rng.uniform(-8, 8), rng.uniform(-6, 6)
    m = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
    m[:, 2] += (tx, ty)
    return cv2.warpAffine(img, m, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)


DEGRADATIONS = ["noise", "blur", "lines", "stamp", "mix"]


def degrade(img: np.ndarray, kind: str, rng: np.random.Generator) -> np.ndarray:
    """Make a clean signature look like it came from a poor scan or a cluttered document.

    noise: scanner grain      blur: out-of-focus scan
    lines: ruling lines       stamp: round stamp outline and small marks
    mix:   two of the above chosen at random
    """
    out = img.astype(np.float32)
    h, w = out.shape
    if kind == "mix":
        for k in rng.choice(["noise", "blur", "lines", "stamp"], size=2, replace=False):
            out = degrade(out.astype(np.uint8), str(k), rng).astype(np.float32)
        return np.clip(out, 0, 255).astype(np.uint8)
    if kind == "noise":
        out += rng.normal(0, 30, out.shape)
        salt = rng.random(out.shape) < 0.01
        out[salt] = 255
    elif kind == "blur":
        k = int(rng.choice([3, 5, 7]))
        out = cv2.GaussianBlur(out, (k, k), 0)
    elif kind == "lines":
        for _ in range(int(rng.integers(2, 5))):
            y = int(rng.integers(0, h))
            cv2.line(out, (0, y), (w - 1, y), 200.0, int(rng.integers(1, 3)))
    elif kind == "stamp":
        cx, cy = int(rng.integers(w // 4, 3 * w // 4)), int(rng.integers(h // 4, 3 * h // 4))
        cv2.circle(out, (cx, cy), int(rng.integers(h // 5, h // 3)), 180.0, 2)
        for _ in range(int(rng.integers(5, 12))):
            x0, y0 = int(rng.integers(0, w - 10)), int(rng.integers(0, h - 10))
            cv2.line(out, (x0, y0), (x0 + int(rng.integers(3, 10)), y0 + int(rng.integers(-3, 4))), 180.0, 1)
    else:
        raise ValueError(f"Unknown degradation: {kind}")
    return np.clip(out, 0, 255).astype(np.uint8)


def to_tensor(img: np.ndarray) -> torch.Tensor:
    return torch.from_numpy(img.astype(np.float32) / 255.0).unsqueeze(0)


# ------------------------------------------------------------------ datasets
class PairDataset(Dataset):
    """Items are (signature A, signature B, label); label 1 = same writer.

    Signature B plays the 'questioned' signature, so degradations are applied
    to B only (A is the clean reference kept on file).
    """

    def __init__(self, pairs, cache: ImageCache, augment_images=False,
                 degrade_kind=None, degrade_prob=1.0, seed=0):
        self.pairs, self.cache = pairs, cache
        self.augment_images, self.degrade_kind = augment_images, degrade_kind
        self.degrade_prob, self.seed = degrade_prob, seed

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, i):
        a_path, b_path, label = self.pairs[i]
        rng = np.random.default_rng(self.seed * 1_000_003 + i)
        a, b = self.cache.get(a_path), self.cache.get(b_path)
        if self.augment_images:
            a, b = augment(a, rng), augment(b, rng)
        if self.degrade_kind and rng.random() < self.degrade_prob:
            kind = self.degrade_kind if self.degrade_kind != "random" else str(rng.choice(DEGRADATIONS))
            b = degrade(b, kind, rng)
        return to_tensor(a), to_tensor(b), torch.tensor(float(label))


class TripletDataset(Dataset):
    """Items are (anchor, positive, negative)."""

    def __init__(self, triplets, cache: ImageCache, augment_images=False,
                 degrade_kind=None, degrade_prob=1.0, seed=0):
        self.triplets, self.cache = triplets, cache
        self.augment_images, self.degrade_kind = augment_images, degrade_kind
        self.degrade_prob, self.seed = degrade_prob, seed

    def __len__(self):
        return len(self.triplets)

    def __getitem__(self, i):
        rng = np.random.default_rng(self.seed * 1_000_003 + i)
        imgs = [self.cache.get(p) for p in self.triplets[i]]
        if self.augment_images:
            imgs = [augment(x, rng) for x in imgs]
        if self.degrade_kind:
            for j in (1, 2):  # positive and negative are the 'questioned' signatures
                if rng.random() < self.degrade_prob:
                    kind = self.degrade_kind if self.degrade_kind != "random" else str(rng.choice(DEGRADATIONS))
                    imgs[j] = degrade(imgs[j], kind, rng)
        return tuple(to_tensor(x) for x in imgs)
