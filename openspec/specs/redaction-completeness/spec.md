# redaction-completeness Specification

## Purpose

What a redaction is guaranteed to remove: redacting `content.ref` also redacts `content.uid`, `content.version`, `content.hash` and `links`; what a reference episode keeps afterwards; and values derived from a redacted field are deleted or recomputed, and not used in the meantime. Introduced by change `redaction-completeness`.
## Requirements
### Requirement: Redacting `content.ref` redacts what locates or identifies the content
A `redacted` block whose `fields` lists `content.ref` SHALL also list each of `content.uid`, `content.version`, `content.hash` and `links` that the episode carries, and each SHALL be absent from the file. A writer asked to redact `content.ref` SHALL redact them in the same act. A validator SHALL reject a file whose block lists `content.ref` while any of the four is present. Each of the four SHALL remain redactable without `content.ref`.

#### Scenario: Redacting the ref of an email
- **WHEN** a writer is asked to redact `content.ref` from an email episode that carries `content.uid`, `content.version`, `content.hash` and `links`
- **THEN** all five are absent from the file, and `redacted.fields` lists all five

#### Scenario: An episode with a ref and nothing else
- **WHEN** a writer is asked to redact `content.ref` from an episode that carries none of the four
- **THEN** `redacted.fields` gains `content.ref` and no other path on that account

#### Scenario: A `uid` left behind
- **WHEN** a file's `redacted.fields` lists `content.ref` and the file still carries `content.uid`
- **THEN** a validator rejects it, naming `content.uid`

#### Scenario: A snapshot link left behind
- **WHEN** a file's `redacted.fields` lists `content.ref` and the file still carries `links` holding an archived snapshot of the content
- **THEN** a validator rejects it, naming `links`

#### Scenario: Repairing an earlier redaction
- **WHEN** an episode redacted under the earlier draft lists `content.ref` and still carries `content.uid`, and a writer redacts `content.uid`
- **THEN** the block's `fields` is the union of old and new, and the file is valid

#### Scenario: Redacting `uid` alone
- **WHEN** a person redacts `content.uid` and not `content.ref`
- **THEN** the file is valid, and `ref`, `version`, `hash` and `links` remain

### Requirement: What a reference episode keeps is stated
The specification SHALL state what a reference episode holds after `content.ref` is redacted: its `id`, `kind`, `occurred`, `standpoint`, `container`, `ordinal` and `timestamp`, its `content.mode` and `content.media_type`, and whichever of `label`, `participants`, `place` and `content.language` were not redacted as well. It SHALL state that redacting `content.ref` is not a side effect, because every field it removes is named in `fields`.

#### Scenario: Reading a tombstone
- **WHEN** a reader meets a reference episode whose `content.ref` is redacted
- **THEN** it finds no `uid`, `version`, `hash` or `links`, and can still read when the happening occurred, from whose standpoint, and of what kind

#### Scenario: A label that says where
- **WHEN** a person redacts `content.ref` and leaves a `label` that names the document
- **THEN** the file is valid, because `label` is redacted only when the person lists it

### Requirement: Derived values of a redacted field are deleted or recomputed
An implementation that keeps values derived from an episode's fields SHALL, when a field is redacted, delete each value derived from it or compute the value again without it. Derived values SHALL include embeddings, classifier and other model outputs, summaries and extractions, and search indexes. A value SHALL be taken as derived from a field when computing it again without that field could change it.

#### Scenario: An embedding
- **WHEN** an implementation holds an embedding of a turn's `content.text`, and `content.text` is redacted
- **THEN** it deletes the embedding

#### Scenario: A topic score
- **WHEN** an implementation holds a classifier's score for a turn, computed from its `content.text`, and `content.text` is redacted
- **THEN** it deletes the score

#### Scenario: A full-text index
- **WHEN** an implementation holds a full-text index over `label`, and an episode's `label` is redacted
- **THEN** it removes that episode's label terms from the index

#### Scenario: A value from two fields
- **WHEN** an implementation holds a summary computed from an episode's `label` and `content.text`, and only `label` is redacted
- **THEN** it deletes the summary, or computes it again from `content.text` alone

#### Scenario: A value from no redacted field
- **WHEN** an implementation holds a count of an episode's children, and the episode's `label` is redacted
- **THEN** the count is not derived from `label`, and it is kept

### Requirement: A derived value of a redacted field is not used
An implementation SHALL NOT read, return, rank by or otherwise use a value derived from a field that the episode's file lists as redacted, whether or not the value has been deleted. It SHALL decide this from the episode file, not from the state of its own stores.

#### Scenario: A redaction pulled from another machine
- **WHEN** a redaction of a turn's `label` made on one machine reaches a second machine, whose store still holds an embedding of that label
- **THEN** the second machine does not return the turn on the strength of that embedding

#### Scenario: A stale index
- **WHEN** a search index still holds terms from a `content.text` that the episode's file lists as redacted
- **THEN** a query matching those terms does not return the episode on their account

### Requirement: An object of another format is not a derived value
The specification SHALL state, informatively, that a judgement written as an object of another format, such as a claim that cites an episode, is not a derived value under these rules, that it is governed by that format's own redaction, and that this is why redaction does not cascade.

#### Scenario: A claim citing a redacted episode
- **WHEN** an episode's `content.text` is redacted, and a claim in a sibling workspace quotes it
- **THEN** nothing in this format requires the claim to change

