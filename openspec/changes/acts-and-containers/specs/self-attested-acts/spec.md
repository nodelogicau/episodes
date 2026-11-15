## MODIFIED Requirements

### Requirement: An act with no record can be recorded as self-attested
The specification SHALL admit a self-attested act: an episode recording something its standpoint did, whose record is that standpoint's own attestation, with `occurred` giving when the act took place. Its `content` SHALL be exactly `{mode: attested}`, with no other key. When the attestation is an episode in the same workspace, the act SHALL name it with a `via` link. `content.ref` SHALL NOT be an episode id, on a self-attested act or on any episode.

#### Scenario: Attested in conversation
- **WHEN** the person tells the harness at 11:00 "log ninety minutes of deep work from nine", and the harness records an episode with `occurred` 09:00–10:30, `basis: stated`, `standpoint` and `source.author` the person, `content: {mode: attested}`, and `links: [{rel: via, href: <the turn's id>}]`
- **THEN** the episode is valid

#### Scenario: Attested through a logging action
- **WHEN** the person presses a "log it" control with no conversation, and the writer records an episode with `content: {mode: attested}`, no `links`, and `standpoint` equal to `source.author`
- **THEN** the episode is valid

#### Scenario: An episode id in `content.ref`
- **WHEN** an episode carries `content: {mode: ref, ref: epi_01a1…}`
- **THEN** a validator rejects it, naming the field

#### Scenario: Other content keys on an act
- **WHEN** an episode carries `content: {mode: attested, text: "ran 5 km"}`
- **THEN** a validator rejects it, naming the field

## ADDED Requirements

### Requirement: The mode makes a self-attested act
A validator SHALL treat as a self-attested act every episode with `content.mode: attested`, and no other episode. It SHALL apply the self-attestation rules to these whatever their `kind`, and whether or not any episode names them as its `container`. `kind: activity` SHALL be recommended and SHALL remain descriptive.

#### Scenario: An unusual kind
- **WHEN** a self-attested act carries `kind: workout`
- **THEN** it is valid if the self-attestation rules hold, and the kind changes nothing

#### Scenario: A childless container
- **WHEN** a conversation container with `content: {mode: none}` has no children, and its standpoint differs from `source.author`
- **THEN** a validator does not apply the self-attestation rules to it, and it is valid

#### Scenario: An act with children
- **WHEN** a self-attested act for a meeting is named as `container` by two note episodes
- **THEN** it is still a self-attested act, and the self-attestation rules apply to it

#### Scenario: An act written under the earlier draft
- **WHEN** a validator reads an episode with `content: {mode: none}`, no children, `kind: activity` and a `via` link
- **THEN** it treats the episode as a container with no children, not as a self-attested act

### Requirement: An attestation made in conversation is recorded and named
When an act is attested in an episode the writer records, which includes every attestation made in a conversation the writer is recording, the writer SHALL record that episode and SHALL link the act `via` it. A writer SHALL NOT omit the link by leaving the attesting episode unrecorded. When nothing the writer records holds the attestation, as with a control whose only purpose is to log the act, the act SHALL have no `via` link for it. The rule SHALL NOT depend on whether `source.harness` is present.

#### Scenario: A harness asked in conversation
- **WHEN** the person asks a harness in conversation to log a run, and the harness records the act
- **THEN** a conformant harness has recorded the turn, and the act links `via` it

#### Scenario: A connector with a logging control
- **WHEN** a connector named in `source.harness` records an act from a "log my run" button, and no episode holds the attestation
- **THEN** the act has no `via` link, and it is valid

## REMOVED Requirements

### Requirement: Shape, not kind, makes a self-attested act
**Reason**: Recognising an act by what is missing made a container with no children an act, so a conversation container whose first turn was never written failed the act rules. An act now states that it is one, through `content.mode: attested`.
**Migration**: Writers record acts with `content: {mode: attested}`. An act written with `content: {mode: none}` under the earlier draft reads as a container with no children: it stays valid, a validator warns on it, and the self-attestation rules no longer apply to it. Episodes are not rewritten, so no conversion is defined.
