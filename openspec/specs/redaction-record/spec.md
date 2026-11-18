# redaction-record Specification

## Purpose

What a `redacted` block and a withdrawn episode say: `fields` lists only paths that were present and removed, and a withdrawn inline episode is not returned as content, though its position may be shown from fields that cannot be redacted. Introduced by change `settle-edge-cases`.

## Requirements

### Requirement: `redacted.fields` lists only what was removed
A path in `redacted.fields` SHALL record that the episode carried that field and that it was removed. A writer asked to redact a path the episode does not carry SHALL refuse, naming the path, unless the episode's `redacted` block already lists it, in which case the request changes nothing for that path. A writer SHALL NOT add a path to `fields` for a field that was absent.

#### Scenario: A field the episode never had
- **WHEN** a writer is asked to redact `place` from an episode that has no `place` and no `redacted` block
- **THEN** it refuses, naming `place`, and the file is unchanged

#### Scenario: Redacting the same field again
- **WHEN** a writer is asked to redact `label` from an episode whose `redacted.fields` already lists `label`
- **THEN** it does not refuse, and `fields` lists `label` once

#### Scenario: One path present and one absent
- **WHEN** a writer is asked to redact `label` and `place` from an episode that carries `label` and not `place`
- **THEN** it refuses, naming `place`, and removes nothing

#### Scenario: Reading the block
- **WHEN** a reader finds `fields: [label, content.text]` on an episode
- **THEN** it can take it that the episode once carried a label and text

### Requirement: A withdrawn episode is not returned as content
The specification SHALL define "out of recall" for an inline episode whose `content.text` is redacted: a reader SHALL NOT return the episode as content in answer to recall. A reader MAY show that the episode exists and where it stands in its container, using only `id`, `kind`, `occurred`, `container`, `ordinal`, `standpoint` and `timestamp`. A reader SHALL NOT show anything that was redacted, from any copy it holds.

#### Scenario: A withdrawn turn in a conversation
- **WHEN** a reader shows a conversation whose seventh turn has `content.text` redacted
- **THEN** it may show a placeholder at position 7 giving the speaker and the time, and shows no text

#### Scenario: A search over turns
- **WHEN** a reader answers a request for what was said about a topic
- **THEN** a withdrawn turn is not among the results

#### Scenario: A label that was kept
- **WHEN** a turn's `content.text` is redacted and its `label` is not
- **THEN** a placeholder for the turn does not show the label, because `label` is not among the fields that cannot be redacted
