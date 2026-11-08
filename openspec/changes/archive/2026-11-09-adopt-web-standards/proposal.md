## Why

Two parts of the format are home-made where open standards already do the job,
and the home-made versions have gaps.

- **`occurred` cannot name an instant in the repeated hour.** `occurred` writes
  a local date-time with no offset plus a separate `tz`. When daylight saving
  ends, a local time happens twice. In Melbourne on 2026-04-05, 02:30 is both
  +11:00 and +10:00, and the episode cannot say which. An email's `Date` header
  gives an offset but no zone, and the format makes the writer guess one.
  [RFC 9557](https://www.rfc-editor.org/rfc/rfc9557) (Internet Extended
  Date/Time Format) writes an offset and a bracketed IANA zone in one value,
  and is what JavaScript's Temporal uses.
- **One episode cannot say how it relates to another.** A self-attested act
  overloads `content.ref` with an episode id, so a validator has to recognise
  it by shape. A transcript cannot say which recording it was made from, and a
  better transcript cannot name the one it improves on (an open question).
  [RFC 8288](https://www.rfc-editor.org/rfc/rfc8288) (Web Linking) already
  defines typed links and an IANA registry of relation types, with absolute
  URIs as the extension mechanism.

## What Changes

- **BREAKING** `occurred.start` and `occurred.end` become RFC 9557 values:
  - a date-time is an RFC 3339 date-time with an offset, followed by a
    bracketed IANA zone when the zone is known, such as
    `"2026-04-05T02:30:00+10:00[Australia/Melbourne]"`;
  - an offset with no zone is valid when the source gives only an offset, such
    as a mail `Date` header;
  - a date alone stays valid.
- **BREAKING** `occurred.tz` is removed for date-times. The zone is the
  bracketed suffix. `tz` remains, optionally, only beside a date alone.
- The offset fixes the instant. A validator warns when the offset disagrees
  with the zone's rules at that local time. Writers do not write RFC 9557's
  critical flag (`!`) or any suffix other than the zone.
- `occurred` values are written as double-quoted YAML strings, because `[` and
  `]` are flow indicators in YAML and the index writes `occurred` in flow
  style.
- The rule that nothing is recorded before it happens compares the instant the
  offset gives with `timestamp`. A date alone is compared as a date, in `tz`
  where present.
- New optional field `links`: a sorted list of `{rel, href}` following RFC 8288.
  - `rel` is a relation type registered with IANA, used in its registered
    meaning, or an absolute URI.
  - `href` is an episode id in the same workspace, or a URI.
  - Links are written when the episode is recorded and never changed. They are
    not mirrored in the index, and `links` joins the closed set of redactable
    fields.
  - Readers do not reject an unknown `rel`. A link whose episode id does not
    resolve is reported as unresolved, not invalid.
- The spec names the meaning of two registered relations between episodes:
  - `via`: the episode records something taken from the target, such as a
    transcript from a recording, or a self-attested act from its attesting turn;
  - `predecessor-version`: the episode supersedes the target as a rendering of
    the same thing, such as a better transcript.
- A link MUST NOT restate `container`. Containment stays `container` and
  `ordinal`, because the index and recall by conversation depend on them.
- **BREAKING** `content.ref` MUST NOT be an episode id. A self-attested act
  always carries `content: {mode: none}`, and its attestation, when an episode
  holds one, is a `via` link. Shape recognition becomes: a non-container with
  `content.mode: none` is a self-attested act.
- Status open questions are updated:
  - derived renderings are answered in part by `via` and
    `predecessor-version`;
  - duplicate recordings note that links are where a later version could mark
    a repeat;
  - an open question is added on uncertain and approximate dates (EDTF,
    ISO 8601-2).
- References list RFC 9557, RFC 8288 and the IANA link relations registry.

## Capabilities

### New Capabilities

- `occurred-time`: the grammar of `occurred.start` and `occurred.end` as
  RFC 9557 values; offset-only and date-only forms; the zone suffix; quoting;
  and offset–zone consistency.
- `episode-links`: the `links` field following RFC 8288, covering relation
  types, targets, immutability, ordering, redaction, the meanings of `via` and
  `predecessor-version`, and the rule against restating `container`.

### Modified Capabilities

- `episode-evidence`: the rule that nothing is recorded before it happens
  compares the instant fixed by the offset, not a local time interpreted in
  `tz`; the scenario about the daylight-saving boundary is replaced by one
  about the repeated hour.
- `self-attested-acts`: an attestation episode is named by a `via` link, not by
  `content.ref`; a self-attested act always has `content.mode: none`; and shape
  recognition no longer looks at `content.ref`.

## Impact

- `README.md`, the spec:
  - `occurred`, `content`, Self-attested acts, the field table, the examples
    and `index.yaml`;
  - Redaction, which gains `links`;
  - a new `links` section;
  - Status and References.
- The YAML examples in the README change form: `occurred` values become quoted
  and no longer carry `tz`.
- There are no implementations yet, and the format is a draft, so there is no
  migration and no version bump.
- This change does not alter standalone conformance. `links` is defined
  entirely in this spec, and no relation it defines targets another format's
  object.
