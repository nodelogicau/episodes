## Context

Each of the six cases is a rule the draft states without saying what happens
at its edge. episodes-cli had to pick an answer to ship, and its design notes
record each pick as spec feedback.

The six fall on three kinds of implementation:

```
                              writer   validator   reader   index rebuild
 #22 a clock that runs ahead    x         x
 #27 where the zone comes from  x
 #29 fields the episode lacked  x
 #30 rebuild after late merge                                    x
 #33 empty sealed month                   x                      x
 #31 withdrawn turn's position                       x
```

Two facts about the format shape the answers:

- **Episodes are never revised.** A wrong zone or a wrong entry in `fields`
  stays for good, so the writer rules lean towards leaving a thing out.
- **A sealed segment never changes.** Any rule about the index has to work
  without rewriting one.

## Goals / Non-Goals

**Goals:**

- Two implementations given the same input write the same episode, the same
  `redacted` block and the same index.
- Each rule can be applied by the implementation it falls on, with what that
  implementation can see.
- No valid episode becomes invalid.

**Non-Goals:**

- Correcting a time a source stated. The time is recorded as stated, and
  `basis` tells the reader how far to trust it.
- A way to repair a late merge other than re-minting.
- Masking index entries, so that a withdrawn turn's position could be hidden.
  *Status* keeps that open.
- Whether `Z` followed by a zone suffix counts as a disagreement for a
  validator. The existing rule compares "the offset" and is left as it is.
- The zone of a `stated` or `inferred` time. Those come from the source or
  from evidence, as now.

## Decisions

### Five minutes, and only for `stated` times

The bound exists to stop a plan being recorded as a happening. A `Date`
header thirty seconds ahead is not a plan. It is two clocks that disagree,
and the draft already says a validator warns for that reason and does not
fail.

- **Five minutes, where the issue suggested two.** It is the allowance
  Kerberos uses for clock skew, so it is a number implementors have met. Mail
  servers and phones are commonly out by more than two minutes. Nothing
  planned is recorded five minutes early by accident.
- **Only `stated`.** A `recorded` or `inferred` time comes from the writer's
  own clock or reasoning, and the same clock supplies `timestamp`. There is
  no second clock to disagree with.
- **The time is written as stated.** Clamping it to `timestamp` was
  considered. It would write a time no source gave, under a basis that says a
  source gave it.
- **One number for writer and validator.** If they differed, a conformant
  writer could write an episode that a conformant validator warns on.
- **A date alone keeps its own allowance.** It already has a day where the
  zone is unknown. Five minutes on top would matter only at midnight, and
  would make the rule harder to state.

A writer MAY use the allowance and need not. A writer that waits for the
clocks to agree is still conformant.

### The zone of a `recorded` time is where the recording was made

"Known" needed a definition. The review of #27 pointed out that the zone
suffix on a turn says where the turn was typed, not where the person lives.
So the sources are ordered by how directly they say that:

1. **The value.** The caller gave a zone with the time.
2. **The device.** The machine the person is typing on reports its zone.
   This is the usual case for a harness on the person's own machine.
3. **`defaults.zone`.** For a harness that knows the local offset and cannot
   ask the device for a name, as when it reads a transcript.

The issue also proposed that the person's statement counts as known. That is
dropped. "I live in Melbourne" says nothing about where this turn was typed,
and a writer that acted on it would be guessing.

`defaults.zone` sits beside `defaults.source`, which is already "writers
only". It holds one IANA name. A reader ignores it, as it ignores every
default.

### A zone that contradicts the offset is left out

Without this, `defaults.zone` is the guess the draft forbids: it would be
written on every turn typed while travelling. The check is cheap, since a
writer that writes zone names already has the zone's rules.

- **It applies to every source,** including a zone in the value. The draft
  already says the offset governs where the two disagree. A writer that
  wrote both would write an episode its own validator warns on.
- **A critical flag still means refuse.** That rule comes from
  `tighten-canonical-form`: the source has said the zone must be honoured.
  This change covers the zone with no flag, and the two fit together:

  ```
                      agrees          disagrees       rules unknown
   zone, no flag      write zone      offset alone    offset alone
   zone, critical     write, no flag  refuse          refuse
  ```

- **A zone the writer has no rules for is left out.** It cannot be checked.
  The offset still fixes the instant, so nothing about when is lost.
- **An instant with no local offset gets no default zone.** A value in `Z`
  says when and not what the local time was. There is nothing to check
  `defaults.zone` against, so applying it would be the unchecked guess again.
  A zone from the device is different: the device is reporting where it is,
  so the writer converts to local time under that zone.

The check does not tell apart two zones that share an offset at that instant:
Brisbane and Melbourne in July. A default of Melbourne is then written for a
turn typed in Brisbane. This is accepted. Catching it needs the device, and a
writer that has the device does not reach the default.

