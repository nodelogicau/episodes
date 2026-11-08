# self-attested-acts Specification

## Purpose

The episode shape for an act that left no record of its own: an act attested by the person who did it, timed from the act, recorded only on their explicit attestation, and recognised by its content shape rather than its kind. Introduced by change `self-attested-acts`.

## Requirements

### Requirement: An act with no record can be recorded as self-attested
The specification SHALL admit a self-attested act: an episode recording something its standpoint did, whose record is that standpoint's own attestation, with `occurred` giving when the act took place. Its `content` SHALL be `{mode: none}`. When the attestation is an episode in the same workspace, the act SHALL name it with a `via` link. `content.ref` SHALL NOT be an episode id, on a self-attested act or on any episode.

#### Scenario: Attested in conversation
- **WHEN** the person tells the harness at 11:00 "log ninety minutes of deep work from nine", and the harness records an episode with `occurred` 09:00–10:30, `basis: stated`, `standpoint` and `source.author` the person, `content: {mode: none}`, and `links: [{rel: via, href: <the turn's id>}]`
- **THEN** the episode is valid

#### Scenario: Attested through a logging action
- **WHEN** the person presses a "log it" control with no conversation, and the writer records an episode with `content: {mode: none}`, no `links`, and `standpoint` equal to `source.author`
- **THEN** the episode is valid

#### Scenario: An episode id in `content.ref`
- **WHEN** an episode carries `content: {mode: ref, ref: epi_01a1…}`
- **THEN** a validator rejects it, naming the field

### Requirement: Self-attestation only
A self-attested act's `standpoint` SHALL equal its `source.author`. When it has a `via` link to an episode that resolves in the workspace, that episode's `standpoint` SHALL equal the act's `standpoint`. A `via` link that does not resolve SHALL be reported as unresolved, not invalid.

#### Scenario: Recording another person's act
- **WHEN** a writer records a self-attested act whose `standpoint` is Jane and whose `source.author` is Ben
- **THEN** a validator rejects it

#### Scenario: Attestation by someone else
- **WHEN** a self-attested act by Ben links `via` an email episode whose standpoint is Jane
- **THEN** a validator rejects it

#### Scenario: The attestation was dropped
- **WHEN** a self-attested act links `via` an episode id that is not in the workspace
- **THEN** a validator reports the link as unresolved and does not reject the episode

### Requirement: Recorded only on explicit attestation
A writer SHALL record a self-attested act only when its standpoint explicitly attests it, by asking for it to be recorded or through an action whose purpose is recording it. A writer SHALL NOT record one from what it infers.

#### Scenario: A passing remark
- **WHEN** the person says in passing "finally got the budget done" without asking for anything to be recorded
- **THEN** a conformant writer records no self-attested act; the turn stays a turn

### Requirement: Shape, not kind, makes a self-attested act
A validator SHALL treat as a self-attested act any episode with `content.mode: none` that no episode names as its `container`. It SHALL apply the self-attestation rules to these whatever their `kind`. A container with `content.mode: none` SHALL remain valid whatever its standpoint. `kind: activity` SHALL be recommended and SHALL remain descriptive.

#### Scenario: An unusual kind
- **WHEN** a self-attested act carries `kind: workout`
- **THEN** it is valid if the self-attestation rules hold, and the kind changes nothing

#### Scenario: A container
- **WHEN** a conversation container with `content: {mode: none}` has turns naming it as `container`, and its standpoint differs from `source.author`
- **THEN** it is valid

### Requirement: Timing follows the happening
A self-attested act's `occurred` SHALL be when the act took place: `stated` when the person gave the time, `inferred` when it was worked out. It SHALL satisfy the rule that nothing is recorded before it happens.

#### Scenario: Logged before it ends
- **WHEN** at 10:00 the person logs a block "nine to half past ten"
- **THEN** a conformant writer does not record the stated `end`; it may record the act with `start` 09:00 and no `end`
