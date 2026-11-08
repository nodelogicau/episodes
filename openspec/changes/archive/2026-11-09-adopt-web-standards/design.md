## Context

`occurred` is a home-made combination of a local date-time with no offset and a
separate IANA `tz`. The spec chose a zone over an offset deliberately, because
"tomorrow at 2" has to be resolved against a place. That choice dropped the
offset, which is the only thing that tells the two instances of a repeated
local hour apart. It also forces a zone where a source gives only an offset.

There are three cases where one episode needs to point at another, and the
spec handles each a different way or not at all:

- a self-attested act points at its attesting turn through `content.ref`;
- a transcript cannot point at its recording;
- a better transcript cannot point at the one it improves on.

`container` is a fourth relation and works well.

The format is a draft with no implementations, so breaking changes cost
nothing now.

## Goals / Non-Goals

**Goals:**

- Make every `occurred` instant unambiguous, including in the repeated hour.
- Use a published grammar for `occurred` that is already implemented in common
  libraries, not a home-made one.
- Give episodes one general, standard way to name relations to other episodes
  and to external resources.
- Simplify the self-attested act rules by taking relations out of `content`.
- Stay standalone, so that every rule is restated in the README.

**Non-Goals:**

- Uncertain or approximate dates (EDTF). They are recorded as an open question.
- A relation for duplicate recordings. Two writers that each record the same
  email do not know about each other, so neither can write the link, and
  episodes are never revised to add one later. This stays an open question.
- Replacing `container`/`ordinal` with links.
- `ni:` URIs (RFC 6920) for `hash`. The hash keeps its `sha256:` form.
- Portable references (`mid:`, iCalendar `UID`) and Memento. They are
  candidates for a separate change.

## Decisions

### RFC 9557, with the offset required and the zone optional

A date-time in `occurred` is `date-time` from RFC 3339 (so it carries an
offset), followed optionally by a time-zone suffix `[<IANA name>]`.

- **Why the offset is required.** It is what fixes the instant and resolves the
  repeated hour. Every source that gives a time gives an offset or UTC. A
  writer that knows only a local time and a zone can compute the offset, except
  in the repeated hour, and that is exactly the case that cannot be guessed.
- **Why the zone is optional.** An email `Date` header gives `+1100` and no
  zone. A required zone made writers guess one, and a guess presented as a
  fact is the failure the format exists to avoid. The zone SHOULD be written
  whenever it is known.
- **Alternatives considered.**
  - Keep `tz` and add an `offset` field. This is the same information as
    RFC 9557 in a home-made shape.
  - RFC 3339 alone with no zone. This loses the zone, and "tomorrow at 2" needs
    it.

### No critical flag and no other suffixes

RFC 9557 lets a suffix carry `!` to make it critical, and allows elective tags
such as `u-ca=`.

- Writers MUST NOT write `!` or any suffix other than the zone. Readers MUST
  accept and ignore elective tags.
- When the offset and zone disagree, the offset wins and a validator warns.
  This follows RFC 9557's treatment of an inconsistency without `!`.
- A reader that meets `!` with an inconsistency has a file it cannot honour, so
  it reports the episode as invalid.

### Dates alone keep `tz`

RFC 9557 defines no suffix on a full date, so a date alone stays `YYYY-MM-DD`.

- `tz` is allowed only beside a date alone, so that comparisons are made in the
  right place.
- `start` and `end` take the same form: both dates, or both date-times.
- Without `tz`, a validator compares a date alone with the recording instant's
  UTC date and allows one day of slack, so it warns only on a date more than a
  day ahead.

### Quoted strings

The index writes `occurred` in flow style (`{start: …}`), where `[`, `]` and `,`
are flow indicators. A YAML 1.1 parser also coerces an unquoted date-time into
a timestamp type and loses the zone. So writers MUST double-quote `start` and
`end` everywhere. The examples change accordingly.

### `links` follows RFC 8288

