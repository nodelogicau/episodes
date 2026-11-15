## Context

Two kinds of episode have no content of their own. A **container** groups its
children: a conversation and its turns. A **self-attested act** records
something a person did that left no record. Both carry
`content: {mode: none}`, and the draft tells them apart by shape: an episode
with `mode: none` that nothing names as its `container` is an act.

```
                 children          no children
 mode: none      container         act            ← the draft
 mode: none      container         container      ← this change
 mode: attested  act               act
```

The shape rule was chosen so that `kind` could stay descriptive. Building
episodes-cli showed what it costs:

- A container is written before its first child, so there is always a moment
  when it has none, and a crash or a partial copy makes that permanent. The
  container then fails the act rules (#21).
- A container's `standpoint` decides whether it passes those rules, so the
  field cannot be given a meaning of its own (#34).
- The rule that an act names its attestation has nothing to key on but the
  writer's good behaviour (#25), and the fix proposed there would catch
  connectors (#17).

Separately, `container` has no rule for a target that is missing (#20), and
the opening line says the format is written by AI harnesses (#17).
episodes-cli has already split attestation into `--via` and `--control`
(episodes-cli#4).

## Goals / Non-Goals

**Goals:**

- An act is an act because it says so, and a container is never mistaken for
  one.
- A container's `standpoint` has one stated meaning.
- The attestation rule holds for harnesses and connectors alike.
- `container` degrades as `links` does when a workspace is incomplete.
- The text says who writes episodes without implying a model is needed.

**Non-Goals:**

- Making `kind` decide validity. It stays descriptive.
- Whether a harness may attest its own acts. That stays open in *Status*.
- A validator check that an act was explicitly attested. No file can show it.
- Converting acts written under the current draft.
- Cycles in `container`, or a limit on depth.
- Uniqueness of `(container, ordinal)`, which is #19.

## Decisions

### A mode, not a flag

An act's content is `{mode: attested}`. The issue suggested
`{mode: none, attested: true}`.

`content` answers where the record of the happening lives. `inline` says it
is here, `ref` says it is elsewhere, and `none` says the episode has no
record of its own because its children do. An act has a record: the person's
word. That is a fourth answer to the same question, so it belongs in the same
field.

A flag would leave more to define: what `attested: false` means, whether it
may appear with `inline` or `ref`, and where it sits in field order. A mode
has none of these. It also makes the validator's test one comparison.

The value is `attested` because the section is already called *Self-attested
acts*, and the rules are about who attests.

### `mode: none` is a container, with or without children

An episode with `mode: none` is a container whatever names it. One with no
children is valid, and a validator warns.

This gives up a check. Today a `mode: none` episode that records someone
else's act is invalid, because it has the act shape and fails "standpoint
equals `source.author`". After this change it is a childless container with a
warning. The check was never strong: adding one child turned any such episode
into a container. The warning keeps it visible, and the remedy for a real
container is to append a child, which changes no existing file.

The alternative from the issue was to exempt a set of container kinds
(`conversation`, `thread`). That would make `kind` decide validity, which the
format has avoided everywhere else.

### An act may have children

The mode alone makes an act, so the test no longer mentions children. Notes
written during a logged meeting can name the act as their `container`.

Forbidding it would need a rule and a validator check for no benefit: the act
rules still apply to the act, and each child is an ordinary episode with its
own standpoint and content.

### A container with nothing of its own is its keeper's

The `standpoint` of a `mode: none` container is the one whose record it is:
the person for a conversation with a harness, the mailbox owner for a thread.

The alternatives were whoever spoke first, and the harness. The first makes
the value depend on an accident of order. The second makes "my episodes" miss
every conversation. "Whose record" is also what *standpoint* already says of
a calendar event: "the record, kept by the person whose calendar holds it".

The rule applies only to containers with nothing of their own. An email that
contains its attachments has content, and its standpoint is its sender, as
for any email.

The text also says what the value does not mean. A reader filtering by
standpoint will find containers, and must not read one as saying its keeper
spoke every turn.

### The attestation rule depends on where the attestation was made

The rule is: when an act is attested in an episode the writer records, the
writer records that episode and links `via` it. Everything said in a
conversation the writer is recording falls under it. An act from a dedicated
control has no such episode and no `via`.

The issue proposed "when `source.harness` is present, `via` is required".
That is checkable, but wrong once connectors set `source.harness`: a "log my
run" button is a dedicated control whoever implements it.

The new rule also closes a gap in the existing one, which required `via` only
"when the attestation is an episode in the workspace". A writer could satisfy
that by not recording the turn. Now it must record it.

No validator can check this in general, as with the rule that an act is
recorded only on explicit attestation. A narrower check was considered: an
act whose harness also recorded a turn from the same standpoint near the same
time must link `via` one. It would report false findings whenever a person
talks to a harness and presses a control in the same minute, so it is left
out.

### `container` is reported like a link

A `container` that does not resolve is reported and is not invalid, in the
words *Links* already uses. Workspaces are copied in part and episodes are
dropped, and a turn is still a turn without its conversation.

A writer records a container first. A validator can see that only through id
order, and only UUIDv7 ids carry an order, so the check applies when both ids
are UUIDv7. Ids under `legacy/` are skipped. It is a warning: clock skew
between two machines can produce it honestly.

### Connectors are writers

The opening line becomes "written by harnesses and connectors". A connector
is described informatively as a writer that parses a source with no model.

`source.harness` names the software that recorded the episode, of either
sort. A new field for connectors was considered and rejected: readers would
have to look in two places for the same fact, and the difference between the
two is already carried by `model`, which is present only when a model took
part.

The informative note on recording, selection and consolidation goes in *When
an episode is recorded*. It is there to stop a reader concluding that every
message must pass through a model to become an episode. It requires nothing.

### Two new capabilities

`containment` holds the container rules, which had no capability. The
existing scenario *A container* under `self-attested-acts` moves there in
substance. `recording-source` holds the rules about who writes.

## Risks / Trade-offs

- **Acts written under the current draft stop being acts.** → The format is a
  draft, and the only known writer is episodes-cli. The text says how such a
  file now reads. A validator's warning on a childless container will name
  them.
- **A validator no longer rejects a contentless episode about someone else's
  act.** → It warns. See *`mode: none` is a container* above.
- **A fourth mode touches every reader.** → A reader that does not know
  `attested` should fail clearly. The mode has no fields of its own, so
  supporting it is small.
- **The warning on a childless container appears in a partial copy** where
  the children were left behind. → It is a warning, and it is true of that
  copy.
- **The attestation rule cannot be checked.** → Neither can the rule it sits
  beside. episodes-cli makes it hard to break by requiring `--via` or
  `--control`.

## Migration Plan

No file is rewritten. episodes-cli changes in two places, each to be raised
as an issue there once this is merged: `act` writes `mode: attested`, and
`validate` keys the act rules on the mode and warns on a childless
`mode: none` episode. Its `--via` and `--control` flags, its container
checks and its default container standpoint already match.

## Open Questions

None for this change. *A harness's own acts without a record* stays open in
*Status*.
