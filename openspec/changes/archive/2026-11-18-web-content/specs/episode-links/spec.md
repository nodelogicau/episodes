## MODIFIED Requirements

### Requirement: `links` follows RFC 8288
An episode MAY carry `links`, a list of mappings each with the keys `rel` and `href`, optionally `anchor`, and no other key. `rel` SHALL be a relation type registered in the IANA Link Relations registry, written in lowercase and used in its registered meaning, or an absolute URI. `href` SHALL be an episode id, which is resolved within the workspace, or a URI. A reader SHALL NOT reject an episode for a `rel` it does not know.

A `rel` SHALL be invalid only when it is neither an absolute URI nor of the form RFC 8288 gives a registered relation type: a lowercase letter followed by lowercase letters, digits, `.` or `-`. A validator SHALL warn on, and SHALL NOT reject, a `rel` of that form that its copy of the registry lacks. A writer SHALL NOT write such a `rel`.

A link with no `anchor` SHALL be about the episode. A link with `anchor` SHALL be about the content the episode refers to. The value of `anchor` SHALL equal the episode's `content.ref`, character for character, and a validator SHALL reject any other value. `anchor` SHALL NOT appear on an episode that carries no `content.ref`. No other use of `anchor` is admitted.

A writer SHALL sort `links` by `rel` and then by `href`, comparing each by Unicode code point, and SHALL write a link with no `anchor` before a link with the same `rel` and `href` that has one.

#### Scenario: A registered relation
- **WHEN** an episode carries `links: [{rel: via, href: epi_01a1…}]`
- **THEN** the episode is valid

#### Scenario: An extension relation
- **WHEN** an episode carries a link whose `rel` is `https://www.w3.org/ns/activitystreams#inReplyTo`
- **THEN** a reader accepts it and gives it no meaning under this format

#### Scenario: A non-URI unregistered relation
- **WHEN** an episode carries `rel: answers`, which has the form of a registered relation and is missing from the validator's copy of the registry
- **THEN** the episode is valid, and the validator warns, naming the link

#### Scenario: A relation registered after the validator was built
- **WHEN** an episode carries a `rel` that IANA registered after a validator's copy of the registry was taken
- **THEN** that validator warns, a validator with a newer copy does not, and both find the episode valid

#### Scenario: A relation of neither form
- **WHEN** an episode carries `rel: Answers` or `rel: "my relation"`, which is neither an absolute URI nor of the registered form
- **THEN** a validator rejects it, naming the link

#### Scenario: A writer asked for an unregistered relation
- **WHEN** a writer is asked to record a link with `rel: answers`, which its copy of the registry lacks
- **THEN** it refuses, and writes nothing

#### Scenario: A link about the referenced content
- **WHEN** a reference episode with `content.ref: https://example.com/report` carries `links: [{rel: canonical, href: https://example.org/report, anchor: https://example.com/report}]`
- **THEN** the episode is valid, and the link says that the referenced page's canonical form is at the `href`

#### Scenario: An anchor that is not the ref
- **WHEN** a reference episode with `content.ref: https://example.com/report` carries a link whose `anchor` is `https://example.com/other`
- **THEN** a validator rejects it, naming the link

#### Scenario: An anchor on an inline episode
- **WHEN** an inline episode carries a link with `anchor`
- **THEN** a validator rejects it, naming the link

#### Scenario: An unknown key on a link
- **WHEN** a link carries a key other than `rel`, `href` and `anchor`
- **THEN** a validator rejects it, naming the link
