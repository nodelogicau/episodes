## Context

The specification is `README.md`. Its constraints:
- It stands alone (`openspec/specs/standalone-conformance`).
- It records only what has happened, timed from the happening (`openspec/specs/episode-evidence`).
- An episode records and never interprets.
- What another person says is never recorded as that person's episode. The `standpoint` section says this for notes.

Issue #2 offers three options:
1. Don't admit acts without a record.
2. Admit them as self-testimony with `mode: none`.
3. Admit them for any standpoint.

It asks for a choice between 1 and 2.

## Goals / Non-Goals

**Goals:**
- An act with no record can be located in time and attributed to whoever did it, so that recall by time and by speaker finds it.
- Every such episode can be traced to an attestation by the person who did the act.
- No harness can use this shape to assert what anyone did.

**Non-Goals:**
- Acts by a harness on its own account. A harness's acts usually leave records (tool calls, messages). Raised in Status if needed.
- Third-party acts, such as Jane saying she finished the report. These stay DKF claims.
- Any judgement about the act: whether it was productive, or whether it fulfilled anything.

## Decisions

**1. Admit the self-attested act (option 2, refined), rather than not admitting it (option 1).**
Under option 1, the act is recoverable only by reading a note or a turn. That is interpretation, so it would become a DKF claim, and the episode store would never locate the act in time. Recall by time and the comparison of meant against done would both miss it. Option 2 puts the act in the index under its own time and standpoint. The danger option 2 brings, a harness asserting acts, is contained by decisions 3 and 4.
Option 3 is rejected for the reason the issue gives: it is the source-monitoring failure that `standpoint` exists to prevent.

**2. The record of the act is the attestation, carried by the existing `content` modes.**
- Attested in the workspace (the person tells the harness "log ninety minutes of deep work this morning"): `content: {mode: ref, ref: epi_<turn>}`. A `ref` may already be any identifier meaningful to something that can fetch it, and an episode id is one. No `hash` is needed, because episodes are never revised.
- Attested with nothing to hold it (a button, a form): `content: {mode: none}`.

Alternatives:
- (a) A new `content.mode: attested`.
- (b) A new top-level `attestation:` field.

Both add vocabulary for something the existing modes already express. "Where the record of it lives" is exactly the attestation.

**3. Self only: the standpoint is the author, and the attestation is the standpoint's.**
- A self-attested act's `standpoint` MUST equal `source.author`.
- When `content` refs an episode, that episode's `standpoint` MUST equal the act's `standpoint`.

A validator can check the first always, and the second whenever the ref resolves in the workspace. A ref that does not resolve is reported as unresolved, not invalid: the attestation may have been redacted or dropped.

**4. Recorded only on explicit attestation.**
A writer MUST record a self-attested act only when the standpoint explicitly attests it: by asking for it to be recorded, or through an action whose purpose is recording it. A writer MUST NOT record one from what it infers, such as a passing "finally got the budget done" in conversation. That passing remark stays a turn, and anything taken from it is a DKF claim. This keeps the harness a scribe and not an interpreter. Validators cannot check it, so it is a writer rule, in the same way that `redacted.reason` must not restate what was removed.

**5. What makes an episode a self-attested act is structural, not `kind`.**
`kind` stays descriptive, and `activity` is only recommended. Validity rules attach to the shape:
- `mode: none` on an episode that is not a container (no episode names it as `container`) is a self-attested act, and decision 3's first rule applies.
- `mode: ref` whose `ref` is an episode id is a self-attested act, and both of decision 3's rules apply.
- A container stays valid with `mode: none` whatever its standpoint.

**6. Timing follows `episode-evidence`.**
`occurred` is when the act took place. It is `stated` when the person gave the time, and `inferred` when it was worked out ("this morning"). The episode is recorded after `occurred.start`. If an end is given, it is no later than the recording.

## Risks / Trade-offs

- [A harness ignores decision 4 and records acts from casual remarks] → Requiring a ref to the attestation, where one exists, makes every such episode checkable in review. The spec says plainly that inference belongs in DKF.
- [A container recorded before its first child looks like a self-attested act for a moment] → A container is normally written together with its first child. A validator run between the two may warn, so the text says writers SHOULD write a container and its first child together.
- [`ref` to an episode id overloads the reference mode] → It is the existing mode used as defined. The text names the case explicitly so that readers resolve `epi_` refs in their own workspace.

## Migration Plan

None. The format is a draft.

## Open Questions

- Should a harness's own acts that left no record have a shape? This is deferred to Status.
- Should a self-attested act be allowed to name others present (`participants`), given that only its standpoint attested it? The proposal allows it, because `participants` is not a claim about what they did. Revisit if it proves misleading.
