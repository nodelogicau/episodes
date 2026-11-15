## Context

A reference episode holds a pointer, and for a web page the pointer is the
least durable thing in the workspace. `source_status` records that the page
went `changed` or `gone`. Nothing recovers what it said: the format does not
copy content, and forbids back-filling it.

Memento (RFC 7089) and Robust Links address this on the web by recording
three things together:

```
 Robust Links                 an episode
 ───────────────────────────  ──────────────────────────────────────
 the original URL             content.ref
 when the link was made       occurred / timestamp
 the snapshot's URL           links: {rel: memento, href: …}   ← new
```

Two of the three are already in an episode. Issue #13 proposes the third as a
link with the registered relation `memento`.

The obstacle is what a link is about. In RFC 8288 a link runs from a context
to a target, and in this format the context is the episode. A `memento` link
on an episode would say the snapshot is a snapshot of the episode, which it
is not. RFC 8288's `anchor` parameter changes a link's context. The
`adopt-web-standards` design deferred it, and #16 asks whether it is needed.

Two other changes bear on this one:

- `redaction-completeness` makes redacting `content.ref` redact `links` as
  well.
- `tighten-canonical-form` rewrites the same `episode-links` requirement:
  the `rel` rule and the sort comparison.

## Goals / Non-Goals

**Goals:**

- A reference episode can point at an archived snapshot of its content, in
  words that mean what RFC 8288 and RFC 7089 say.
- A link can be about the referenced content, in one checkable form.
- Nothing is sent to an archive that the person did not ask to send.
- The format still copies nothing.

**Non-Goals:**

- A general `anchor`. Links about arbitrary resources have no use here.
- The Memento protocol itself: TimeGates, TimeMaps and datetime negotiation
  are for whatever fetches.
- Choosing or naming an archive.
- Snapshots of mail, calendar events or files. Nothing forbids one, but the
  practice and the relation are the web's.
- Adding a snapshot after the episode is recorded.
- Defining a meaning for any anchored relation other than `memento`.

## Decisions

### `anchor` equals `content.ref`

A link may carry `anchor`, and its value is the episode's `content.ref`,
exactly.

In RFC 8288, `anchor` is the URI of the link's context. The context wanted
here is the content the episode refers to, and the format already holds its
identifier in `ref`. So the anchor is not a new marker with a meaning to
define: it is the standard parameter with the value the standard calls for.
It also lines up with Robust Links, which keeps the original URL beside the
snapshot's.

A validator can check it by comparing two strings. It follows that `anchor`
appears only on an episode that has a `ref`.

Alternatives:

- **A fixed token, such as `"#content"`.** It does not repeat `ref`. But a
  fragment of a YAML file has no defined meaning, and written unquoted it is
  a YAML comment, so `anchor: #content` reads as null without any error.
- **A field in `content`,** such as `content.snapshot`, and no `anchor`. It
  is simpler for this one case. It leaves #16 unanswered for every other
  link about the content, and each such relation would need its own field.
- **A general `anchor`.** It would let an episode make statements about any
  resource, which is not what an episode is for.

Repeating `ref` costs a line. It does not add a disclosure, because
`redaction-completeness` removes `links` whenever `content.ref` is redacted.

`ref` is "a URI or an identifier meaningful to whatever can fetch it", so an
`anchor` may hold a value that is not a URI. That is a looser reading than
RFC 8288's, and it is accepted: the rule that matters is equality with
`ref`, and for web pages, where snapshots exist, `ref` is a URL.

### Any relation may be anchored, and one gets a meaning

`anchor` is allowed on any link, so `canonical` or `alternate` can be said of
the referenced page and not of the episode. The format gives a meaning to
one anchored relation, `memento`, as it does to `via` and
`predecessor-version` between episodes. A reader gives the others no
meaning, as for any relation it does not know.

### `memento` requires `anchor`

A `memento` link with no `anchor` is invalid. An episode is a file in a
workspace and has no archived snapshot, so the link could only be a mistake,
and a reader should not have to guess that the content was meant.

This does not conflict with the rule that a reader does not reject an
episode for a `rel` it does not know. `memento` is a relation the format now
defines.

### Linked only at recording

*Links are written once* already rules out adding a snapshot later. That
fits what the link is for: it says what the content was when the episode was
recorded, and a later snapshot may be of a later page.

The writer may link a snapshot it had made while recording, or an existing
one it has compared with what it fetched. The second matters because many
pages are already archived, and making a new capture of each is slow and
discloses more. The comparison is the writer's responsibility. An older
snapshot of a page that has since changed is not linked.

### Archiving is explicit

Submitting a page to an archive gives the archive the page, and for a public
archive it publishes it. A writer does that only when the person asks for
that content to be archived. Recording an episode is not such a request.

This is a rule for writers that no validator can check, like the rule that a
self-attested act is recorded only on explicit attestation.

Linking a snapshot that already exists submits nothing, so it needs no
request.

### A fallback for readers, not a copy

A reader that cannot get the content as recorded may fetch the snapshot. It
says that what it shows is an archive's copy.

`source_status` is unchanged by this, because it is an observation of the
source. A `gone` page with a snapshot is still `gone`.

The rule against back-filling stands, and the text repeats it here because a
snapshot is the obvious temptation. The workspace holds a second pointer and
no content, which is what "Point, don't copy" asks.

### A snapshot may not match the hash

Archives rewrite links and add banners when they replay a page, so a
snapshot's bytes often differ from what was hashed. A reader may compare. A
mismatch is reported as unverified. It is not a `changed` source, since the
snapshot is not the source, and it does not make the episode invalid.

### Sorting

Links sort by `rel`, then `href`, by code point. Two links can now share
both and differ only in whether they are anchored, so the one with no
`anchor` comes first. An `anchor` has one possible value in a given episode,
so no further rule is needed.

### The delta is written on top of `tighten-canonical-form`

OpenSpec replaces a modified requirement whole. This change and
`tighten-canonical-form` both modify *`links` follows RFC 8288*, so the
delta here contains that change's text and scenarios with the `anchor` rules
added. It must be archived after `tighten-canonical-form`. Archived first,
it would bring that change's `rel` rule in early, and the later archive
would then remove `anchor`.

## Risks / Trade-offs

- **A snapshot can be taken down or changed by the archive.** → It is a
  pointer like any other, and the reader reports what it finds.
- **An archive's copy may differ from what was recorded.** → A reader says it
  is an archive's copy, and reports a hash mismatch as unverified.
- **A snapshot URL discloses the original URL.** → `redaction-completeness`
  removes `links` with `content.ref`. This change should not be merged before
  it.
- **A writer may link the wrong existing snapshot.** → It is required to
  compare. Nothing checks that it did.
- **`anchor` repeats `ref`.** → One line, checkable, and removed together
  with `ref` on redaction.
- **Two changes modify one requirement.** → See the ordering above.

## Migration Plan

Nothing in a workspace changes: no existing episode carries `anchor`.
Order of merging: `tighten-canonical-form` and `redaction-completeness`,
then this change. episodes-cli follows, to be raised as an issue there:
`record ref` accepts an anchored link, and `validate` checks `anchor`
against `content.ref` and rejects a `memento` link without one.

## Open Questions

None.
