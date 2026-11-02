# Data folder

Datasets are not stored in this repository. Download them yourself, read each dataset's terms of use, and place them here:

```
data/
  CEDAR/
  BHSig260/
    Hindi/
    Bengali/
  GPDS_Synthetic/      (optional)
```

Search for each dataset by name and use the authors' page or a trusted repository.

Facts to keep in mind (from the SigNet paper):

- BHSig260 has 260 signers: 100 Bengali and 160 Hindi, each with 24 genuine and 30 forged signatures.
- GPDS Synthetic has 4,000 signers, each with 24 genuine and 30 forged signatures.

Folder layouts differ between sources, so write a small loader that builds this structure in code:

```python
data = {
    "writer_001": {"genuine": ["path/a.png", ...], "forged": ["path/b.png", ...]},
    "writer_002": {...},
}
```

`src/pairs.py` expects exactly that dictionary.
