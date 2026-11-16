## Context

*Redaction* removes fields from an episode and keeps the episode. It makes
two promises that its rules do not keep.

**The tombstone.** Redacting `content.ref` "leaves a reference episode as a
bare tombstone: it says that something of this kind happened at this time
from this standpoint, and no longer where". But the redactable fields are
listed one at a time, and a person who names `content.ref` has removed only
that:

```
 content:
   mode: ref
   ref: gmail:msg_18f2c3a9b4d5e6f7      ← redacted
   uid: mid:CAF3x9q@mail.example.com    ← still finds the message by search
   version: "18f2c3a9b4d5e6f7"          ← the id that ref carried
   hash: sha256:9f2a…                   ← confirms a guess at the content
 links:
   - rel: memento
     href: https://web.archive.org/…/https://example.com/private   ← the URL
```

(The `memento` link is the kind #13 proposes. Any link to the same resource
does the same.) A validator cannot find this for them, because whether an `href` or a
`version` discloses the location is a judgement (#37).

**Derived values.** An implementation "that keeps embeddings deletes those of
a redacted field, because an embedding can disclose what it was computed
from". The reason given applies to anything computed from the field, and the
rule names only one kind (#18).

Recall by query (#38) will add caches computed from redactable fields, and
its review found that a cache on a second machine is stale between a `git
pull` and its next update.

## Goals / Non-Goals

**Goals:**

- Redacting `content.ref` leaves nothing in the file that locates or
  identifies the content, by a rule a validator can check.
- An implementation that conforms cannot keep, or use, anything computed from
  a redacted field.
- Both rules are stated so that a later recall section can rely on them.

**Non-Goals:**

- Erasure from version control. *What redaction does not remove* stands.
- Redacting indexed fields. *Index masking* stays open in *Status*.
- Cascading to other episodes or other formats.
- Whether `fields` may list a field the episode never carried, which is #29.
- Judging whether `label`, `participants` or `place` disclose a location.
- Changing DKF's redaction text.

## Decisions

### Redacting `content.ref` takes four fields with it

A block that lists `content.ref` also lists `content.uid`,
`content.version`, `content.hash` and `links`, where the episode carries
them. The issue proposed `uid` and `links`. Each of the four, taken in turn:

- **`content.uid`** is defined as a way to find the content when `ref` fails.
  Leaving it defeats the redaction by the format's own rule.
- **`links`** may hold the location as an `href`, and an archived snapshot
  always does. Links are redacted whole, so the choice is all or none.
- **`content.version`** is whatever the source calls a version. It is often
  an opaque id, and in the draft's example it is the provider's message id.
- **`content.hash`** does not say where the content is. It does let anyone
  holding a candidate confirm that it is the content. With `ref` and `uid`
  gone it also has no remaining use, since nothing can be fetched to compare
  with it.

Two narrower rules were considered:

- **Only links whose `href` discloses the location.** Not checkable, and
  links cannot be redacted one at a time.
- **A warning.** The tombstone's definition would then be false whenever the
  warning was ignored, and redaction cannot be redone more carefully later in
  any way that removes what earlier readers saw.

The cost is a harmless link lost now and then, such as `predecessor-version`
to another episode. Redacting `content.ref` is explicit, rare and
irreversible, so erring toward removal is the right side.

### It is not a side effect

*Redaction* says nothing redacts as a side effect. That sentence is about
events that are not redactions: a source being deleted, a citing object being
withdrawn. Here a person redacts, and the redaction has a defined extent.
Every field removed is named in `fields`, so the file still says exactly what
was taken out. The text says this, so the two rules are not read as
conflicting.

### `label` and the rest stay the person's choice

`label`, `participants`, `place` and `content.language` are not included. A
subject line can say where a document is, but it usually does not, and the
episode is of little use without it. They stay redactable one by one. The
text lists what a tombstone keeps, so a person can see what else they might
name.

`media_type` stays because it is not redactable, and it is what "of this
kind" means beyond `kind`.

### Every derived value, with a test

The rule covers "values derived from an episode's fields", with embeddings,
model outputs, summaries and search indexes as examples and not as a closed
list. A new kind of cache is covered without a change to the text.

"Derived from a field" is defined by a test: computing the value again
without the field could change it. That settles the cases a list would not:

- A summary computed from `label` and `content.text` is derived from both.
  When one is redacted it is deleted, or computed again from the other.
- A count of an episode's children is derived from no redactable field, and
  is kept.

"Deletes or recomputes" replaces "deletes" for the first of these.

### Not used, as well as deleted

Deleting happens where the redaction is made. A workspace is shared through
git, so the redaction arrives on other machines as a changed file, and their
stores still hold the old values until something updates them. In that
interval a query can return an episode on the strength of a vector of its
redacted label, which tells the person asking what the label said.

So an implementation must not use a derived value of a field the file lists
as redacted, and it decides from the file. The check costs nothing extra
where it matters: recall reads the file before returning an episode.

This makes the stores' freshness a matter of speed and not of safety, which
is the property DKF's semantic cache has for whole objects. Here it has to
hold per field, because an episode with one field redacted is still an
episode that may be returned.

### Other formats' objects are outside the rule

A claim that cites an episode was computed from it in some sense. It is not a
cache: it is a record with its own author, its own review and its own
redaction. The informative note says so, and ties it to the existing rule
that redaction does not cascade.

### One new capability

`redaction-completeness` holds all of it. The requirement in
`standalone-conformance` lists the redaction rules the document must state.
Its list still holds: this change adds rules and removes none.

## Risks / Trade-offs

- **Existing redactions of `content.ref` may become invalid.** → Redacting
  the leftover fields repairs the file, since a second redaction merges into
  the block. The format is a draft.
- **A harmless link is lost with `content.ref`.** → Accepted. See above.
- **A `label` can still disclose a location.** → The text lists what a
  tombstone keeps. An implementation may prompt for the rest.
- **"Could change it" has edge cases,** such as a model that happens to
  ignore a field. → The test is whether the field was an input, and when in
  doubt the value is deleted.
- **The no-use rule needs a file read before a derived value is trusted.** →
  Recall already reads the file. A background job that only ranks must check
  too.
- **DKF's text will differ from this one** until it is changed there. → Noted
  in the proposal for the DKF repository.

## Migration Plan

No file is rewritten by this change. episodes-cli follows, to be raised as an
issue there once this is merged: `redact` adds the four fields when
`content.ref` is named, and `validate` rejects a block that lists
`content.ref` while one remains.

## Open Questions

None for this change. Whether `fields` may list a field the episode never
carried is #29.
