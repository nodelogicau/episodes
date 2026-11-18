## ADDED Requirements

### Requirement: A derived cache is kept outside the workspace
An implementation MAY keep derived caches to serve recall: a semantic cache of vectors, a full-text index, and a cache of participants. Each SHALL be stored outside the workspace directory tree, and SHALL NOT be committed, published or served. A validator and a source check SHALL NOT read one. A workspace SHALL be valid, and recall SHALL be correct, with no cache present.

#### Scenario: A clone with no cache
- **WHEN** a workspace is cloned to a machine that has never built a cache
- **THEN** every query returns what the baseline and filters give

#### Scenario: A cache inside the workspace
- **WHEN** an implementation writes vectors to a directory under the workspace root
- **THEN** it is non-conformant, whether or not the directory is ignored by version control

#### Scenario: Validation
- **WHEN** a validator runs on a machine whose cache is corrupt
- **THEN** its result is the same as on a machine with no cache

### Requirement: Each cache entry records its episode and field
Every entry in a derived cache SHALL record the id of the episode it was computed from and the field it was computed from. An entry computed from content the workspace does not hold SHALL record `content.ref` as its field.

#### Scenario: A vector of a label
- **WHEN** an implementation embeds an episode's `label`
- **THEN** the vector records the episode's id and the field `label`

#### Scenario: A participants entry
- **WHEN** a participants cache holds that an episode names a person
- **THEN** the entry records the episode's id and the field `participants`

### Requirement: A cache only proposes
A derived cache SHALL only propose episodes. Before an episode is returned on the strength of a cache entry, the implementation SHALL read the episode's file and confirm that the file carries the entry's field. For a participants cache it SHALL also confirm that `participants` still holds the reference asked for. A missing, partial or stale cache MAY lower recall or speed, and SHALL NOT cause an episode to be returned that the baseline and filters would not allow.

#### Scenario: A redaction not yet seen by the cache
- **WHEN** a redaction of an episode's `participants` arrives from another machine, and this machine's participants cache still holds its entry
- **THEN** the episode is not returned for a participant filter

#### Scenario: A stale vector
- **WHEN** a semantic cache holds a vector of a `label` that the episode's file now lists as redacted
- **THEN** the vector proposes the episode, the check against the file fails, and the episode is not returned on that account

#### Scenario: A partial cache
- **WHEN** a semantic cache covers half the workspace
- **THEN** the semantic stage proposes fewer episodes, and the baseline's results are unchanged

### Requirement: A full-text index stands in for the scan only where it agrees
An implementation MAY use a full-text index in place of scanning the files for the baseline. It SHALL do so only where the index returns the episodes the scan would. Where it cannot establish that the index is current, it SHALL scan.

#### Scenario: An episode added since the index was built
- **WHEN** an episode matching the query was merged after the full-text index was last updated
- **THEN** the episode is still in the result

#### Scenario: Tokenising differently
- **WHEN** a full-text index splits `auth/session` into two tokens, and the query is `auth/session`
- **THEN** the implementation still returns exactly what the baseline's substring match returns

### Requirement: A semantic cache records its model
A semantic cache SHALL record the identifier of the model that produced its vectors. An implementation SHALL NOT consult a vector produced by a model other than the one in use. A vector of a field the workspace holds SHALL NOT need recomputing under the same model, since that text changes only by redaction.

#### Scenario: A model is replaced
- **WHEN** an implementation changes its embedding model, and its cache records the old model's identifier
- **THEN** the semantic stage does not consult the old vectors

### Requirement: An episode may have more than one vector
A semantic cache MAY hold more than one vector for one episode. A vector covering part of `content.text` SHALL record the span it covers and a hash of that span. Spans SHALL be internal to the cache: they are not a way to cite part of an episode, and two implementations need not agree on them. A query SHALL still resolve to the episode.

#### Scenario: A pasted document
- **WHEN** a turn's `content.text` is longer than the model's input limit
- **THEN** the implementation may embed it as several spans, and a match on any of them proposes the turn

#### Scenario: Redaction
- **WHEN** the turn's `content.text` is redacted
- **THEN** every vector of every span is deleted, as for any value derived from the field

### Requirement: A vector of referenced content is tied to `content.hash`
An implementation MAY fetch the content a reference episode points at and embed it. The vector SHALL be kept only in the semantic cache, and the implementation SHALL NOT keep the fetched content. The vector SHALL record the `content.hash` it was computed against, and SHALL be consulted only while the episode's file carries that `content.hash`. An implementation SHALL NOT embed the content of a reference episode that carries no `content.hash`.

Where the content fetched does not match the episode's `content.hash`, the implementation SHALL NOT embed it, and SHALL record what it observed in `source_status` as any source check does. A vector of an episode whose `source_status` is `changed` or `gone` SHALL NOT be consulted, and SHALL be deleted no later than the cache's next update.

#### Scenario: Embedding a document
- **WHEN** an implementation fetches a document, and the bytes hash to the episode's `content.hash`
- **THEN** it may embed the text, and the vector records the episode's id, the field `content.ref` and that hash

#### Scenario: The source has changed
- **WHEN** the bytes fetched hash to a different value
- **THEN** the implementation embeds nothing, and the episode's `source_status` records `changed`

#### Scenario: The source is gone
- **WHEN** an episode's `source_status` becomes `gone`, and the cache holds a vector of its content
- **THEN** the vector is not consulted, and is deleted at the cache's next update

#### Scenario: No hash
- **WHEN** a reference episode carries `version` and no `hash`
- **THEN** only its `label` is embedded

#### Scenario: The ref is redacted
- **WHEN** an episode's `content.ref` is redacted, which removes `content.hash` with it
- **THEN** the vector of its content is deleted, and until it is, the check against the file fails
