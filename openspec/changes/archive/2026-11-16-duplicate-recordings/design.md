## Context

*Status* asks, under *Duplicate recordings*: should `(container, ordinal)` be
unique, should writers avoid a second `(standpoint, uid)`, and how is a
duplicate marked once it exists.

Two facts about the format shape every answer:

- **Episodes are never revised.** A duplicate cannot be merged, renumbered or
  linked after it is written. A rule can only act at the write, or report
  afterwards.
- **A workspace is merged through git.** Two writers on two machines cannot
  see each other. Whatever a writer is told to avoid, a merge can still
  produce.

So each rule here has the same form: the writer avoids it where it can see,
the validator reports it where it happened anyway, and nothing is invalid.

```
                      writer (can see)      validator (after)
 repeated ordinal     MUST NOT              warns
 second uid           SHOULD NOT            MAY report   (unchanged)
 hash of other bytes  MUST NOT              cannot tell
```

episodes-cli already does the first two. For the third it hashes whatever
bytes the caller supplies.

## Goals / Non-Goals

**Goals:**

- A writer knows what to do on a repeated `ordinal` and a repeated `uid`.
- Readers show the children of a container in one order.
- Two writers that record one stored copy of some content write the same
  `hash`.
- Narrow the open question in *Status* to what is still open.

**Non-Goals:**

- Marking a duplicate that exists. No registered relation fits, and episodes
  are not revised to add a link. That stays open.
- A duplicate rule for content with no `uid`, such as files and web pages.
- Telling apart instances of a recurring event. iCalendar does it with
  `RECURRENCE-ID`, which `uid` does not carry.
- Changing the line-ending rule, including for binary content.
- Putting `uid` or `hash` in the index.

## Decisions

### A writer does not reuse an `ordinal`

MUST NOT, where the writer can see the other episode. A repeated `ordinal`
has no good reading: two turns cannot both be seventh. Refusing is always
possible, because finding the children of a container is an index lookup.

The validator warns and does not reject. Two branches that each append the
next turn will assign the same `ordinal`, and git merges them without
conflict, since each turn is its own file. Rejecting would make a clean merge
produce an invalid workspace that nothing can repair.

### How an `ordinal` is chosen

The draft says only "position within `container`, an integer from 1". Two
writers given one conversation should number it alike.

- **Where the source has positions, the writer uses them.** Page 5 of a scan
  is `ordinal: 5` even if pages 3 and 4 were not recorded. The position is a
  fact about the source.
- **Otherwise, one more than the highest.** Not the count of children plus
  one: after a gap or a dropped episode, the count could land on an `ordinal`
  in use.

Gaps are valid. They arise from the first rule, and from dropped episodes.

### Readers order by `ordinal`, then by id

The issue offered this as informative. It is a requirement, because the point
of the change is that implementations agree, and a repeated `ordinal` is the
case where they would not.

Id is the tie-break because ids are UUIDv7, so the earlier recording usually
comes first, and because it needs no file to be opened: `container`,
`ordinal` and `id` are all in the index. The comparison is by code point, as
for every sorted string.

Children with no `ordinal` come last, by id. `ordinal` is required only where
order is meaningful, so such children have no position to honour, but a
reader still has to put them somewhere.

### A second `uid` is a SHOULD NOT

A writer that can see the workspace SHOULD NOT record a second reference
episode with the same `standpoint`, `media_type` and `uid`.

MUST NOT was considered. Three things are against it:

- **`uid` is not in the index,** so that it stays redactable. Finding a match
  means reading episode files, which is linear in history unless the
  implementation keeps a cache. A MUST would make every write depend on one.
- **A redacted `uid` cannot be matched.** A writer would then record a second
  episode it was required not to.
- **Sharing a `uid` does not prove sameness.** Every instance of a recurring
  event shares its series' `UID`. The writer has to be able to proceed when
  told the content is distinct.

The exception is "told explicitly", not "judges". A writer does not decide
that two things with one `uid` differ. Its caller says so.

A writer that declines names the existing episode. The usual reason to record
a reference episode is that something wants to cite it, and the existing one
serves.

The validator's rule stays as it is: it MAY report and MUST NOT reject.

### `hash` covers the representation `media_type` names

"As fetched" depended on the fetch. The rule now names the bytes:

- `message/rfc822`: the complete raw message as the mailbox stores it.
- `text/calendar`: the iCalendar object holding the event, as the store
  returns it.
- Any other type: the bytes of that representation.
- No `media_type`: the bytes `ref` returns.

`media_type` already says which format's identifier `uid` is. It now also
says which bytes `hash` covers, so one field fixes both.

Requiring `media_type` with `hash` was considered and left as a SHOULD. A
file in storage has an obvious byte sequence whether or not its type is
known, and a hash of it is still useful.

### No `hash` without those bytes

MUST NOT, where the issue said SHOULD NOT. A hash's only use is to be
compared with a later fetch. A hash of a provider's JSON, written under
`message/rfc822`, will never equal a hash of the raw message, so every reader
that checks it will observe the source as `changed`. That is worse than no
hash: it is a false report, written into a file that is never revised.

The writer leaves `hash` out and records `version` where the source has one.
An ETag or a sequence number detects change without the bytes.

### A hash identifies a copy

"As the mailbox stores it" means two people's copies of one message hash
differently, because each mailbox adds headers on delivery. The text says so.
The format already says episodes from different standpoints are not
duplicates and that `uid` is the identity, so nothing depends on hashes
matching across mailboxes.

Hashing only the parts all copies share was considered. It would need a
canonical form of a message, which is a specification of its own, and the
hash could no longer be checked with a plain fetch.

### Three capabilities

`ordinals` and `content-hash` are new. The writer rule on `uid` is added to
`content-identity`, beside the validator rule it pairs with. `ordinals` is
kept apart from `containment`, which the change `acts-and-containers`
introduces and which is not yet in `openspec/specs/`.

## Risks / Trade-offs

- **A hash written before this change may cover other bytes,** and nothing in
  the file says so. → A reader will observe `changed`, as for any mismatch.
  The format is a draft and the only known writer is episodes-cli.
- **Fewer episodes will carry a `hash`.** Provider APIs often return JSON
  only. → `version` covers change detection, and a wrong hash is worse than
  none.
- **"One more than the highest" needs the writer to hold a lock** between
  reading and writing. → On one machine a write lock does it. Across machines
  nothing can, which is why a repeat is a warning.
- **A writer may skip a recording that was distinct,** on a reused
  `Message-ID`. → The existing episode is named, and the caller can say the
  content is distinct.
- **The line-ending rule still applies to binary content,** so a PDF's `hash`
  need not equal a plain SHA-256 of the file. → Unchanged by this change, and
  worth its own issue.

## Migration Plan

No file is rewritten. Two things follow in episodes-cli, each to be raised as
an issue there once this is merged: its help and README say which bytes a
caller supplies for `hash`, and `list` orders children by `ordinal` and then
by id if it does not already.

## Open Questions

None for this change. *Status* keeps, under *Duplicate recordings*: how an
existing duplicate is marked, and what a writer does about content with no
`uid`.
