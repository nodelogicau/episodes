## ADDED Requirements

### Requirement: `links` follows RFC 8288
An episode MAY carry `links`, a list of mappings each with exactly the keys `rel` and `href`. `rel` SHALL be a relation type registered in the IANA Link Relations registry, written in lowercase and used in its registered meaning, or an absolute URI. `href` SHALL be an episode id, which is resolved within the workspace, or a URI. A writer SHALL sort `links` by `rel` and then by `href`. A reader SHALL NOT reject an episode for a `rel` it does not know.

#### Scenario: A registered relation
- **WHEN** an episode carries `links: [{rel: via, href: epi_01a1…}]`
- **THEN** the episode is valid

#### Scenario: An extension relation
- **WHEN** an episode carries a link whose `rel` is `https://www.w3.org/ns/activitystreams#inReplyTo`
- **THEN** a reader accepts it and gives it no meaning under this format

#### Scenario: A non-URI unregistered relation
- **WHEN** an episode carries `rel: answers`, which is neither registered nor an absolute URI
- **THEN** a validator rejects it, naming the link

### Requirement: Links are written once
A writer SHALL write `links` when it records the episode and SHALL NOT add, remove or change a link afterwards, except by redaction. A link to an episode SHALL name an episode recorded before it.

#### Scenario: Adding a link later
- **WHEN** a writer tries to add a link to an existing episode file
- **THEN** that is a non-conformant change to the file

### Requirement: Links are unindexed and redactable
`links` SHALL NOT be mirrored in the index. `links` SHALL be in the closed set of redactable fields, and redacting it SHALL remove the whole list.

#### Scenario: Redacting a link to a private URL
- **WHEN** a person redacts an episode's links
- **THEN** `links` is absent from the file, `redacted.fields` lists `links`, and no index entry changes

### Requirement: An unresolved episode link is reported, not invalid
A link whose `href` is an episode id that does not resolve in the workspace SHALL be reported as unresolved, and SHALL NOT make the episode invalid.

#### Scenario: The target was never copied
- **WHEN** an episode links `via` an episode id that is not in the workspace
- **THEN** a validator reports the link as unresolved and accepts the episode

### Requirement: `via` and `predecessor-version` between episodes
Between episodes, `via` SHALL mean that the episode records something taken from its target, such as a transcript made from a recording or a self-attested act from its attesting turn. `predecessor-version` SHALL mean that the episode supersedes its target as a rendering of the same thing. A link SHALL NOT change the episode it targets.

#### Scenario: A transcript of a voice memo
- **WHEN** a harness transcribes a voice memo recorded as reference episode A
- **THEN** it records an inline episode B with `derivation: transcribed` and `links: [{rel: via, href: A}]`

#### Scenario: A better transcript
- **WHEN** a harness later produces a better transcript C of the same memo
- **THEN** C carries `links: [{rel: predecessor-version, href: B}, {rel: via, href: A}]`, and B is unchanged

### Requirement: Links do not restate containment
A writer SHALL NOT write a link that restates `container`. A validator SHALL warn, naming the episode, on an `up` or `collection` link whose target is the episode's own `container`.

#### Scenario: A turn that links up to its conversation
- **WHEN** a turn has `container: X` and `links: [{rel: up, href: X}]`
- **THEN** a validator warns, naming the turn

### Requirement: Links record provenance, not judgement
The specification SHALL state that links record relations known when the episode is recorded, such as provenance and versioning, and that no relation it defines targets an object of another format. A judgement about an episode SHALL NOT be recorded as a link.

#### Scenario: Reading the links section
- **WHEN** an implementor reads the definition of `links`
- **THEN** it defines no relation to a DKF claim or an intention, and implementing it needs no other format
