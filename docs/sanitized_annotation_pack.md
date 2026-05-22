# Sanitized Annotation Pack

This document explains the reviewer-facing annotation pack under `supplementary/annotation/gpt41_v04_stress_sanitized_pack/`.

The pack contains the case files and instructions used for single-pass validation of the GPT-4.1 v0.4 stress trajectories. It is safe for reviewer inspection because it omits condition labels, expected-action metadata, heuristic scores, private mapping files, and model-run identifiers.

The pack is included so that reviewers can inspect the evidence available to the validator and compare it with the blinded validation CSV in `results/human/`.

To regenerate a comparable pack from raw model trajectories, run:

```bash
bash scripts/build_gpt41_v04_sanitized_annotation_pack.sh
```

The generated private mapping file must not be shared with annotators before labels are frozen.
