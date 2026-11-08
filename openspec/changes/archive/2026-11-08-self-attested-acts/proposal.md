## Why

Issue #2: much of what a person does leaves no record. A solo 90-minute block of deep work produces no email, file or calendar event. The draft has no shape for an act like that. `content` must be `inline`, `ref` or `none`, and `none` is described only for containers. The closest available episode is a note or a turn, but those are dated when they were written, not when the act took place. So the act is missing from recall by time, and that is exactly where a comparison of what was meant with what was done looks.

## What Changes

- Admit the **self-attested act**: an episode recording something its standpoint did, attested by that same person, with `occurred` giving when the act took place. The issue's option 2.
- Its record is the attestation:
  - When the person attested in an episode in the same workspace (a turn or a note), `content` is `{mode: ref, ref: epi_…}` pointing at that episode.
  - When nothing holds the attestation (for example, a "log it" button), `content` is `{mode: none}`.
- Widen `mode: none` beyond containers: it is valid on a container, and on a self-attested act.
- Constrain who can attest:
  - The standpoint of a self-attested act MUST be its `source.author`.
  - If it refs an attestation episode, that episode's standpoint MUST be the same.
  - A writer MUST record one only on the standpoint's own explicit attestation, never from what a harness infers.
- Recommend `kind: activity`, which stays descriptive. No validity rule hinges on `kind`.
- Reject recording acts on another person's behalf (option 3). What someone else says they did remains a DKF claim reported from the episode that says it, as the `standpoint` section already states for notes.

## Capabilities

### New Capabilities
- `self-attested-acts`: the episode shape for an act that left no record of its own: when it is valid, what its content is, and who may attest it.

### Modified Capabilities
<!-- None. `episode-evidence` still holds: a self-attested act is recorded after it happens and timed from the act. `standalone-conformance` still holds: the attestation link is within the workspace. -->

## Impact

- `README.md` only. Affected sections:
  - `EPISODE` (the `kind` row and the `content` row)
  - `content` (the `mode: none` paragraph, plus a new subsection)
  - When an episode is recorded
  - Status
- No change to the index: self-attested acts are indexed like any episode, by `occurred` and `standpoint`, which is the point.
- Once implemented, issue #2 can be closed.
