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
2. Run the adversarial review yourself, in this session — do not spawn a subagent. Actively try
   to **refute the analysis**. Verify against the data, never against your own code: re-derive
   each key quantity from the raw rows (recompute the filter, cross-tab the flags, pull and read
   the discrepant cases) rather than re-reading the code that produced it, and check every column
   used against what it actually means in the source data — a clause can be logically clean and
   still wrong about the field's semantics. Check at minimum:
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
   - **Overclaiming:** anything in outputs or the draft brief stated with more certainty than the
     analysis supports.
3. Rank findings by severity: **[blocker] / [warning] / [note]**.
4. **Cap what you present.** Report every [blocker] (objective bugs that must be remedied), and
   if there are fewer than two blockers, fill up to a total of two findings with the top-ranked
   remainder. Never present more than that cap. Everything else you checked collapses into one
   short "also checked, holds" line in the artifact — no per-item write-ups. Nine findings is a
   worse audit than two that matter.

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

End the file with a `## Brief follow-ups` section. A fix changes the code and outputs, but the
brief is the student's to change, so this list is what tells them which parts of it the audit
touched. One line per item, in this form:

- `- [revise] Q2: "<the brief sentence, quoted exactly as it stands now>" — <the finding it
  conflicts with, and the corrected number or fact from the outputs>`: a brief sentence that a
  finding contradicts, whatever the disposition. **accept** does not exempt it: a student can
  accept that a finding leaves the conclusion standing while a number in the brief is still
  wrong.
- `- [disclose] Q<n or "any">: <the limitation, named in a few words>`: one line per disclose
  disposition.
- `- [check] Q<n>: <the finding>`: a fix that changed a number or result the brief will need,
  when there is no draft brief yet or the draft doesn't state that number.

Quote the brief and the outputs; never draft replacement wording, a corrected sentence, or the
disclosure itself. Same hard rule as /coach-brief: every word of the brief is the student's. If
nothing in the audit touches the brief, write `None.` under the heading. Then tell the student
in one line how many follow-ups there are and that `/submit` will check them.
