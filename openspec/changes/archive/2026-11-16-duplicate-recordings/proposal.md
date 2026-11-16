## Why

*Status* lists *Duplicate recordings* as an open question: the same recording
made twice, by on-demand recording that runs again, by two machines recording
one email, or by a replayed turn taking an `ordinal` already used. It asks
three things: should `(container, ordinal)` be unique, should writers avoid a
second `(standpoint, uid)`, and how is a duplicate marked once it exists.

Episodes are never revised, so a duplicate cannot be repaired after it is
written. The only place to act is at the write. The reference implementation,
episodes-cli, had to choose what its writer does in each case, and raised an
issue for each:

- **Two children of one container can hold the same `ordinal`** (#19), and the
  draft does not say how a writer picks one.
- **A writer is told nothing about a second `(standpoint, media_type, uid)`**
  (#23). Only the validator has a rule, and it reports after the fact.
- **`hash` is "over the content as fetched", and that depends on the fetch**
  (#24). One email is raw RFC 822 bytes from one call and JSON from another.
  Two writers can each follow the rule and write different hashes, so a
  reader checking the source sees a change that never happened.

Issues #19, #23 and #24, and the review comments on each. This answers the
first two questions in *Status* and leaves the third open.

## What Changes

- **A writer does not reuse an `ordinal`.** A writer MUST NOT write an
  `ordinal` that another episode it can see already holds in the same
  `container`.
- **How an `ordinal` is chosen.** Where the source gives positions, as the
  pages of a document or the attachments of an email do, the writer uses
  them. Otherwise it writes one more than the highest `ordinal` in the
  container. Gaps are valid.
- **A repeated `ordinal` is a warning, not an error.** Two branches can each
  assign the same next `ordinal` and merge cleanly. A validator warns, naming
  both episodes, and neither is invalid.
- **Readers order children by `ordinal`, then by id.** This makes the order
  the same everywhere when an `ordinal` repeats.
- **A writer avoids a second recording of the same content.** A writer that
  can see the workspace SHOULD NOT record a reference episode whose
  `standpoint`, `media_type` and `uid` match an existing one, unless it is
  told that this is a distinct thing, as an instance of a recurring event is.
  It is a SHOULD because `uid` is not in the index, and two machines cannot
  see each other's writes. The validator's rule is unchanged: it MAY report
  such episodes and MUST NOT reject them.
- **`hash` covers the representation `media_type` names:**
  - `message/rfc822`: the complete raw message, headers and body, as the
    mailbox stores it;
  - `text/calendar`: the iCalendar object that holds the event;
  - any other type: the bytes of that representation;
  - with no `media_type`: the bytes `ref` returns. A writer SHOULD write
    `media_type` whenever it writes `hash`.
- **A writer without those bytes writes no `hash`.** A writer that holds only
  a provider's own rendering, such as an API's JSON for a message, MUST NOT
  write a hash of it under that media type. It leaves `hash` out and records
  `version` where the source has one. **BREAKING** for a writer that hashes
  whatever its fetch returned.
- **A hash identifies one stored copy, not the message.** Two recipients'
  copies of one email differ in their `Received` headers. The text says that
  hashes are not compared across standpoints, and that `uid` is the identity.
- ***Duplicate recordings* in *Status* is narrowed** to what remains: how an
  existing duplicate is marked, and content that has no `uid`.

## Capabilities

### New Capabilities

- `ordinals`: `ordinal` within a container, covering:
  - a writer does not reuse one, and how it chooses one;
  - a repeated `ordinal` is warned on, not invalid;
  - readers order children by `ordinal` and then by id.
- `content-hash`: what `content.hash` is taken over, covering:
  - the bytes for `message/rfc822`, `text/calendar` and other media types;
  - no `hash` when the writer does not hold those bytes;
  - a hash identifies one copy, and is not compared across standpoints.

### Modified Capabilities

- `content-identity`: a new requirement that a writer avoids a second
  reference episode with the same `standpoint`, `media_type` and `uid`. The
  existing requirement *Possible duplicates are reported, never rejected* is
  unchanged.

The hash requirement in `standalone-conformance` requires the hash to be
fully specified in the document and fixes the algorithm and line-ending rule.
Naming the bytes adds to what the document specifies and changes neither, so
that requirement is unchanged.

## Impact

- `README.md`:
  - the `ordinal` row of the `EPISODE` field table;
  - *Containment*, with the `ordinal` rules;
  - `content`, the paragraph on duplicates under `uid` and the paragraph
    defining `hash`;
  - *Status*, the *Duplicate recordings* entry.
- No field is added. An episode with a repeated `ordinal`, or a second
  recording of one `uid`, stays valid.
- A `hash` already written over other bytes cannot be told from a correct
  one. A reader that fetches the named bytes will observe such a source as
  `changed`. That is the existing behaviour for any hash mismatch.
- episodes-cli already refuses a repeated `ordinal`, warns on one in
  `validate`, and refuses a second `uid` without `--allow-duplicate`. Two
  things follow, each to be raised as an issue there:
  - its help and README say which bytes a caller must supply for `hash`;
  - `list` orders children by `ordinal` and then by id, if it does not
    already.
- Closes #19, #23 and #24.
