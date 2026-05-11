# Results Status

This document tracks which results are currently diagnostic and which are final.

## Current status

Human annotation is in progress. The numbers below come from the automatic diagnostic scorer and should not be treated as final empirical claims.

## Diagnostic runs completed

| Run | Split | Trajectories | Parse success | Status |
|---|---:|---:|---:|---|
| GPT-4.1 v0.3 seed | 40 scenarios x 4 conditions | 160 | 100% | Diagnostic; ceiling effect for unsafe action |
| GPT-4.1 v0.4 stress | 24 scenarios x 4 conditions | 96 | 100% | Diagnostic; primary annotation target |
| Llama 3.1 8B v0.3 seed | 40 scenarios x 4 conditions | 160 | 100% | Diagnostic; useful weaker-model comparison |

## Key diagnostic patterns

- GPT-4.1 seed run: trace conditions produced reliable redress traces, but the run had no adverse-side-effect harms under the diagnostic scorer.
- GPT-4.1 stress run: stress scenarios produced some adverse-action variation and remain the primary human-annotation target.
- Llama 3.1 8B seed run: traces were generated reliably, but trace generation alone did not ensure safe behavior.

## Final paper should report

- human annotation agreement;
- adjudicated safety labels;
- adjudicated redressability scores;
- automatic diagnostic scores only as supporting or triage analysis;
- qualitative examples selected after annotation is complete.
