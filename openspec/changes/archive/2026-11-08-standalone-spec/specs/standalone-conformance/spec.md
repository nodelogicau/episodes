## ADDED Requirements

### Requirement: Episodes reference no other format's objects
The specification SHALL define no episode field whose value is an identifier of an object defined by another format. In particular, `EPISODE` SHALL NOT define `occasion`.

#### Scenario: Validating with no sibling workspace
- **WHEN** a validator checks an episodes workspace with no DKF or intentions workspace present
- **THEN** it can decide whether every episode is valid, without resolving any reference

#### Scenario: A draft file carries `occasion`
- **WHEN** a reader encounters an `occasion` key on an episode
- **THEN** it treats the key as a field an implementation added, does not reject the file, and gives the key no meaning

### Requirement: Identities are defined without another format's object model
The specification SHALL define `source.author`, `standpoint`, `participants` and `place` as a URI where one is known, otherwise a string identifier. It SHALL state that resolving them is outside the format, and that a value nobody can resolve is still valid.

#### Scenario: A standpoint with no resolvable identity
- **WHEN** an episode's `standpoint` is a string identifier that resolves to nothing
- **THEN** the episode is valid

#### Scenario: Reading the definition
- **WHEN** an implementor reads the definitions of `author`, `standpoint`, `participants` and `place`
- **THEN** none of them requires knowing what a DKF particular is

### Requirement: The content hash is fully specified in the document
The specification SHALL define `content.hash` completely: SHA-256 over the content, with CRLF sequences normalised to LF and nothing else changed (no trailing whitespace, Unicode form or final-newline changes), written as `<algorithm>:<digest>`. Writers SHALL write `sha256`. Readers SHALL accept any `<algorithm>:<digest>` and SHALL report an algorithm they do not implement as unverified, not invalid.

#### Scenario: Line endings differ
- **WHEN** content is fetched with CRLF line endings and was hashed with LF line endings
- **THEN** the hashes match

#### Scenario: Unknown algorithm
- **WHEN** a reader meets `hash: blake3:…` and does not implement BLAKE3
- **THEN** it reports the hash as unverified and does not reject the episode

### Requirement: Redaction is fully specified in the document
The specification SHALL state every redaction rule that applies to episodes, without deferring to another specification. These are:
- the required block fields;
- the closed set of redactable paths;
- that a required field is valid when absent only because the block lists it;
- that a file carries at most one block, and further redaction merges into it;
- that redaction is irreversible and never implicit;
- that it does not cascade;
- the statement of what redaction does not remove, including the MUST for git-backed stores.

#### Scenario: A redacted inline episode lacks text
- **WHEN** an inline episode has no `content.text` and its `redacted.fields` lists `content.text`
- **THEN** the episode is valid

#### Scenario: Text missing with no redaction
- **WHEN** an inline episode has no `content.text` and no `redacted` block lists it
- **THEN** a validator rejects the file

#### Scenario: Redacting twice
- **WHEN** a writer redacts `label` from an episode whose `redacted.fields` is already `[content.text]`
- **THEN** the file has one `redacted` block, with the new `timestamp`, `reason` and `source` and with `fields` `[content.text, label]`

### Requirement: Sharding and the index are fully specified in the document
The specification SHALL state, without deferring to another specification:
- that a file's path derives from its id alone, under the UTC month of the id's minting instant;
- the `legacy/` directory for ids with no derivable month;
- the sealing rule, with one month of grace;
- exactly which changes a file in a sealed month may undergo;
- the shape of the root index and of sealed segments, including segment `count`;
- late-merge detection;
- validation of future-dated ids.

#### Scenario: Deriving a path
- **WHEN** an episode id was minted on 2026-11-07 UTC
- **THEN** its file is `episodes/2026-11/<id>.yaml`

#### Scenario: Changing a sealed month
- **WHEN** a writer changes an episode in a sealed month by anything other than rewriting `source_status` or adding to `redacted`
- **THEN** the change is non-conformant

#### Scenario: A late merge
- **WHEN** the number of files in a sealed month's directory differs from its segment's `count`
- **THEN** validation fails, naming the files

#### Scenario: An id far in the future
- **WHEN** a validator finds an id minted two or more months after the validator's current month
- **THEN** validation fails, naming the episode

### Requirement: Text about other formats is informative
The specification SHALL contain a Conformance section stating which sections are normative. All text describing DKF, intentions or the family of formats SHALL be informative and SHALL place no requirement on an episodes implementation.

#### Scenario: Implementing episodes alone
- **WHEN** an implementor builds a writer, reader and validator from the normative sections only
- **THEN** the implementation conforms, with no DKF or intentions code or data

#### Scenario: A sibling format is mentioned
- **WHEN** a normative section mentions DKF or intentions
- **THEN** the mention is labelled informative, or only says what an episode does not hold
