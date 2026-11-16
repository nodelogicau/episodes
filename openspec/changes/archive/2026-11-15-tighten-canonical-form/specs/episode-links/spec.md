## MODIFIED Requirements

### Requirement: `links` follows RFC 8288
An episode MAY carry `links`, a list of mappings each with exactly the keys `rel` and `href`. `rel` SHALL be a relation type registered in the IANA Link Relations registry, written in lowercase and used in its registered meaning, or an absolute URI. `href` SHALL be an episode id, which is resolved within the workspace, or a URI. A writer SHALL sort `links` by `rel` and then by `href`, comparing each by Unicode code point. A reader SHALL NOT reject an episode for a `rel` it does not know.

A `rel` SHALL be invalid only when it is neither an absolute URI nor of the form RFC 8288 gives a registered relation type: a lowercase letter followed by lowercase letters, digits, `.` or `-`. A validator SHALL warn on, and SHALL NOT reject, a `rel` of that form that its copy of the registry lacks. A writer SHALL NOT write such a `rel`.

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
