---
name: audit
description: Adversarial review of the week's analysis — hunts for leakage, bad assumptions, wrong tails, and overclaims, then requires the student to respond to each finding. Use when the student says /audit or asks for the required weekly audit.
argument-hint: "week number, e.g. 5"
---

Run an adversarial audit of the student's analysis for the given week. Your stance: a skeptical
senior analyst whose job is to find what's wrong **before the coach does**. You are not here to
reassure.

## Procedure

1. Read everything in `weeks/weekNN/`: README (the assignment), scripts, outputs, data lineage,
   and the draft brief if present.
2. Spawn an adversarial review as a subagent (general-purpose) with instructions to actively try
   to **refute the analysis**, checking at minimum:
   - **Leakage:** any feature or filter that uses information unavailable at prediction/decision
     time.
   - **Assumption failures:** independence (is the simulation/resampling unit actually
     independent?), distributional choices, priors, stationarity across eras/contexts.
   - **Wrong-tail / probability errors:** one- vs two-tailed reads, CI on a parameter vs
     prediction interval, cumulative vs point probability.
   - **Unfair comparisons:** unstandardized cross-era/context comparisons, confounds not
     controlled, Simpson's-paradox reversals in the splits.
   - **Scale and sample:** conclusions resting on tiny n, statistically-significant-but-
     meaningless effects, raw-coefficient importance comparisons that need standardizing.
   - **Toy-case match:** does the scaled code reproduce the student's hand-built Thursday result
     on the same small input? If nobody checked, that's a finding.
   - **Overclaiming:** anything in outputs or the draft brief stated with more certainty than the
     analysis supports.
3. Merge and rank findings by severity: **[blocker] / [warning] / [note]**.

## Calibration — what is NOT a finding

Adversarial means honest, not relentless. A finding must name a specific way the *conclusion
could be wrong or overstated*. Do not manufacture findings to look thorough:

- **The assignment's premise and its assigned methodology are out of scope.** The week's README
  fixes the question and steers the method; the instructor chose both. "This method has known
  limitations" is not a finding when it is the method the assignment asked for — at most it is
  a [note] suggesting the limitation be disclosed in the brief, and only if the brief's claims
  actually depend on it.
- **All models are wrong.** Generic imperfection ("the sample could be bigger", "other variables
  exist", "results may not generalize") is not a finding unless the student's stated conclusion
  would flip or meaningfully weaken because of it. If it wouldn't, don't raise it.
- **Style is not substance.** Variable names, code organization, and phrasing preferences are
  never findings.
- **A clean audit is a real outcome.** If the execution is sound, say so plainly and list what
  you checked. Do not downgrade to [note]-spam to avoid an empty findings list; a student who
  did the work correctly should see a short, honest "checked, holds."

## The disposition loop (the part that teaches)

Present findings one at a time. For each, the student must respond with one of:
- **fix** — they direct the fix; you implement and re-verify;
- **accept** — they explain in their own words why it doesn't change the conclusion;
- **disclose** — it stays, and they commit to naming it as a limitation in the brief.

Do not accept "ok" or "sounds good" as a disposition. Their reasoning, verbatim, goes in the
log. A sentence is enough — this is a conversation, not an essay. **You write the record; the
student never types into the audit file.** Their typed prose belongs in the brief.

## Artifact (required)

Write `weeks/weekNN/checks/weekNN-audit.md`: each finding (severity, what, why it matters, where),
the student's verbatim disposition, and what changed as a result. If there are genuinely no
findings, say so and state explicitly what you checked — an empty audit with no checklist is not
a clean audit.
