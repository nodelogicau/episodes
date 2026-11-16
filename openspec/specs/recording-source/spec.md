# recording-source Specification

## Purpose

Who writes episodes: harnesses and connectors. `source.harness` names whatever recorded the episode, `source.model` is present only when a model took part, and recording is kept apart from selection and consolidation. Introduced by change `acts-and-containers`.
## Requirements
### Requirement: Episodes are written by harnesses and connectors
The specification SHALL describe the format as written by harnesses and connectors, and SHALL NOT describe it as written by AI harnesses only. It SHALL state, informatively, that a connector is a writer that parses a source deterministically, and that recording a reference episode requires no model.

#### Scenario: Reading the opening
- **WHEN** an implementor reads the opening paragraph
- **THEN** it does not say that a model sits on the path by which an episode is written

#### Scenario: A mailbox sync job
- **WHEN** a job with no model reads a mailbox and writes a reference episode for a message from its headers
- **THEN** it is a conformant writer

### Requirement: `source.harness` names whatever recorded the episode
`source.harness` SHALL name the software that recorded the episode, whether an AI harness or a connector. `source.model` SHALL be present only when a model took part in recording the episode, and a writer SHALL NOT write it otherwise.

#### Scenario: A connector
- **WHEN** a mailbox connector records an email on Ben's behalf
- **THEN** it writes `source: {author: <Ben>, harness: gmail-sync}` with no `model`

#### Scenario: A transcript
- **WHEN** a harness records a transcript that a speech model produced
- **THEN** it writes `source.model` naming that model

#### Scenario: A harness that parsed without its model
- **WHEN** an AI harness records a calendar event by parsing it, with no model call
- **THEN** it writes `source.harness` and no `source.model`

### Requirement: Recording is distinguished from what follows it
The specification SHALL state, informatively, that recording an episode is separate from selecting which episodes merit interpretation and from consolidating them into another format's objects, and that only recording belongs to this format. The statement SHALL NOT require any implementation to select or consolidate.

#### Scenario: Implementing episodes alone
- **WHEN** an implementation records episodes and does nothing else with them
- **THEN** it conforms, and the informative text places no requirement on it

