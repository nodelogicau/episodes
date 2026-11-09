# content-language Specification

## Purpose

The language of an episode's content as recorded, `content.language`: one BCP 47 tag, recorded only when the source states it or the harness set it, never from detection. On a transcript it is the language of the text, not the audio. Introduced by change `content-language`.

## Requirements

### Requirement: `content.language` holds one BCP 47 tag
An inline or reference episode MAY carry `content.language`, the language of its content as recorded. Its value SHALL be one language tag that is well-formed under BCP 47 (RFC 5646). Content in more than one language SHALL use the tag `mul`. A writer SHALL NOT write `und`; a language that is not known SHALL be left out.

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
- **WHEN** an episode carries `content.language: english`
- **THEN** a validator rejects it, naming the field

### Requirement: `language` is recorded only when known
A writer SHALL record `content.language` only when the source states the language, or when the harness produced the text in a language it set. A writer SHALL NOT record a language chosen by language detection.

#### Scenario: A stated language
- **WHEN** a harness records an email whose header is `Content-Language: fr`
- **THEN** it writes `content.language: fr`

#### Scenario: A detected language
- **WHEN** a harness records a typed turn whose language it knows only by running a detector over the text
- **THEN** it writes no `language`, and the episode is valid

### Requirement: On a reference episode, `language` is as stated when recorded
On a reference episode, `content.language` SHALL be the language the source stated when the episode was recorded. It SHALL NOT be rewritten if the source later states another. `content.media_type` SHALL NOT be required with it.

#### Scenario: A calendar event with a stated language
- **WHEN** a harness records the arranging of an event whose `SUMMARY` has `LANGUAGE=ja`
- **THEN** it writes `content.language: ja`, and the episode is valid with or without `media_type`

### Requirement: A transcript's `language` is its text's
On an episode with `derivation: transcribed` or `ocr`, `content.language` SHALL be the language of the episode's `text`, not of the audio or image it was made from. The language of the audio or image SHALL be recorded, if known, on that medium's own episode. A language detected by the recogniser SHALL NOT be recorded.

#### Scenario: A transcript made with a set language
- **WHEN** a harness transcribes a voice memo with a recogniser told to expect Japanese, and records the transcript `via` the memo's episode
- **THEN** the transcript episode carries `content.language: ja`

#### Scenario: A transcript with an auto-detected language
- **WHEN** a recogniser detects the language itself
- **THEN** the transcript episode carries no `language`

### Requirement: Content with no mode carries no language
An episode with `content: {mode: none}` SHALL NOT carry `content.language`.

#### Scenario: A container with a language
- **WHEN** a conversation container with `content.mode: none` carries `content.language`
- **THEN** a validator rejects it, naming the field

### Requirement: Case and registry checks
Writers SHALL write tags in the case RFC 5646 §2.1.1 recommends. Readers SHALL compare tags without regard to case. A validator MAY warn on a subtag not in the IANA Language Subtag Registry, and SHALL NOT reject an episode for it.

#### Scenario: Case-insensitive comparison
- **WHEN** a reader compares `EN-au` with `en-AU`
- **THEN** it treats them as the same tag

#### Scenario: An unregistered subtag
- **WHEN** an episode carries a well-formed tag with a region subtag the validator's copy of the registry lacks
- **THEN** the validator may warn, and the episode is valid

### Requirement: `language` is redactable and unindexed
`content.language` SHALL be in the closed set of redactable fields and SHALL NOT be mirrored in the index. Redacting `content.text` SHALL NOT redact `content.language`.

#### Scenario: Withdrawing an inline episode
- **WHEN** a person redacts `content.text` from an episode carrying `content.language`
- **THEN** `language` stays unless `redacted.fields` also lists `content.language`, and no index entry changes
