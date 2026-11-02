"""Loss functions that teach the network what 'close' and 'far' mean."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ContrastiveLoss(nn.Module):
    """Works on pairs.

    same = 1 for a genuine pair (pull the embeddings together)
    same = 0 for a mismatched pair (push apart until at least `margin` away)

        L = same * d^2 + (1 - same) * max(0, margin - d)^2
    """

    def __init__(self, margin: float = 1.0):
        super().__init__()
        self.margin = margin

    def forward(self, emb_a, emb_b, same):
        same = same.float()
        d = F.pairwise_distance(emb_a, emb_b)
        loss = same * d.pow(2) + (1.0 - same) * F.relu(self.margin - d).pow(2)
        return loss.mean()


class TripletLoss(nn.Module):
    """Works on triplets: anchor, positive (same writer), negative (forgery or other writer).

        L = max(0, d(anchor, positive) - d(anchor, negative) + margin)

    The anchor should be closer to the positive than to the negative by at
    least `margin`.
    """

    def __init__(self, margin: float = 1.0):
        super().__init__()
        self.margin = margin

    def forward(self, anchor, positive, negative):
        d_ap = F.pairwise_distance(anchor, positive)
        d_an = F.pairwise_distance(anchor, negative)
        return F.relu(d_ap - d_an + self.margin).mean()
