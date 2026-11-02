"""Training and evaluation of the Siamese network (PyTorch)."""

import copy
import random
from dataclasses import dataclass

import numpy as np
import torch
from torch.utils.data import DataLoader

from .datasets import ImageCache, PairDataset, TripletDataset
from .losses import ContrastiveLoss, TripletLoss
from .metrics import (auc, best_balanced_accuracy, equal_error_rate,
                      far_frr_at_threshold)
from .model import SiameseNet
from .pairs import make_pairs, make_triplets


@dataclass
class TrainConfig:
    epochs: int = 15
    batch_size: int = 64
    lr: float = 1e-3
    weight_decay: float = 1e-4
    margin: float = 1.0
    embedding_dim: int = 128
    pairs_per_epoch: int = 20000
    val_pairs: int = 4000
    patience: int = 5
    num_workers: int = 0
    size: tuple = (128, 192)


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


@torch.no_grad()
def pair_distances(model, dataset, device, batch_size=128):
    """Distance between the two signatures of every pair, plus the labels."""
    model.eval()
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    dists, labels = [], []
    for a, b, y in loader:
        ea, eb = model(a.to(device), b.to(device))
        dists.append(SiameseNet.distance(ea, eb).cpu())
        labels.append(y)
    return torch.cat(dists).numpy(), torch.cat(labels).numpy()


def train_model(data, train_writers, val_writers, loss_name, cfg: TrainConfig,
                device, seed, cache: ImageCache, degrade_training=False, log=print):
    """Train one model. Returns (model, decision threshold, history).

    The threshold is the equal-error-rate point on VALIDATION pairs of the
    training dataset. It is then applied unchanged to every test set.
    """
    set_seed(seed)
    model = SiameseNet(cfg.embedding_dim).to(device)
    optimiser = torch.optim.Adam(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    contrastive, triplet = ContrastiveLoss(cfg.margin), TripletLoss(cfg.margin)

    val_pairs = make_pairs(data, val_writers, cfg.val_pairs, seed=777)
    val_set = PairDataset(val_pairs, cache)

    best_eer, best_state, history, bad_epochs = 1.0, None, [], 0
    for epoch in range(cfg.epochs):
        model.train()
        degrade_kwargs = dict(degrade_kind="random", degrade_prob=0.5) if degrade_training else {}
        if loss_name == "contrastive":
            pairs = make_pairs(data, train_writers, cfg.pairs_per_epoch, seed=seed * 1000 + epoch)
            train_set = PairDataset(pairs, cache, augment_images=True, seed=seed * 1000 + epoch, **degrade_kwargs)
        else:
            triplets = make_triplets(data, train_writers, cfg.pairs_per_epoch, seed=seed * 1000 + epoch)
            train_set = TripletDataset(triplets, cache, augment_images=True, seed=seed * 1000 + epoch, **degrade_kwargs)
        loader = DataLoader(train_set, batch_size=cfg.batch_size, shuffle=True,
                            num_workers=cfg.num_workers, drop_last=True)
        total, count = 0.0, 0
        for batch in loader:
            optimiser.zero_grad()
            if loss_name == "contrastive":
                a, b, y = (t.to(device) for t in batch)
                ea, eb = model(a, b)
                loss = contrastive(ea, eb, y)
            else:
                a, p, n = (t.to(device) for t in batch)
                loss = triplet(model.embed(a), model.embed(p), model.embed(n))
            loss.backward()
            optimiser.step()
            total += loss.item()
            count += 1
        d, y = pair_distances(model, val_set, device)
        eer, _ = equal_error_rate(d, y)
        history.append({"epoch": epoch + 1, "train_loss": total / max(count, 1), "val_eer": eer})
        log(f"  epoch {epoch + 1:02d}  loss {total / max(count, 1):.4f}  val EER {eer:.4f}")
        if eer < best_eer - 1e-4:
            best_eer, best_state, bad_epochs = eer, copy.deepcopy(model.state_dict()), 0
        else:
            bad_epochs += 1
            if bad_epochs >= cfg.patience:
                log("  early stop")
                break

    model.load_state_dict(best_state)
    d, y = pair_distances(model, val_set, device)
    val_eer, threshold = equal_error_rate(d, y)
    return model, threshold, history


def evaluate_condition(model, data, writers, cache, threshold, device,
                       n_pairs=4000, seed=1234, degrade_kind=None):
    """Test pairs are identical for every model (same seed), so comparisons are fair."""
    pairs = make_pairs(data, writers, n_pairs, seed=seed)
    dataset = PairDataset(pairs, cache, degrade_kind=degrade_kind, seed=seed)
    d, y = pair_distances(model, dataset, device)
    far, frr = far_frr_at_threshold(d, y, threshold)
    eer, _ = equal_error_rate(d, y)
    return {
        "n_pairs": len(pairs),
        "EER": eer,
        "AUC": auc(d, y),
        "FAR": far,
        "FRR": frr,
        "acc_fixed": 1.0 - (far + frr) / 2.0,
        "acc_best": best_balanced_accuracy(d, y),
    }
