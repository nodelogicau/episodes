## ADDED Requirements

### Requirement: `hash` covers the representation `media_type` names
`content.hash` on a reference episode SHALL be taken over these bytes, before the line-ending rule is applied:

- for `message/rfc822`, the complete raw message, headers and body, as the mailbox stores it;
- for `text/calendar`, the iCalendar object that holds the event, as the calendar store returns it;
- for any other media type, the bytes of the content in that representation;
- with no `media_type`, the bytes that `ref` returns.

A writer SHOULD write `media_type` whenever it writes `hash`.

#### Scenario: An email fetched raw
- **WHEN** a writer fetches a message's raw RFC 822 bytes and records it with `media_type: message/rfc822`
- **THEN** its `hash` is taken over those bytes, headers included

#### Scenario: Two fetches of one message
- **WHEN** one writer fetches a stored message over IMAP and another fetches the same stored message through a provider's raw-message call
- **THEN** both write the same `hash`

#### Scenario: A calendar event
- **WHEN** a writer fetches an event from a CalDAV store and records it with `media_type: text/calendar`
- **THEN** its `hash` is taken over the iCalendar object the store returned

#### Scenario: A file
- **WHEN** a writer records a PDF in storage with `media_type: application/pdf`
- **THEN** its `hash` is taken over the file's bytes

### Requirement: No `hash` without the named bytes
A writer that does not hold the bytes the previous requirement names SHALL NOT write `hash`. In particular it SHALL NOT write, under a media type, a hash of a provider's own rendering of the content. It SHALL record `version` where the source has one.

#### Scenario: A message as provider JSON
- **WHEN** a writer holds only a provider API's JSON for a message and records it with `media_type: message/rfc822`
- **THEN** it writes no `hash`

#### Scenario: A calendar event as provider JSON
- **WHEN** a writer holds only a provider API's JSON for an event, which carries an ETag
- **THEN** it writes no `hash`, and records the ETag as `version`

#### Scenario: A reader checking the source
- **WHEN** a reader fetches the raw message for an episode with `media_type: message/rfc822` and a `hash`
- **THEN** it can compare the two, because the hash was taken over the same representation

### Requirement: A hash identifies one stored copy
The specification SHALL state that `hash` identifies the copy of the content that the episode's `ref` points at, that copies of one message held by different people differ, and that the identity of content across copies is `uid`. A reader SHALL NOT conclude from differing hashes that episodes with different standpoints record different content.

#### Scenario: Two recipients
- **WHEN** Ben's episode and Jane's episode record one email with the same `uid`, and their hashes differ because each mailbox added its own `Received` headers
- **THEN** a reader does not take them for different messages

#### Scenario: One mailbox, two machines
- **WHEN** two machines record the same message from the same mailbox, each from the raw bytes
- **THEN** the two episodes carry the same `hash`
