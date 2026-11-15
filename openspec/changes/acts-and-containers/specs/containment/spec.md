## ADDED Requirements

### Requirement: `mode: none` is a container with nothing of its own
`content: {mode: none}` SHALL mean that the episode is a container with no content of its own, such as a conversation whose turns are its children. Such an episode SHALL be valid whatever its `standpoint`, and whether or not any episode names it as `container`. A validator SHALL warn, naming the episode, on one that no episode in the workspace names as `container`, and SHALL NOT reject it. A writer SHOULD write a container together with its first child.

#### Scenario: A conversation and its turns
- **WHEN** a conversation episode with `content: {mode: none}` is named as `container` by its turns
- **THEN** it is valid, and a validator does not warn

#### Scenario: The first turn was never written
- **WHEN** a writer crashes after writing a conversation container and before writing its first turn
- **THEN** the container is valid, and a validator warns that it has no children, naming it

#### Scenario: The first turn arrives later
- **WHEN** a turn naming that container is then written
- **THEN** the warning no longer applies, and no existing file has changed

### Requirement: A container with nothing of its own is its keeper's
The `standpoint` of an episode with `content: {mode: none}` SHALL be the person or agent whose record the container is. It SHALL imply nothing about who spoke or acted within the container: each child states its own `standpoint`. A container that has content of its own SHALL keep the standpoint its content gives it.

#### Scenario: A conversation with a harness
- **WHEN** a harness records Ben's conversation with it
- **THEN** the conversation container's `standpoint` is Ben, and each turn's `standpoint` is its speaker

#### Scenario: A mail thread
- **WHEN** a writer records a thread from Ben's mailbox as a container, with messages sent by Jane
- **THEN** the thread's `standpoint` is Ben, and each message's `standpoint` is its sender

#### Scenario: An email with attachments
- **WHEN** an email sent by Jane is the `container` of its attachments
- **THEN** the email's `standpoint` is Jane, as for any email

#### Scenario: Filtering by standpoint
- **WHEN** a reader lists episodes whose `standpoint` is Ben and finds a conversation container
- **THEN** it does not conclude that Ben spoke every turn in it

### Requirement: A container is recorded before its children
A writer SHALL record a container before any episode that names it as `container`. A validator SHALL warn, naming the child, when the child's id and its container's id are both UUID version 7 and the container's id sorts later. It SHALL NOT apply the check when either id is not a UUID version 7.

#### Scenario: Written in order
- **WHEN** a writer records a conversation and then its first turn
- **THEN** the container's id sorts before the turn's

#### Scenario: A container minted later
- **WHEN** a turn's `container` names an episode whose UUIDv7 id sorts after the turn's own
- **THEN** a validator warns, naming the turn, and the turn is valid

#### Scenario: A legacy id
- **WHEN** a turn's `container` names an episode whose id is not a UUID version 7
- **THEN** a validator makes no check of the order

### Requirement: An unresolved `container` is reported, not invalid
A `container` whose episode id does not resolve in the workspace, because the container was dropped or never copied, SHALL be reported as unresolved and SHALL NOT make the episode invalid.

#### Scenario: A partial copy
- **WHEN** a workspace holds a turn whose container was not copied with it
- **THEN** a validator reports the `container` as unresolved, naming the turn, and the turn is valid
