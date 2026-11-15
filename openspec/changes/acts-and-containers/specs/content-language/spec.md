## MODIFIED Requirements

### Requirement: Content with no mode carries no language
An episode with `content: {mode: none}` or `content: {mode: attested}` SHALL NOT carry `content.language`.

#### Scenario: A container with a language
- **WHEN** a conversation container with `content.mode: none` carries `content.language`
- **THEN** a validator rejects it, naming the field

#### Scenario: An act with a language
- **WHEN** a self-attested act with `content.mode: attested` carries `content.language`
- **THEN** a validator rejects it, naming the field
