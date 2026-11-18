# archived-snapshots Specification

## Purpose

The `memento` relation on a reference episode: what it names and that it requires `anchor`, when a snapshot may be linked, that archiving needs an explicit request, how a reader uses a snapshot, and that a snapshot is not proof of the content. Introduced by change `web-content`.

## Requirements

### Requirement: `memento` names an archived snapshot of the referenced content
On a reference episode, a link with `rel: memento` and `anchor` SHALL mean that its `href` is an archived snapshot, in the sense of RFC 7089, of the content `content.ref` points at, as that content was when the episode was recorded. Its `href` SHALL be a URI and SHALL NOT be an episode id. A `memento` link with no `anchor` SHALL be invalid. An episode MAY carry more than one `memento` link.

#### Scenario: A web page with a snapshot
- **WHEN** a reference episode with `content.ref: https://example.com/report` carries `links: [{rel: memento, href: https://web.archive.org/web/20261107031500/https://example.com/report, anchor: https://example.com/report}]`
- **THEN** the episode is valid

#### Scenario: A memento with no anchor
- **WHEN** an episode carries `links: [{rel: memento, href: https://web.archive.org/web/20261107031500/https://example.com/report}]` with no `anchor`
- **THEN** a validator rejects it, naming the link

#### Scenario: Two archives
- **WHEN** a reference episode carries two `memento` links to snapshots held by different archives
- **THEN** the episode is valid

### Requirement: A snapshot is linked only when the episode is recorded
A writer SHALL write a `memento` link only when it records the episode, and SHALL NOT add one afterwards. The snapshot SHALL be one the writer caused to be made while recording, or an existing one the writer has compared with the content it fetched and found to be the same content.

#### Scenario: A snapshot made while recording
- **WHEN** a person asks a writer to record a page and archive it, and the writer obtains a snapshot before writing the episode
- **THEN** the episode is written with the `memento` link

#### Scenario: An existing snapshot
- **WHEN** a writer finds that an archive already holds a snapshot of the page, and the snapshot's content is the content the writer fetched
- **THEN** it may link that snapshot

#### Scenario: A snapshot made later
- **WHEN** a snapshot of the page is made a week after the episode was recorded
- **THEN** no writer adds a link to it, because links are written once

#### Scenario: An older snapshot of a page that has since changed
- **WHEN** an archive holds a snapshot from last year, and the page the writer fetched today differs from it
- **THEN** the writer does not link that snapshot

### Requirement: Archiving needs an explicit request
A writer SHALL NOT cause content to be submitted to an archive unless the person on whose behalf it records has explicitly asked for that content to be archived. Recording an episode SHALL NOT of itself be such a request.

#### Scenario: Recording without archiving
- **WHEN** a person asks a writer to record a page and says nothing about archiving
- **THEN** the writer submits nothing to any archive

#### Scenario: A private page
- **WHEN** a writer records a page that requires the person's credentials to read
- **THEN** it does not submit the page to an archive unless the person has asked for that page to be archived

### Requirement: A reader may fall back to a snapshot
A reader that cannot fetch the content as recorded, because the source is `changed`, `unreachable` or `gone`, MAY fetch a `memento` link's `href` in its place. It SHALL present what it fetched as an archive's copy and not as the source. Using a snapshot SHALL NOT change the episode's `source_status`, which describes the source. A writer SHALL NOT copy a snapshot's content into the episode.

#### Scenario: The page is gone
- **WHEN** an episode's `source_status.state` is `gone` and the episode carries a `memento` link
- **THEN** a reader may show the snapshot, says that it is an archived copy, and the state stays `gone`

#### Scenario: The page has changed
- **WHEN** an episode's `source_status.state` is `changed` and the episode carries a `memento` link
- **THEN** a reader may show the snapshot as the content at the time of recording

#### Scenario: No back-fill
- **WHEN** a source is found to be `gone` and a snapshot of it can still be fetched
- **THEN** no writer adds the snapshot's text to the episode

### Requirement: A snapshot is not proof of the content
The specification SHALL state that an archive may serve a page with changes of its own, so a snapshot need not match `content.hash`. A reader MAY compare a snapshot with `content.hash`. It SHALL report a snapshot that does not match as unverified, and SHALL NOT treat the episode as invalid or the source as `changed` on that account.

#### Scenario: A rewritten page
- **WHEN** a reader fetches a snapshot whose links the archive has rewritten, and its hash differs from `content.hash`
- **THEN** the reader reports the snapshot as unverified, and the episode is valid

#### Scenario: A matching snapshot
- **WHEN** a reader fetches a snapshot whose hash equals `content.hash`
- **THEN** it may report the snapshot as verified
