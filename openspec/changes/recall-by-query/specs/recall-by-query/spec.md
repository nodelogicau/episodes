## ADDED Requirements

### Requirement: Recall by query is specified in the document
The specification SHALL define, in its own text and without requiring DKF, what an implementation that answers a free-text query returns. It SHALL state that an implementation need not answer free-text queries, and that one which does follows these rules. It SHALL name, informatively, the DKF section the rules were restated from.

#### Scenario: An implementation with no query operation
- **WHEN** an implementation reads, writes and validates episodes and offers no free-text query
- **THEN** it is conformant

#### Scenario: Reading the format alone
- **WHEN** an implementor builds recall by query from the episodes document only
- **THEN** every rule it needs is stated there

### Requirement: A baseline that needs no model runs on every query
An implementation that answers a free-text query SHALL resolve it without a model, as follows, on every query.

- Whitespace SHALL be trimmed from the edges of the query. The query's terms SHALL be its runs of non-whitespace characters.
- From each term, and from the whole query, leading and trailing characters of Unicode general category P SHALL be removed, as written and before folding. Interior characters SHALL be kept.
- A term that is empty after trimming SHALL be ignored. A query that is empty after trimming SHALL resolve nothing, and SHALL NOT be an error.
- A text SHALL match when the trimmed whole query, or any one trimmed term, occurs in it under Unicode case folding. Terms combine by OR.
- The texts SHALL be an episode's `label`, and the `content.text` of an inline episode.
- An episode SHALL also match when a term, before or after trimming, equals its `content.uid` exactly, with no folding.

The baseline SHALL NOT apply stemming, stopwords or any other change to terms. The specification SHALL state that the baseline is linear in history.

#### Scenario: A question mark
- **WHEN** the query is `timeout?` and a turn's `content.text` contains "the session timeout is ten minutes"
- **THEN** the turn matches

#### Scenario: Any one term
- **WHEN** the query is `what is the session timeout` and an episode's `label` is "Timeout review"
- **THEN** the episode matches, on the term `timeout`

#### Scenario: Interior punctuation
- **WHEN** the query is `v1.2.3.` and a turn's text contains "released v1.2.3 today"
- **THEN** the turn matches, because only the trailing full stop is removed

#### Scenario: An empty query
- **WHEN** the query is `?!`
- **THEN** nothing is resolved, and no error is raised

#### Scenario: A message identifier
- **WHEN** the query is `mid:20261107.1424@example.org` and a reference episode's `content.uid` is that value
- **THEN** the episode matches

#### Scenario: A reference episode's content
- **WHEN** the query is a word that appears in the body of an email and not in its episode's `label`
- **THEN** the baseline does not match the episode, because the workspace does not hold the body

#### Scenario: No stemming
- **WHEN** the query is `dog's` and a turn's text contains "the dog barked"
- **THEN** the baseline does not match on that account

### Requirement: Other stages only add
An implementation MAY run other stages, such as a semantic stage. A stage other than the baseline MAY add episodes to the result and SHALL NOT remove an episode the baseline found.

#### Scenario: A name the model handles badly
- **WHEN** the query is a ticket number that appears in one turn's text, and a semantic stage ranks that turn low
- **THEN** the turn is in the result, because the baseline found it

#### Scenario: A paraphrase
- **WHEN** the query shares no term with a turn, and a semantic stage proposes the turn
- **THEN** the turn may be in the result

### Requirement: A query resolves to episodes, each carrying `resolution`
Each result SHALL be one episode. An episode SHALL NOT be returned because another episode matched, so a container is returned only when its own `label`, text or `content.uid` matched or a stage proposed it. Each result SHALL carry `resolution`, the first of these that applies:

- `uid`, when a term equalled the episode's `content.uid`;
- `lexical`, when the baseline matched otherwise;
- `semantic`, when only another stage proposed the episode.

An implementation MAY report which field, and which span of `content.text`, matched.

#### Scenario: A turn matches and its conversation does not
- **WHEN** a turn's text matches the query and its container's `label` does not
- **THEN** the turn is returned, carrying its `container`, and the container is not a result

#### Scenario: Found two ways
- **WHEN** the baseline matches a turn's text and a semantic stage also proposes the turn
- **THEN** the turn's `resolution` is `lexical`

#### Scenario: Found by identifier
- **WHEN** a term equals an episode's `content.uid` and another term occurs in its `label`
- **THEN** its `resolution` is `uid`

### Requirement: Results are returned in a fixed order
Results SHALL be ordered by `resolution`: `uid`, then `lexical`, then `semantic`. Within `uid` and within `lexical`, they SHALL be ordered by the number of the query's distinct trimmed terms, compared under case folding, that matched the episode, most first, and then by `id` in descending Unicode code point order. Order within `semantic` SHALL be the implementation's own. A `limit` SHALL be applied after the filters and after ordering.

#### Scenario: More terms first
- **WHEN** the query is `session timeout`, one turn contains both words and another contains only "timeout"
- **THEN** the turn with both comes first

#### Scenario: A tie
- **WHEN** two turns each match one term
- **THEN** the turn with the greater `id` comes first

#### Scenario: A limit
- **WHEN** two implementations with no semantic stage answer one query over one workspace with `limit: 5`
- **THEN** they return the same five episodes in the same order

#### Scenario: A repeated term
- **WHEN** the query is `timeout Timeout timeout?`
- **THEN** it has one distinct term for ordering

### Requirement: Filters run afterwards, against the files and the index
An implementation SHALL apply every filter after the stages, reading the index and the episode files and not any cache. It SHALL support filtering by `occurred`, `container`, `standpoint` and `kind`, and MAY support others. It SHALL NOT return an inline episode whose `content.text` is redacted. A match on a field SHALL count only while the episode's file carries that field.

#### Scenario: A redacted label
- **WHEN** a stage proposes an episode on the strength of its `label`, and the episode's file lists `label` in `redacted.fields`
- **THEN** the episode is not returned on that account

#### Scenario: A label redacted, text kept
- **WHEN** an episode's `label` is redacted and its `content.text` matches the query
- **THEN** the episode is returned, with `resolution: lexical`

#### Scenario: A withdrawn turn
- **WHEN** a stage proposes a turn whose `content.text` is redacted
- **THEN** the turn is not returned

#### Scenario: A standpoint filter
- **WHEN** a query is filtered to one `standpoint`, and a matching turn has another
- **THEN** the turn is not returned

### Requirement: Recall by participant reads the files
An implementation MAY filter by participant. The filter SHALL match an episode whose `participants`, in its file, holds the reference given, compared as written. It SHALL be usable with or without a query. The specification SHALL state that `participants` is not in the index, so the filter is linear in history, and that a participants cache is the remedy.

#### Scenario: Mail sent to someone
- **WHEN** recall is filtered to the participant `mailto:alex@example.org`, and an email episode's `participants` holds that reference
- **THEN** the episode is returned

#### Scenario: Redacted participants
- **WHEN** an episode's `participants` is listed in `redacted.fields`
- **THEN** the participant filter does not match it

#### Scenario: A different spelling
- **WHEN** the filter is `mailto:Alex@example.org` and the file holds `mailto:alex@example.org`
- **THEN** the filter does not match, because references are compared as written
