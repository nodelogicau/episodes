## ADDED Requirements

### Requirement: `content.uid` holds the content's own identifier
A reference episode MAY carry `content.uid`, the identifier that the content's own format assigns to it, as the source gave it. Where that format defines a URI form for its identifier, `uid` SHALL be written in that form. Otherwise it SHALL be written verbatim. For mail, `uid` SHALL be the `Message-ID` written as a `mid:` URI (RFC 2392), with the angle brackets removed and the value percent-encoded as RFC 2392 requires. For iCalendar content, `uid` SHALL be the `UID` property value, written verbatim. A writer SHALL record `uid` whenever the source exposes one.

#### Scenario: An email
- **WHEN** a harness records an email whose header is `Message-ID: <CAF3x9q@mail.example.com>`
- **THEN** it writes `content.uid: mid:CAF3x9q@mail.example.com` beside the provider's `ref`

#### Scenario: A calendar event
- **WHEN** a harness records the arranging of an event whose iCalendar `UID` is `7q2m4k9d0s1a@google.com`
- **THEN** it writes `content.uid: 7q2m4k9d0s1a@google.com`

#### Scenario: A source with no identifier
- **WHEN** a harness records a file from storage
- **THEN** it writes no `uid`, and the episode is valid

### Requirement: `media_type` is required with `uid`
When `content.uid` is present, `content.media_type` SHALL be present, and it SHALL say which format's identifier `uid` is.

#### Scenario: `uid` without a media type
- **WHEN** a reference episode carries `uid` and no `media_type`
- **THEN** a validator rejects it, naming the field

### Requirement: `uid` is identity, `ref` is location
`content.ref` SHALL keep its meaning, which is whatever can fetch the content. `content.uid` SHALL NOT be used as a locator in place of `ref`, and `ref` SHALL NOT be taken as the content's identity. An inline episode SHALL NOT carry `uid`.

#### Scenario: `uid` on an inline episode
- **WHEN** an inline episode carries `content.uid`
- **THEN** a validator rejects it, naming the field

### Requirement: Content can be found again by `uid`
A reader whose `ref` does not resolve MAY search the source for the content by `uid`. Content found that way SHALL be observed as `available`, or as `changed` if its hash or version differs, and SHALL NOT be observed as `gone`. The episode's `ref` SHALL NOT be rewritten. A source SHALL be observed as `gone` only when the content cannot be found by `ref` or, where `uid` is present, by `uid`.

#### Scenario: A mailbox migration
- **WHEN** an email episode's provider `ref` no longer resolves after the person moves mail providers, and a search of the new mailbox by its `mid:` finds the message with a matching hash
- **THEN** the reader records `source_status.state: available` and leaves `ref` unchanged

### Requirement: Possible duplicates are reported, never rejected
A validator MAY report reference episodes that share `standpoint`, `content.media_type` and `content.uid` as possible duplicates. It SHALL NOT reject an episode for sharing them.

#### Scenario: One email recorded on two machines
- **WHEN** two episodes with different ids both record the same email, from the same standpoint, with the same `uid`
- **THEN** a validator may report them as possible duplicates, and both remain valid

#### Scenario: Different standpoints
- **WHEN** Ben's episode and Jane's episode carry the same `uid`
- **THEN** they are not reported as duplicates

### Requirement: `uid` is redactable and unindexed
`content.uid` SHALL be in the closed set of redactable fields and SHALL NOT be mirrored in the index.

#### Scenario: Redacting a Message-ID
- **WHEN** a person redacts `content.uid`
- **THEN** it is absent from the file, `redacted.fields` lists `content.uid`, and no index entry changes
