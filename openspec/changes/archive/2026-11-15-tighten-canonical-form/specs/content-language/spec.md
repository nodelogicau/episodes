## MODIFIED Requirements

### Requirement: `content.language` holds one BCP 47 tag
An inline or reference episode MAY carry `content.language`, the language of its content as recorded. Its value SHALL be one language tag that is well-formed under BCP 47 (RFC 5646). Well-formed SHALL mean that the tag matches the grammar of RFC 5646 §2.1, which can be checked without the IANA Language Subtag Registry. Content in more than one language SHALL use the tag `mul`. A writer SHALL NOT write `und`; a language that is not known SHALL be left out.

#### Scenario: A rendered summary
- **WHEN** a harness records text it rendered from structured data in Australian English
- **THEN** it writes `content.language: en-AU`

#### Scenario: A bilingual email
- **WHEN** an email's header is `Content-Language: en, ja` and neither is the main language
- **THEN** the writer records `content.language: mul`

#### Scenario: Undetermined
- **WHEN** an episode carries `content.language: und`
- **THEN** a validator rejects it, naming the field

#### Scenario: An ill-formed tag
- **WHEN** an episode carries `content.language: en_AU`
- **THEN** a validator rejects it, naming the field

#### Scenario: A well-formed tag that names no language
- **WHEN** an episode carries `content.language: english`, which matches the grammar as a primary language subtag of seven letters and is not in the registry
- **THEN** the episode is valid, and a validator may warn
