## ADDED Requirements

### Requirement: A writer avoids a second recording of the same content
A writer that can see the workspace SHOULD NOT record a reference episode whose `standpoint`, `content.media_type` and `content.uid` all equal those of an existing reference episode, unless it is told explicitly that the content is a distinct thing. A writer that declines SHOULD name the existing episode, so that whatever asked can cite it. A second such episode SHALL remain valid.

#### Scenario: A connector runs again
- **WHEN** a connector that recorded an email yesterday meets the same email today, with the same standpoint, media type and `uid`
- **THEN** it does not record a second episode, and reports the id of the first

#### Scenario: An instance of a recurring event
- **WHEN** a writer is asked to record one instance of a weekly meeting, whose `UID` an earlier episode from the same standpoint already carries, and is told it is a distinct occurrence
- **THEN** it records the episode

#### Scenario: Two machines
- **WHEN** two machines each record one email before either has the other's episode, and the workspaces merge
- **THEN** both episodes are valid, and a validator may report them as possible duplicates
