## Why

A reference episode's `content.ref` is usually a provider id, such as
`gmail:msg_…` or `gcal:evt_…`. That id names a copy in one account, not the
thing itself.

- When a mailbox moves, the ref stops resolving and the episode reads as
  `unreachable` or `gone`, even though the email still exists.
- Two recordings of one email made through different connectors carry
  different refs, so nothing in the episodes shows they are the same thing.
  The *Duplicate recordings* open question calls these aliasing refs "harder
  still".

Mail and calendars already give their content identifiers that do not depend
on the provider:

- the `Message-ID` header, which has a standard URI form, `mid:`
  ([RFC 2392](https://www.rfc-editor.org/rfc/rfc2392));
- the iCalendar `UID` ([RFC 5545](https://www.rfc-editor.org/rfc/rfc5545)).

Issue #11.

## What Changes

- New optional field `content.uid` on a reference episode. It holds the
  identifier the content's own format assigns, as the source gave it.
  - It is written as a URI where the format defines a URI form: a `Message-ID`
    becomes a `mid:` URI.
  - It is written verbatim otherwise, as with an iCalendar `UID`.
  - When `uid` is present, `content.media_type` is required, because it says
    which format's identifier `uid` is.
- `ref` keeps its meaning: whatever can fetch the content. `uid` is not a
  locator, and `ref` is not an identity. A writer records `uid` whenever the
  source exposes one.
- A reader whose `ref` no longer resolves MAY find the content again by `uid`.
  A source found that way is not `gone`.
- A validator MAY report episodes that share `standpoint`, `media_type` and
  `uid` as possible duplicates. It never rejects them, because two recordings
  of one email are both valid.
- `content.uid` joins the closed set of redactable fields. It is not mirrored
  in the index, which keeps it redactable.
- `uid` is only on reference episodes. An inline episode MUST NOT carry it,
  because its identity is its episode id.
- The *Duplicate recordings* open question is updated: `uid` makes aliases
  detectable, and what a writer does about a duplicate stays open.
- References list RFC 2392, and RFC 5322 for `Message-ID`.

## Capabilities

### New Capabilities

- `content-identity`: `content.uid` covering:
  - its forms (a `mid:` URI for mail, a verbatim iCalendar `UID`);
  - the `media_type` requirement;
  - its separation from `ref`;
  - finding content again by `uid` and its effect on `source_status`;
  - duplicate reporting;
  - redaction;
  - its exclusion from the index and from inline episodes.

### Modified Capabilities

None. The redaction requirement in `standalone-conformance` requires the
closed set to be stated, not its members, so adding a member changes no
requirement.

## Impact

- `README.md`:
  - the `content` section, with the reference example and a new paragraph on
    `uid`;
  - `source_status`;
  - Redaction;
  - the `index.yaml` exclusion sentence;
  - Status and References.
- The change is additive. No existing field changes meaning.
- Closes #11.
