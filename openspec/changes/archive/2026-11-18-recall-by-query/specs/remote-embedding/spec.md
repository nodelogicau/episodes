## ADDED Requirements

### Requirement: Remote embedding is off unless configured on the machine
An implementation SHALL NOT send any text of an episode to an embedding service on another host unless the machine it runs on is configured to. That configuration SHALL live outside the workspace, and nothing in the workspace SHALL be able to turn remote embedding on. The specification SHALL state that episodes carry no scope, so that where remote embedding is on it covers every episode the configuration does not exclude.

#### Scenario: A fresh machine
- **WHEN** an implementation with a remote embedding service available runs on a machine with no configuration
- **THEN** it sends nothing, and the semantic stage runs locally or not at all

#### Scenario: A workspace that asks for it
- **WHEN** a cloned workspace's `episodes.yaml` carries a key asking for remote embedding
- **THEN** the key is ignored, as unknown keys are, and nothing is sent

#### Scenario: Turned on
- **WHEN** the machine's configuration turns remote embedding on and excludes nothing
- **THEN** the `label` and inline `content.text` of any episode may be sent

### Requirement: Configuration may narrow remote embedding by indexed fields
The configuration MAY limit remote embedding to episodes selected by `standpoint`, `kind` or `source.harness`. An implementation that offers such limits SHALL apply them from the episode's own fields. The format SHALL NOT add a scope field to an episode on this account.

#### Scenario: Conversations only
- **WHEN** the configuration allows remote embedding for `kind: message` and no other kind
- **THEN** the text of an `email` episode's `label` is not sent

#### Scenario: No scope in the file
- **WHEN** an implementor looks for a field of an episode that says who may see it
- **THEN** the specification has told them there is none, and that the limit is the machine's

### Requirement: Fetched content needs its own setting
An implementation SHALL NOT send content fetched for a reference episode to an embedding service on another host unless the machine's configuration allows that separately from remote embedding of text the workspace holds. The setting SHALL be off by default.

#### Scenario: Remote embedding on, fetched content off
- **WHEN** remote embedding is turned on and the setting for fetched content is not
- **THEN** an email's body is embedded locally or not at all, and its `label` may be sent

#### Scenario: Both on
- **WHEN** both settings are on
- **THEN** the fetched body of an email may be sent to the service
