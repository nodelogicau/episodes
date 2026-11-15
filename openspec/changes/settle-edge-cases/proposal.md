## Why

Building the reference implementation, episodes-cli, found six cases where
the draft states a rule and leaves its edge undecided. Each is small. In each,
two implementations that follow the text can still behave differently, and
episodes-cli had to choose:

- **A source's clock runs ahead of the writer's** (#22). "Nothing is recorded
  before it happens" has no tolerance for writers, so mail whose `Date`
  header is thirty seconds ahead cannot be recorded until the clocks agree,
  and the writer cannot correct a time the source stated.
- **A writer has no defined way to learn the zone** for a time it observed
  itself (#27). The zone is "written whenever it is known, and never
  guessed", and the draft does not say what makes it known.
- **`redacted.fields` may or may not list a field the episode never had**
  (#29).
- **An index rebuild after a late merge meets a contradiction** (#30): the
  index must be reconstructible from the files, and a sealed segment never
  changes.
- **"Out of recall" does not say whether a withdrawn turn's position may be
  shown** (#31).
- **A sealed month with no files may or may not get a segment** (#33), so two
  indexes of the same files can differ.

Issues #22, #27, #29, #30, #31 and #33, and the review comment on #27.

## What Changes

- **A stated time may be up to five minutes ahead of the recording.** A
  writer MAY record an episode whose `basis` is `stated` and whose
  `occurred.start` or `end` is at most five minutes later than `timestamp`,
  recording the time as the source stated it. A validator warns only beyond
  the same five minutes. For `recorded` and `inferred` times the bound stays
  exact, because the writer supplies those from its own clock. The allowance
  for a date alone is unchanged.
- **Where a zone for a `recorded` time comes from.** It is the zone in which
  the recording was made, and a writer takes it from, in order:
  - the value it is given, when that carries a zone;
  - the device at which the person took part, as that device reports its
    zone at the time;
  - `defaults.zone` in `episodes.yaml`, a new optional key holding an IANA
    zone name.
  A writer that has none of these writes the offset alone.
- **A writer never writes a zone that contradicts the offset.** If the zone's
  offset at that instant differs from the offset being written, the writer
  leaves the zone out. This is what stops a configured zone being written
  for a turn typed while travelling. A writer that has only an instant, and
  no local offset to check against, does not apply `defaults.zone` at all.
- **A default zone is never applied to a `stated` or `inferred` time.** A
  source that gives only an offset is recorded with the offset alone, as now.
- **`redacted.fields` lists only what was removed.** A writer MUST refuse to
  redact a path the episode does not carry, unless the block already lists
  it.
- **A rebuild never rewrites a sealed segment.** When a sealed month's
  directory does not match its segment's `count`, a rebuild fails, naming the
  files, as validation does. The text says that "reconstructible" holds for a
  workspace with no late merge.
- **A sealed month with no files has no segment** and no entry in `segments`.
- **"Out of recall" means not returned as content.** A reader MAY show that a
  withdrawn turn existed at its position, using only fields that cannot be
  redacted, and MUST NOT show anything that was redacted.

## Capabilities

### New Capabilities

- `index-segments`: two rules for sealed segments:
  - a rebuild does not rewrite an existing segment, and fails on a count
    that does not match;
  - a sealed month with no files has no segment.
- `redaction-record`: what a `redacted` block and a withdrawn episode say:
  - `fields` lists only paths that were present when redacted;
  - a withdrawn episode is not returned as content, and its position may be
    shown from fields that cannot be redacted.

### Modified Capabilities

- `episode-evidence`: in *Nothing is recorded before it happens*, the
  five-minute allowance for a `stated` time, for writers and validators.
- `occurred-time`: a new requirement on where a writer learns the zone for a
  `recorded` time, including `defaults.zone` and the rule that a zone is not
  written when it contradicts the offset. The existing requirements are
  unchanged.

The sharding and index requirement in `standalone-conformance` lists what the
document must state. Its list still holds, so that requirement is unchanged.

## Impact

- `README.md`:
  - `occurred`: *The zone is written whenever it is known*, and *Nothing is
    recorded before it happens* with the paragraph on what a validator warns
    on;
  - *Redaction*: the paragraph on `fields`, and *Redacting `content.text`
    withdraws an inline episode*;
  - *Sharding*: *A late merge is detected by count*;
  - *`episodes.yaml`*: the example and a sentence on `defaults.zone`;
  - *`index.yaml`*: the paragraphs on segments and on reconstruction.
- One optional key is added to `episodes.yaml`. No episode field is added,
  and no valid episode becomes invalid.
- episodes-cli already does four of these: it refuses to redact an absent
  path, never rewrites a segment, writes no segment for an empty month, and
  shows a placeholder for a withdrawn turn. Two things follow, each to be
  raised as an issue there:
  - `record` allows a `stated` time up to five minutes ahead, where it
    refuses any;
  - it leaves the zone out when the zone contradicts the offset. It already
    reads `defaults.zone`.
- Closes #22, #27, #29, #30, #31 and #33.
