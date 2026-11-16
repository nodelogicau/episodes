## ADDED Requirements

### Requirement: A writer does not reuse an `ordinal`
A writer SHALL NOT write an episode whose `container` and `ordinal` both equal those of another episode it can see in the workspace.

#### Scenario: A replayed turn
- **WHEN** a writer is asked to record a turn with `ordinal: 7` in a conversation that already has a turn with `ordinal: 7`
- **THEN** it refuses, naming the existing episode, and writes nothing

#### Scenario: The same ordinal in another container
- **WHEN** a writer records a turn with `ordinal: 7` in a conversation with no such turn, and another conversation has one
- **THEN** it writes the episode

### Requirement: How a writer chooses an `ordinal`
Where the source gives its parts positions, as the pages of a document or the attachments of an email do, a writer SHALL write those positions, counted from 1. Otherwise a writer SHALL write one more than the highest `ordinal` held by an episode in the container, and 1 when none holds one. An `ordinal` SHALL NOT be invalid for leaving a gap.

#### Scenario: The next turn
- **WHEN** a writer records a turn in a conversation whose turns hold ordinals 1 to 6
- **THEN** it writes `ordinal: 7`

#### Scenario: The first child
- **WHEN** a writer records the first turn of a conversation
- **THEN** it writes `ordinal: 1`

#### Scenario: Pages of a scan
- **WHEN** a writer records only pages 2 and 5 of a scanned document as children of its episode
- **THEN** it writes `ordinal: 2` and `ordinal: 5`, and both are valid

#### Scenario: After a gap
- **WHEN** a container's children hold ordinals 1, 2 and 9, and the source gives no positions
- **THEN** the writer writes `ordinal: 10` for the next child

### Requirement: A repeated `ordinal` is reported, not invalid
A validator SHALL warn, naming both episodes, when two episodes share a `container` and an `ordinal`. It SHALL NOT reject either.

#### Scenario: Two branches
- **WHEN** two branches each record a turn with `ordinal: 8` in one conversation, and the branches merge
- **THEN** a validator warns, naming both turns, and both are valid

### Requirement: Children are ordered by `ordinal`, then by id
A reader that presents the children of a container in order SHALL order them by ascending `ordinal`, and those that share an `ordinal` by id, compared by Unicode code point. Children with no `ordinal` SHALL follow those with one, ordered by id.

#### Scenario: A shared ordinal
- **WHEN** a reader lists a conversation in which two turns hold `ordinal: 8`
- **THEN** it lists the one with the lower id first, between the turns with ordinals 7 and 9

#### Scenario: Children without an ordinal
- **WHEN** a container has two children with ordinals 1 and 2 and two with none
- **THEN** a reader lists the two with ordinals first, then the other two by id
