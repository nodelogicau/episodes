## Context

`content.ref` is "a URI or an identifier meaningful to whatever can fetch it".
In practice that is a connector's id for one copy in one account. It is the
right thing for fetching and the wrong thing for identity. The content's own
format usually carries an identity:

- mail has `Message-ID` (RFC 5322), with the URI form `mid:` (RFC 2392);
- iCalendar has `UID` (RFC 5545). JSCalendar's `uid` is the same value.

Common providers can look content up by these: Gmail through the
`rfc822msgid:` search and the Google Calendar API through `iCalUID`, and IMAP
and CalDAV both support searching by them.

Issue #11 proposed putting the portable identifier either in `ref` or in a
`rel: alternate` link.

## Goals / Non-Goals

**Goals:**

- Record the content's own identity beside its locator, so that a reference
  survives a source migration and aliases of one thing can be recognised.
- Use the standard forms where they exist, and invent no URI scheme.

**Non-Goals:**

- Resolving the duplicate-recordings question. This change makes duplicates
  detectable. What writers should do about them stays open.
- An identity for files or web pages. Neither has an identifier its format
  assigns. A file's identity is its hash, which `content.hash` already holds.
- Indexing `uid` for lookup on recording. That would make it unredactable,
  which is the trade-off the index already makes for `content.ref`.

## Decisions

### A separate `content.uid`, not a portable `ref`

- `ref` answers "how do I fetch it", and `uid` answers "what is it".
- Making `ref` portable would make every fetch a search, and would lose the
  provider's direct id, which is often the only one an API accepts.
- **Alternatives considered.**
  - `ref` SHOULD be portable. This makes fetching slower, and some
    connectors cannot search.
  - A `rel: alternate` link. Its context would be the episode, not the
    referenced content, which is the anchor question raised in #16. `alternate`
    also means "a substitute representation", not "the same thing's
    identifier".

### One field, with its form set by `media_type`

- `uid` is the identifier the content's format assigns. It is written as a URI
  where that format defines a URI form, and verbatim otherwise.
- A `Message-ID` therefore becomes `mid:<id>`, with the angle brackets
  removed and the value percent-encoded as RFC 2392 requires.
- An iCalendar `UID` is written exactly as it appears. It is often
  `xxx@google.com`, which is not a URI, and no standard scheme exists for it.
- Because a bare `abc@example.com` could be either kind of identifier,
  `media_type` is required when `uid` is present: `message/rfc822` or
  `text/calendar`.
- **Alternatives considered.**
  - Separate `message_id` and `ical_uid` fields. That needs a new field for
    each new format.
  - A home-made `ical-uid:` URI scheme. Inventing a scheme defeats the point of
    using standards.

### Recurring events

The arranging of a recurring series is recorded with the series `UID`. An
instance that was arranged on its own, as an override, is identified by `UID`
plus `RECURRENCE-ID`. The `UID` alone does not identify it.

- **Decision:** `uid` holds the `UID`, and a writer recording an override
  instance appends nothing to it. The instance's `ref` and `version` still
  locate it.
- This is recorded as a known limit. A `uid` shared by a series and its
  override is not proof that the two episodes are duplicates. This matters
  because duplicate reporting also compares `standpoint` and `media_type`, so
  a series and its override would still be reported as possible duplicates.
- **Alternatives considered.** A `recurrence_id` field. This is deferred until
  a use appears.

### Finding content again by `uid`

When `ref` is unreachable, a reader MAY search by `uid`.

- If it finds the content, the source is `available`, or `changed` if the hash
  or version differs. It is never `gone`.
- The episode's `ref` is not rewritten, because episodes are not revised. An
  implementation may keep its own cache from `uid` to the new locator, which
  is outside the format.
- `gone` therefore means that the content could not be found by `ref` or by
  `uid`.

### Duplicates are reported, never rejected

- A validator MAY report episodes sharing `standpoint`, `media_type` and `uid`
  as possible duplicates.
- `standpoint` is included because two people's records of one email are
  different episodes, and whether they are about the same email is a
  judgement for another format.
- Nothing is rejected, because both recordings are valid, and episodes are
  never revised to merge them.

### Redactable and unindexed

A `Message-ID` can disclose the sender's domain and host, so `uid` joins the
closed redactable set. It is not mirrored in the index.

## Risks / Trade-offs

- **`Message-ID` is not always unique.** Broken mailers reuse ids, and a
  message's sent copy and received copy share one.
  - Mitigation: the sent and received copies are the same email, so sharing is
    correct for them.
  - Reuse by a broken mailer is why the format reports possible duplicates and
    never asserts them.
- **Encoding errors in `mid:`.**
  - Mitigation: the spec states the transformation (strip the angle brackets,
    percent-encode as RFC 2392 requires) and gives an example.
- **A writer that cannot see the source's identifier** leaves `uid` out.
  - Mitigation: the field is optional, and an episode without it is no worse
    than an episode today.

## Migration Plan

There is none. The change is additive and the format is a draft.

## Open Questions

- Whether a `recurrence_id` is needed so that `uid` can identify an
  overridden instance of a recurring event, not only its series.