### `fields` records what was removed

Two readings were possible: `fields` is what the person asked to redact, or
what was taken out. The second is chosen.

- **The block is evidence.** "Who removed what" is what the draft says it
  records. Listing `place` on an episode that never had one says something
  false, in a block that is never removed.
- **It keeps the validator's test sound.** A required field may be absent
  only because `fields` lists it. A path listed for a field that was never
  there weakens what a listing means.
- **Refuse, not skip.** A request to redact a field that is not there is
  most likely a mistake about which episode or which field. Refusing the
  whole request tells the person. Dropping the path silently would not.

The exception is a path the block already lists. Redacting again is defined
as a union, so asking twice has to be harmless.

This fits `redaction-completeness`, which says redacting `content.ref` also
lists "each of" the identifying fields "that the episode carries".

A validator cannot check the rule. Once a field is gone, a file that had it
and a file that never did look the same. It is a writer rule only.

### A rebuild fails on a late merge

The draft says both that the index can be rebuilt from the files and that a
segment never changes. After a late merge only one can hold.

The segment wins. Sealing is what lets a consumer cache a segment for good,
and the draft's remedy for a late merge is already to re-mint. A rebuild
that absorbed the late files would make the remedy optional and the cache
wrong, with nothing reported.

So a rebuild does what validation does: it compares the directory with
`count` and fails, naming the files. It names both directions, a file with no
entry and an entry with no file, since `count` can be wrong either way.

"Reconstructible" is then true of a workspace with no late merge, and the
text says so. A rebuild still writes the root, and any segment that is
missing altogether, since writing a missing segment rewrites nothing.

### No segment for an empty month

A segment with `count: 0` and no entries carries nothing. Writing one for
every empty month would also make the index depend on how many months passed
between two episodes.

The rule is for whatever writes the index. A validator is told only not to
expect a segment for such a month.

### A withdrawn turn keeps its place

The turn's `id`, `ordinal`, `standpoint` and `occurred` are in the index and
cannot be redacted, so the format already discloses that a turn was there.
Hiding the position in a reader would hide nothing, and would make the next
turn read as a reply to the wrong one.

- **MAY, not MUST.** A reader that lists search results has no use for a
  placeholder. A reader that shows a thread does.
- **Only the fields that cannot be redacted.** A placeholder built from them
  can never show something a later redaction removes. A `label` that was
  kept is left out for that reason, though the person did not redact it.
- **"Not returned as content"** is the part every reader must do. Recall is
  for what was said, and a withdrawn turn says nothing.

### Two new capabilities, two modified

`index-segments` and `redaction-record` are new. `redaction-record` is kept
apart from `redaction-completeness`, which is not yet in `openspec/specs/`
and covers what is removed, where this covers what the block and the
remaining episode say.

The tolerance modifies *Nothing is recorded before it happens* in
`episode-evidence`. The zone rules are two added requirements in
`occurred-time`. `tighten-canonical-form` modifies a different requirement
there, so the two changes can be archived in either order.

## Risks / Trade-offs

- **Five minutes lets a short plan through.** A harness could record "call
  in three minutes" as a stated happening. → It would also have to claim a
  source stated it. The rule against copying a time from a plan still holds.
- **A zone given by the source is dropped where it contradicts the offset.**
  → The offset already governs, so the instant is unchanged. What is lost is
  a zone name the format would have warned on.
- **A writer with old time zone data drops a zone it should keep,** when a
  zone's rules have changed since. → The episode is still correct, with less
  detail. Writing a zone the writer cannot check is the worse error.
- **`defaults.zone` is wrong for a traveller in a zone with the same
  offset.** → Accepted, as above.
- **Refusing an absent path makes bulk redaction stricter.** "Redact `place`
  from these forty episodes" fails on the ones without it. → The caller
  filters first. An implementation may offer that as a convenience, provided
  each block lists only what was removed.
- **A rebuild that fails leaves a workspace without a usable index** until
  the branch is re-minted. → That is the state validation already reports.
  Readers fall back to the files, which the draft requires them to be able
  to do.

## Migration Plan

No file is rewritten. An index that holds a segment for an empty month stays
readable, and its segment is left alone, since segments do not change.

Two things follow in episodes-cli, each to be raised as an issue there once
this is merged: `record` allows a `stated` time up to five minutes ahead, and
it leaves the zone out when the zone contradicts the offset or the value has
no local offset.

## Open Questions

None for this change. One thing was noticed and left: RFC 9557 reads `Z` as
"local offset unknown", so `Z[Australia/Melbourne]` is not inconsistent
there, and the draft's validator rule does not say how it treats that form.
