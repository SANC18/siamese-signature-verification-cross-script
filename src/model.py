"""The Siamese network: one CNN encoder used twice, with shared weights."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Encoder(nn.Module):
    """A small CNN that turns a signature image into an embedding.

    Input:  a batch of grayscale images, shape (batch, 1, height, width)
    Output: a batch of embeddings, shape (batch, embedding_dim)

    The first convolution layers find edges and short strokes, deeper layers
    combine them into shapes. Global average pooling at the end lets the
    network accept images of different sizes.
    """

    def __init__(self, embedding_dim: int = 128):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.fc = nn.Linear(128, embedding_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x).flatten(1)
        return self.fc(x)


class SiameseNet(nn.Module):
    """Runs the SAME encoder on two signatures and returns both embeddings.

    There is only one encoder object, so the 'two networks' share every weight
    by construction. This is what makes the two embeddings comparable.
    """

    def __init__(self, embedding_dim: int = 128, normalize: bool = True):
        super().__init__()
        self.encoder = Encoder(embedding_dim)
        self.normalize = normalize

    def embed(self, x: torch.Tensor) -> torch.Tensor:
        """One signature in, one embedding out (length 1 if normalize=True)."""
        z = self.encoder(x)
        return F.normalize(z, dim=1) if self.normalize else z

    def forward(self, a: torch.Tensor, b: torch.Tensor):
        return self.embed(a), self.embed(b)

    @staticmethod
    def distance(emb_a: torch.Tensor, emb_b: torch.Tensor) -> torch.Tensor:
        """Euclidean distance between embeddings. Small = similar signatures."""
        return F.pairwise_distance(emb_a, emb_b)
