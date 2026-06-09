# Skill Engineering Lab Report

## Summary

Skill: `ai-video-creator-style`  
Iteration: `iteration-001`  
Cases: 12  
Decision: **ship**

This lab compares the same evaluation set across three states:

```text
without_skill -> with_skill v1 -> with_skill v2
```

The point is not that the generated video copy is beautiful. The point is that Skill behavior becomes observable, gradable, and improvable.

## Metrics

| Config | Pass Rate | Trigger Recall | Over-trigger | Avg Tokens | Avg Time |
| --- | ---: | ---: | ---: | ---: | ---: |
| without_skill | 16.7% | n/a | n/a | 720 | 480 ms |
| with_skill v1 | 75.0% | 80.0% | 50.0% | 1142 | 828 ms |
| with_skill v2 | 100.0% | 100.0% | 0.0% | 935 | 625 ms |

## Lift

| Comparison | Quality Lift | Token Delta |
| --- | ---: | ---: |
| v1 vs baseline | 58.3% | 58.7% |
| v2 vs baseline | 83.3% | 29.9% |
| v2 vs v1 | 25.0% | -18.2% |

## What Changed From v1 To v2

- `description` now includes negative boundaries: no press releases, project plans, issue triage, or generic non-video writing.
- `SKILL.md` now has a clear output contract: titles, cover text, demo plan, outline, script, self-check.
- Required checks are hardened: title count, cover line length, demo-first opening, old/new contrast.
- A deterministic verifier script exists for package structure and line-length checks.

## Top v1 Badcases

| Case | Type | Score | Failure Patterns |
| --- | --- | ---: | --- |
| `boundary-sparse-brief` | boundary | 20.0% | trigger_mismatch, outcome_incomplete, style_weak, generalization_risk |
| `extension-cover-only` | extension | 20.0% | trigger_mismatch, outcome_incomplete, style_weak, generalization_risk |
| `negative-press-release` | negative | 50.0% | trigger_mismatch, outcome_incomplete, efficiency_cost |

## Top v2 Badcases

No failing badcases.

## Failure Pattern Diagnosis

| Pattern | without_skill | v1 | v2 | Suggested Action |
| --- | ---: | ---: | ---: | --- |
| efficiency_cost | 0 | 9 | 0 | Move deterministic checks into scripts and trim references. |
| generalization_risk | 4 | 2 | 0 | Add paraphrase/boundary cases to regression set. |
| outcome_incomplete | 10 | 3 | 0 | Harden required output checklist. |
| style_weak | 10 | 10 | 0 | Improve references and examples. |
| trigger_mismatch | 0 | 3 | 0 | Tighten or broaden `description` boundaries. |

## Governance Assets Created

- `evals/cases.json`: 12-case seed eval set.
- `runs/iteration-001/benchmark.json`: benchmark summary.
- `runs/iteration-001/*/trace.jsonl`: routing and reference-loading traces.
- `runs/iteration-001/*/grading.json`: structured grading output.
- `skills/ai-video-creator-style/scripts/validate_package.py`: deterministic verifier.
- `governance/versions.json`: version hypotheses, risks, metrics, and decisions.
- `governance/reason_archive.json`: badcase root-cause archive.
- `governance/regression_set.json`: must-keep regression cases.

## Next Actions

1. Add 3-5 real product briefs from past work as regression cases.
2. Replace the deterministic simulator with real LLM calls behind the same grading interface.
3. Add a small HTML dashboard if this will be used in live workshops.
4. Track future v3 changes in `governance/versions.json`.
5. Keep negative cases in the regression set to prevent over-triggering.