`links` is a list of `{rel, href}` mappings, sorted by `rel` and then by `href`
for byte-identical output.

- `rel` is a lowercase relation type from the IANA Link Relations registry, or
  an absolute URI, as RFC 8288 §2.1 allows.
- `href` is an episode id, resolved within the workspace, or a URI.
- Other target attributes (`title`, `type`, `hreflang`) are left out until a
  use for them appears.
- **Why RFC 8288 and not home-made fields.** Its registry already names most
  useful relations, and the URI extension rule gives namespacing without the
  format having to run one. Readers ignore relations they do not know, which
  keeps the format open.
- **Alternatives considered.**
  - Dedicated fields such as `derived_from` and `attestation`. Each one is
    another field and another redaction rule.
  - JSON-LD and PROV-O. These are much heavier, and this format has no RDF
    elsewhere.

### Links are immutable, unindexed and redactable

- **Immutable.** Links are written at recording, under the accumulation-only
  principle. A link can only point to an episode that already exists or to an
  outside resource, so nothing ever needs adding later.
- **Unindexed.** Links are left out of the index so that a sealed segment never
  has to change.
- **Redactable.** Because links are not indexed, `links` can join the closed
  redactable set. An outside URI can disclose as much as a `content.ref`.
  Redaction removes the whole list, because paths into a list have no stable
  addressing.

### Two relations given episode meanings

The spec names two registered relations as used between episodes:

- **`via`** (RFC 4287): "the source of the information in the link's context".
  A transcript is `via` its recording, and a self-attested act is `via` its
  attesting turn.
- **`predecessor-version`** (RFC 5829): the target is an earlier version. A
  better transcript names the transcript it supersedes. The older episode is
  not changed.

Other registered relations may be used with their registered meanings, and the
spec gives them no further rules.

- **Alternatives considered.** `duplicate` (RFC 6249) means "byte-identical
  representations", which a repeated recording is not, so it is not adopted for
  duplicates.

### `container` stays, and links do not restate it

The index mirrors `container` and `ordinal`, and recall by conversation depends
on them. A link with `rel: up` or `rel: collection` that points at the
container would be a second, unindexed copy of the same fact, which could drift
from the first. Such a link is forbidden, and a validator warns on one.

### Self-attested acts use `via`

`content.ref` names something outside the workspace that is fetched, so an
episode id there now fails validation. A self-attested act is always
`content: {mode: none}`. Its attestation, when an episode holds one, is a `via`
link, and a validator checks that the target's standpoint matches the act's.

Shape recognition becomes a single test: an episode with `content.mode: none`
that no episode names as `container`. This removes the second test, which
looked for "any `content.ref` that is an episode id".

## Risks / Trade-offs

- **RFC 9557 is newer than RFC 3339, and library support is uneven.**
  - Mitigation: the format is RFC 3339 plus a simple, well-defined suffix, so
    a reader can split it off by hand.
  - Temporal, java.time and Python's `zoneinfo` all have what is needed.
- **A writer with only a local time and a zone may struggle to compute the
  offset in the repeated hour.**
  - Mitigation: this is the honest state of its knowledge. It records the
    offset it believes was in force, and `basis` records how the time is known.
- **Quoting is easy to forget.**
  - Mitigation: the rule is stated once, applied in every example, and a
    validator warns on an unquoted value in source text if it can see it.
- **`links` might attract interpretive relations**, such as one meaning
  "fulfils an intention", which would undo the "Record, never interpret"
  principle.
  - Mitigation: the spec says links record provenance and versioning known at
    recording. A relation that judges an episode belongs in a claim in another
    format. The informative text is restated to say so.

## Migration Plan

There is none. The format is a draft with no declared version and no
implementations. All README examples are rewritten in the new form.

## Open Questions

- Whether `anchor` (RFC 8288's context override) should be allowed, so that a
  link can be about the referenced content rather than the episode. It is
  deferred until a use appears.
