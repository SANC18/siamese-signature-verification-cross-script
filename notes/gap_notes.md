# Research gap notes

For every paper, record what it tested and what it did not. The gap shows up as a pattern down the right-hand column.

| Paper | What it tested | What it did not test or admits as a limitation |
| --- | --- | --- |
| Dey et al. 2017 (SigNet) | Siamese CNN on CEDAR, GPDS, Bengali, Hindi; a cross-dataset experiment | Best accuracy came from training on the same dataset as the test set (verify in the full text) |
| Parracho 2025 | Cross-dataset generalization, ResNet-34 Siamese, contrastive vs triplet | Datasets seen in the abstract: CEDAR, ICDAR, GPDS Synthetic (check whether Indian scripts are covered) |

## Patterns I notice

(Write these yourself after reading three or four papers.)

## Draft gap statement

"Existing work [does X], but [Y] has not been [examined or tested] for [condition]. This study [does Z]."

## Checks before I claim the gap

- [ ] Searched Google Scholar for cross-dataset and cross-script signature verification
- [ ] Read the full text of Parracho 2025
- [ ] Read the open-issues list in Hameed et al. 2021
- [ ] Looked at "Cited by" for SigNet and Parracho
