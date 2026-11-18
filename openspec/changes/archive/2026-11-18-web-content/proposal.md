## Why

A reference episode points at content the format does not control, and web
pages are the content most likely to change or vanish. `source_status`
records that a source went `changed` or `gone`, but by then nothing can be
recovered, and the format refuses to back-fill content.

The web has an established practice for this.
[Memento](https://www.rfc-editor.org/rfc/rfc7089) (RFC 7089) and the
[Robust Links](https://robustlinks.mementoweb.org/) convention record, beside
the live URL, when the link was made and the URL of an archived snapshot.
Issue #13 proposes that a reference episode may link to one with the
registered `memento` relation.

That link cannot be written correctly today. A link's context is always the
episode, and a snapshot is a snapshot of the page that `content.ref` points
at, not of the episode. RFC 8288 has a parameter for exactly this, `anchor`,
which the `adopt-web-standards` design deferred (#16).

Issues #13 and #16, and the review comments on both.

## What Changes

- **A link MAY carry `anchor`, in one form only.** `anchor` says the link is
  about the referenced content and not about the episode. Its value MUST
  equal the episode's `content.ref`, so it appears only on a reference
  episode, and a validator can check it. A link with no `anchor` is about the
  episode, as now. No other use of `anchor` is admitted.
- **`links` holds `rel`, `href` and optionally `anchor`.** Writers sort by
  `rel`, then `href`, and put a link with no `anchor` before one with it.
- **A third relation gets a meaning: `memento`.** On a reference episode, a
  `memento` link with `anchor` names an archived snapshot of the content as
  it was when the episode was recorded. A `memento` link with no `anchor` is
  invalid, since an episode has no snapshot.
- **A snapshot is linked only at recording.** Links are written once, so a
  snapshot made later is never added. The writer links a snapshot it made
  while recording, or one it has checked against the content it fetched.
- **Archiving is explicit, never automatic.** Submitting a page to an archive
  discloses it to the archive. A writer MUST NOT cause content to be archived
  unless the person asks for it.
- **A reader MAY fall back to the snapshot** when the source is `changed`,
  `unreachable` or `gone`. It says that what it shows is an archive's copy.
  The episode's `source_status` still describes the source, and a writer
  still MUST NOT back-fill content from the snapshot.
- **A snapshot is not proof.** An archive may replay a page with changes of
  its own, so a snapshot need not match `content.hash`. A reader MAY compare,
  and reports a mismatch as unverified, not as invalid.
- The text says why this keeps to "Point, don't copy": the workspace still
  holds a pointer and no content.
- References gain RFC 7089.

## Capabilities

### New Capabilities

- `archived-snapshots`: the `memento` relation on a reference episode,
  covering:
  - what it names, and that it requires `anchor`;
  - when a snapshot may be linked;
  - that archiving needs an explicit request;
  - how a reader uses a snapshot, and what it does not prove.

### Modified Capabilities

- `episode-links`: in *`links` follows RFC 8288*,
  - a link MAY carry `anchor`, whose value equals `content.ref`;
  - what `anchor` means, and that it is valid only on a reference episode;
  - where an anchored link sorts.

## Impact

- `README.md`:
  - *Links*: the paragraph defining a link, the list of relations with a
    meaning, and *Links are written once*;
  - *`source_status`*: a sentence on falling back to a snapshot, beside the
    rule against back-filling;
  - *Design Principles*, *Point, don't copy*, if a sentence is needed there;
  - References.
- The change is additive. No existing link changes meaning, and an episode
  with no `anchor` is unaffected.
- **Depends on two changes that are not yet merged:**
  - `redaction-completeness`. A snapshot URL contains the original URL, and
    `anchor` repeats `content.ref`. Both are safe only because redacting
    `content.ref` also redacts `links`.
  - `tighten-canonical-form`. It modifies the same requirement in
    `episode-links`, so this change's delta is written on top of it and is
    archived after it.
- episodes-cli follows, to be raised as an issue there: `record ref` accepts
  an anchored link, and `validate` checks `anchor` against `content.ref` and
  rejects a `memento` link without one.
- Closes #13 and #16.
