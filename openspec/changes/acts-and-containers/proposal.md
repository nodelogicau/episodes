## Why

A self-attested act and a container are the two episodes with no content of
their own, and the draft tells them apart by what is missing: an episode with
`content.mode: none` that no episode names as its `container` is an act. Five
issues come from that rule, or need it settled first:

- **A childless container is read as an act** (#21). A conversation container
  whose first turn was never written, after a crash or a partial copy, matches
  the act shape. It then fails the act rules and is invalid, though nothing is
  wrong with it.
- **A container's `standpoint` has no stated meaning** (#34). It is required,
  and writers fill it differently. Under the shape rule it also decides
  whether a childless container is valid.
- **The rule that an act names its attestation depends on the writer's good
  behaviour** (#25). The issue proposed keying it on `source.harness`, which
  would catch a connector that logs acts from a dedicated control.
- **`container` has no rule for a target that does not resolve,** or for the
  order in which a container and its children are recorded (#20).
- **The draft says episodes are "written by AI harnesses"** (#17), though most
  of what an episode holds needs no model to write. It also leaves unclear
  what `source.harness` names when a connector recorded the episode.

Issues #17, #20, #21, #25 and #34, and the review comments on each.

## What Changes

- **BREAKING: a self-attested act says that it is one.** Its content is
  `{mode: attested}`, a fourth mode beside `inline`, `ref` and `none`.
  `content` says where the record lives, and for an act the record is the
  standpoint's own word. A validator applies the act rules to every episode
  with `mode: attested`, and to no other. Recognition by shape is removed.
- **`mode: none` means a container with nothing of its own, and only that.**
  One with no children is valid whatever its standpoint. A validator warns on
  it, naming the episode, because a container is not meant to stay empty.
  Writers still SHOULD write a container together with its first child.
- **The `standpoint` of a container with nothing of its own is the one whose
  record the container is:** the person in a conversation with a harness, the
  mailbox owner for a mail thread. It says nothing about who spoke within it.
  Each child states its own. A container with content of its own, such as an
  email with attachments, keeps the standpoint its content gives it.
- **An act may be a container.** The mode alone makes an act, so an episode
  may name one as its `container`, as notes attached to a logged meeting
  would.
- **An act links `via` its attestation whenever the writer recorded one.** When
  the attestation was made in an episode the writer recorded, which includes
  every attestation made in conversation, the act MUST link `via` that
  episode. An act attested through a dedicated control has no `via`, as now.
  The rule does not depend on `source.harness`.
- **`container` is treated as links are.** One that does not resolve is
  reported as unresolved and does not make the episode invalid. A writer MUST
  record a container before its children. A validator warns when both ids are
  UUIDv7 and the container's sorts later.
- **Episodes are written by harnesses and connectors.** The opening line
  changes. `source.harness` names whatever recorded the episode, an AI harness
  or a connector such as `gmail-sync`, and `model` is present only when a
  model took part.
- **An informative note separates recording from what follows it:** recording
  (parsing, no model needed), selection and consolidation. Only recording
  belongs to this format.
- `content.language` is not carried with `mode: attested`, as it is not with
  `mode: none`.

## Capabilities

### New Capabilities

- `containment`: `container` and containers, covering:
  - `mode: none` is a container with nothing of its own, valid with or
    without children, with a warning when it has none;
  - whose standpoint such a container's is;
  - a container is recorded before its children;
  - a `container` that does not resolve is reported, not invalid.
- `recording-source`: who writes episodes, covering:
  - `source.harness` names whatever recorded the episode, a harness or a
    connector;
  - `source.model` is present only when a model took part;
  - recording a trace requires no model.

### Modified Capabilities

- `self-attested-acts`:
  - *An act with no record can be recorded as self-attested*: its content is
    `{mode: attested}`, and it links `via` its attestation whenever the writer
    recorded one;
  - *Shape, not kind, makes a self-attested act* is replaced: the mode makes
    an act, whatever its `kind` and whether or not anything names it as
    `container`.
- `content-language`: *Content with no mode carries no language* also covers
  `mode: attested`.

## Impact

- `README.md`:
  - the opening paragraph;
  - *Source and timestamp*;
  - the `content` row of the `EPISODE` table, and the `mode: none` paragraph
    in `content`;
  - *`standpoint`*, with a sentence on containers;
  - *Containment*;
  - *Self-attested acts*, including its example;
  - *When an episode is recorded*, with the informative note.
- **Existing files.** An act written under the current draft has
  `mode: none`. Under this change it reads as a childless container: valid,
  with a warning, and no longer checked as an act. The format is a draft and
  episodes are not rewritten, so the text says this plainly and offers no
  conversion.
- episodes-cli follows, each to be raised as an issue there:
  - `act` writes `mode: attested`, and `validate` keys the act rules on it;
  - `validate` drops the act rules for a childless `mode: none` episode and
    warns in their place;
  - `--via` and `--control` already match the attestation rule
    (episodes-cli#4).
  Its container checks and its default container standpoint already match.
- Closes #17, #20, #21, #25 and #34.
