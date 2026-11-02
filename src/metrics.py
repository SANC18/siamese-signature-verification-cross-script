"""Evaluation metrics: FAR, FRR, EER and AUC.

Convention used everywhere in this project:
    label 1 = genuine pair (same writer)
    label 0 = forged or different-writer pair
    A pair is ACCEPTED when its distance is <= the threshold.
"""

import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve


def far_frr_at_threshold(distances, labels, threshold):
    """Return (FAR, FRR) at a given distance threshold.

    FAR: share of forged pairs wrongly accepted.
    FRR: share of genuine pairs wrongly rejected.
    """
    distances = np.asarray(distances, dtype=float)
    labels = np.asarray(labels)
    genuine = distances[labels == 1]
    forged = distances[labels == 0]
    frr = float(np.mean(genuine > threshold))
    far = float(np.mean(forged <= threshold))
    return far, frr


def equal_error_rate(distances, labels):
    """Return (EER, threshold) where FAR and FRR are as equal as possible.

    Compute this on the VALIDATION set, then reuse the threshold on the test
    set. Never pick the threshold on the test set.
    """
    scores = -np.asarray(distances, dtype=float)  # higher score = more genuine
    fpr, tpr, thresholds = roc_curve(labels, scores)
    fnr = 1.0 - tpr
    idx = int(np.nanargmin(np.abs(fnr - fpr)))
    eer = float((fpr[idx] + fnr[idx]) / 2.0)
    threshold = float(-thresholds[idx])
    return eer, threshold


def auc(distances, labels):
    """Area under the ROC curve: closer to 1 means better separation."""
    return float(roc_auc_score(labels, -np.asarray(distances, dtype=float)))


def best_balanced_accuracy(distances, labels):
    """Best-case accuracy over ALL thresholds, as 0.5 * (TPR + TNR).

    This is the 'best threshold for each test set' style of accuracy. A real
    system cannot know that threshold in advance, so we report it only for
    comparison with papers that use it, next to the fixed-threshold accuracy.
    """
    fpr, tpr, _ = roc_curve(labels, -np.asarray(distances, dtype=float))
    return float(np.max(0.5 * (tpr + (1.0 - fpr))))
