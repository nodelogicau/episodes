## Why

Redaction is explicit, rare and irreversible, so a person who redacts
something should be able to rely on what the format says the result is. In
two places the draft promises more than its rules deliver:

- **Redacting `content.ref` does not remove where the content is** (#37). The
  draft says it "leaves a reference episode as a bare tombstone: it says that
  something of this kind happened at this time from this standpoint, and no
  longer where". But fields are redacted one by one, and others in the same
  file can still say where:
  - `content.uid` is defined as a way to find the content again when `ref`
    stops resolving, and a `mid:` names the sending domain;
  - `links` can hold the location as an `href`, and an archived snapshot's
    URL contains the original;
  - `content.version` is the source's own id for a version, and in the
    draft's own example it is the message id that `ref` carries.
- **Only embeddings are deleted** (#18). An implementation "that keeps
  embeddings deletes those of a redacted field, because an embedding can
  disclose what it was computed from". So can a topic score, a cached
  summary or a full-text index, and an implementation can keep all three and
  still conform.

Both matter more once recall by query is defined (#38), since it adds caches
derived from redactable fields.

Issues #18 and #37, and the review comments on #18 and #38.

## What Changes

- **BREAKING: redacting `content.ref` redacts everything that locates or
  identifies the content.** A `redacted` block that lists `content.ref` also
  lists `content.uid`, `content.version`, `content.hash` and `links`, for
  each of those the episode carries. A writer adds them in the same act, and
  a validator rejects a file whose block lists `content.ref` while any of the
  four is still present. This is not a side effect: it is one redaction, and
  every field it removes is named in `fields`.
- **What the tombstone keeps is stated.** After `content.ref` is redacted, a
  reference episode keeps its id, `kind`, `occurred`, `standpoint`,
  `container` and `ordinal`, its `media_type`, and whichever of `label`,
  `participants`, `place` and `content.language` were not redacted as well.
- **Each of the four can still be redacted alone.** Redacting `content.uid`
  or `links` without `content.ref` is unchanged.
- **The rule for embeddings covers every derived value.** An implementation
  that keeps values derived from an episode's fields (embeddings, classifier
  or other model outputs, summaries, search indexes) deletes or recomputes
  those derived from a redacted field.
- **"Derived" is defined:** a value is derived from a field if computing it
  again without that field could change it.
- **A derived value is not used once its field is redacted,** whether or not
  it has been deleted yet. A redaction made on one machine reaches another
  through git before that machine's caches are updated, so the check is made
  against the episode file.
- **An informative note** says that a judgement already written as an object
  of another format, such as a DKF claim citing the episode, is not a derived
  value under this rule. It is governed by that format's redaction, which is
  why redaction does not cascade.

## Capabilities

### New Capabilities

- `redaction-completeness`: what a redaction is guaranteed to remove,
  covering:
  - redacting `content.ref` also redacts `content.uid`, `content.version`,
    `content.hash` and `links`;
  - what a reference episode keeps afterwards;
  - derived values of a redacted field are deleted or recomputed, and are
    not used in the meantime;
  - what counts as derived, and what does not.

### Modified Capabilities

None. The redaction requirement in `standalone-conformance` lists the rules
the document must state, and the rule that redaction is never implicit and
the statement of what it does not remove are both kept. The requirements
that make `content.uid` and `links` redactable are unchanged.

## Impact

- `README.md`, in *Redaction*:
  - the paragraph on the closed set, with the `content.ref` rule;
  - *Redacting `content.text` withdraws an inline episode*, where the
    tombstone is described;
  - *It is irreversible and never implicit*, with a sentence that the
    `content.ref` rule is not a side effect;
  - *What redaction does not remove*, with the derived-value rule and the
    informative note.
- **Existing files.** An episode whose block lists `content.ref` and which
  still carries one of the four becomes invalid. It is repaired by redacting
  again: further redaction merges into the block, so adding the missing
  fields is allowed.
- **Cost.** Redacting `content.ref` loses links that disclosed nothing, such
  as `predecessor-version` to another episode.
- episodes-cli follows, to be raised as an issue there: `redact` adds the
  four fields when `content.ref` is named, and `validate` rejects a block
  that lists `content.ref` while one remains.
- DKF's redaction text has the same sentence about embeddings. The review
  comment on #18 suggests the same generalisation there, in the same words.
  That is for the DKF repository and is not part of this change.
- Closes #18 and #37.
