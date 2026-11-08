# Episodes Format

An open format for episodic memory: what happened, when and where, from whose
standpoint, and where the record of it lives. Designed to be written by AI
harnesses, reviewed by people through git, and cited by the
[Dialectical Knowledge Format](https://github.com/nodelogicau/particulars) and
[intentions](https://github.com/nodelogicau/intentions) by reference rather
than by shared schema.

> **Draft.** Nothing in this document is declared. Field names and the file
> layout will change before `episodes/0.1`.

---

## The Problem

A harness that helps a person keeps two kinds of memory today. What is believed
goes into a DKF workspace as claims; what is meant goes into an intentions
workspace. What actually happened has nowhere to go.

So it is pushed into the format built for belief. A person who wants to record
that the certificate was renewed on Tuesday writes a DKF claim about the event,
and that claim is now open to reconciliation, contradiction and synthesis,
none of which apply: you don't reconcile a past event, only beliefs about it.
intentions says outright that a retrospective account is not its job. And the
conversations in which a person tells their assistant all of this are kept by
no format at all. They live in the harness's own chat history, which is
proprietary, per account, and invisible to every other harness, so the one
thing a claim most often comes from is the one thing it cannot cite.

[Forgetting](https://forgetting.fyi) names this as the family's gap and says why
it matters: episodic memory is where the loop between intending and doing
closes. Without a record of what was done there is nothing to compare with
what was meant, nothing for a self-understanding to cite, and no basis for
asking whether a person is becoming who they meant to be.

---

## Purpose

This format is **episodic memory that keeps its standpoint**: a record of
things that happened, each located in time and place, each saying whose
experience or record it is, and each pointing at where the content lives.

It is the third member of a family:

| Memory | Format | Holds | Changes by |
|---|---|---|---|
| semantic | [particulars](https://github.com/nodelogicau/particulars) | what is believed | reconciliation |
| prospective | [intentions](https://github.com/nodelogicau/intentions) | what a person means to do | resolution and retirement |
| episodic | episodes | what happened | accumulation only |

The formats are coupled only by reference, and only in one direction: a DKF
claim cites an episode as its evidence, and an episode cites nothing in either
of the other formats. Neither of them validates an episode, and this
specification is complete without them: an episodes workspace can be written,
read and validated by an implementation that knows nothing of DKF or
intentions (see [Conformance](#conformance)).

*Forgetting* leaves open whether episodes are a third format or a DKF
extension. They are a third format, for the reason that paper gives for
separating the kinds at all: a store that treats them the same gets at least
one of them wrong. An episode needs no dialectic and must never be revised,
and a DKF object exists to be revised. That episodes would be cited by claims
constantly argues only for a clean reference, and DKF already has one:
`source.document.ref` may name something its reader cannot fetch, such as a
conversation, and an episode id is exactly that.

Procedural memory remains outside the family's formats; see *Forgetting* §8.

---

## The Approach

**An episode records and never interprets.** Interpretation is what DKF is for,
and projection is what intentions is for. The division follows the three
dimensions of time in Heidegger's account of temporality (*Being and Time*,
§65): having-been, the present in which things are taken up and understood,
and the future one projects towards. Episodes are what has been, the given
that cannot be revised. Particulars are the working-over of what was given.
Intentions are projection, already grounded in that account and in Bratman's.

The split matters because the same event supports different readings, and the
reading is where agency lives. Two people can live through the same meeting
and take different beliefs from it; one person can revise what they took from
it a year later. If the event and its reading are stored together, revising the
reading rewrites the event. Kept apart, the event stays fixed and every reading
of it cites the same record.

It follows that an episode carries nothing that is a judgement: no topics, no
confidence, no sentiment, no summary, no claim that it went well or fulfilled
anything. Each of those is a DKF claim citing the episode.

**Most episodes are traces, not copies.** An email, a calendar event and a file
already have a home. An episode about one of them holds a pointer, a hash to
show whether the thing pointed at has changed, and enough metadata to stand as
a record after the thing is gone. The content lives where it lives. The
exception is content that has no other home, chiefly a person's conversations
with a harness, which the episode holds inline.

**Episodes don't break down; they are where reflection happens.** In
*Forgetting*'s terms, a belief breaks down when it is contradicted and a plan
when it is blocked. A record of what happened is never wrong as a record. It
becomes useful at the moment a person steps back and asks whether they acted as
they meant to, which is why it must be complete, located and trustworthy, and
why it must not editorialise.

Kierkegaard put the asymmetry in a line: "Life can only be understood
backwards; but it must be lived forwards" (*Journals*, 1843, tr. Dru). The
family divides that sentence between its formats. intentions holds the living
forwards. Particulars holds the understanding. Episodes hold the backwards: what
the understanding is reached from, and what it has to answer to. Without them,
understanding has nothing to look back on but its own earlier conclusions.

---

## Conformance

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted
as described in [BCP 14](https://www.rfc-editor.org/info/bcp14)
([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119),
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they
appear in all capitals.

[Core Object Types](#core-object-types) and [File Layout](#file-layout) are
normative, except where a passage is marked informative. Every other section
is informative.

This specification is complete on its own. A writer, reader or validator
conforms by implementing the normative sections alone, with no DKF or
intentions code, data or workspace. Where the normative text names a sibling
format, it either is marked informative or says only what an episode does not
hold.

---

## Core Object Types

The format defines one object type, `EPISODE`, and two blocks that may be
appended to it: `source_status`, an observation about whether the referenced
content can still be reached, and `redacted`. Everything else is
implementation.

### Identifiers

Every episode id is `epi_` followed by a lowercase canonical UUID version 7
([RFC 9562](https://www.rfc-editor.org/rfc/rfc9562)):

```
epi_01a1b4b3-0d5e-7f61-8c24-a3e7b9f10d58
```

UUIDv7 is time-ordered, so a directory listing is a chronological log of when
episodes were recorded. Implementations MUST mint with a monotonic counter so
that ids created within the same millisecond still sort in creation order. The
instant in the id is the **recording** instant; when the episode happened is
`occurred`, and consumers MUST NOT require the two to agree. An episode is
often recorded long after it happened.

Readers MUST accept any id matching `^epi_[A-Za-z0-9-]+$`. Validators MAY warn
on ids that are not UUIDv7.

### Field order

The order in which fields are shown below is the canonical order. Writers
SHOULD emit fields in it; readers MUST accept any order and MUST NOT reject a
file for its arrangement. Fields an implementation adds are written after all
specified fields. A reader MUST NOT reject a file for a field this
specification does not define, and MUST give such a field no meaning under
this format; an `occasion` left by an earlier draft is such a field.
Canonical order is what makes two implementations produce byte-identical files
for identical episodes, and so what makes a workspace reviewable as a diff.

### Source and timestamp

Every episode carries a `source` block and a `timestamp`. (Informative: this is
the same shape DKF and intentions use, so one harness can write all three.)

```yaml
source:
  author: https://github.com/benfortuna   # on whose behalf this was recorded
  harness: claude                          # optional: the harness that recorded it
  model: claude-opus-5-5                   # optional: the model
timestamp: 2026-11-07T06:09:18Z            # recording time, RFC 3339 UTC
```

`source` says who **recorded** the episode. It MUST contain at least one of
`author` or `harness`; a harness recording a conversation on its own is a valid
source. `author` is a **reference**: the person or agent on whose behalf the
episode was recorded.

A reference, here and in `standpoint`, `participants` and `place`, is a URI
where one is known, and otherwise a string that identifies a person, agent or
place to whoever wrote it. Resolving a reference is outside this format. A
reference that nothing can resolve is still valid, and a reader MUST NOT reject
an episode for one. (Informative: a DKF workspace may treat these values as
particulars.)

`source` is not the same as `standpoint`, below. A harness may record, on Ben's
behalf, an email that Jane sent: the source is the harness acting for Ben; the
standpoint is Jane's. Collapsing the two is the source-monitoring failure the
family exists to prevent (Johnson, Hashtroudi and Lindsay 1993), in which a
person keeps what was said and loses who said it.

Every timestamp field is an [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339)
`date-time`. Writers write recording instants in UTC with `Z` at seconds
precision. `occurred` is the exception, below.

### `EPISODE`

```yaml
# episodes/2026-11/epi_01a1b4b2-3c1d-7e5a-9f02-6b8c4d2e1a37.yaml
id: epi_01a1b4b2-3c1d-7e5a-9f02-6b8c4d2e1a37
type: episode
kind: message
occurred:
  start: 2026-11-07T14:24:00
  tz: Australia/Melbourne
  basis: recorded
standpoint: https://github.com/benfortuna
participants:
  - https://github.com/benfortuna
  - https://claude.ai
container: epi_01a1b4b1-8a20-7d43-b6e1-0c9f5a7d3e12
ordinal: 7
content:
  mode: inline
  media_type: text/markdown
  derivation: verbatim
  text: |
    where does llm inference/agentic looping fit in this design? i assume
    conversations is a loop, with particulars and intentions as tools
source:
  author: https://github.com/benfortuna
  harness: claude
timestamp: 2026-11-07T03:24:40Z
```

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | `epi_` + UUIDv7. |
| `type` | yes | Always `episode`. |
| `kind` | yes | What sort of happening this is: `conversation`, `message`, `email`, `event`, `note`, `upload`, `call`, `activity`, or another short lowercase word. **Descriptive only**: it drives display and filtering, never which fields are valid. A reader MUST NOT reject an unknown `kind`. |
| `occurred` | yes | When it happened, below. |
| `standpoint` | yes | A reference to the person or agent whose act, utterance or experience this records, below. |
| `participants` | no | References to those present or addressed, sorted. May include the standpoint. |
| `place` | no | A reference to where it happened. |
| `label` | no | A short human-readable name for the episode, such as an email's subject or an event's title, captured when it is recorded. Not a summary. |
| `container` | no | The episode this one is part of: a conversation for its turns, a thread for its messages, an email for its attachments. |
| `ordinal` | no | Position within `container`, an integer from 1. Required when `container` is present and order is meaningful. |
| `content` | yes | Where the record of it lives, below. A container with no content of its own, and a self-attested act with nothing to hold its attestation, carry `content: {mode: none}`. |
| `source` | yes | Who recorded it. |
| `timestamp` | yes | When it was recorded. |
| `source_status` | no | Whether referenced content can still be reached, below. |
| `redacted` | no | A redaction block, below. |

#### `occurred`

```yaml
occurred:
  start: 2026-11-07T14:24:00     # local date-time, no offset
  end: 2026-11-07T15:10:00       # optional
  tz: Australia/Melbourne        # IANA zone name
  basis: stated                  # recorded | stated | inferred
```

`start` and `end` are local date-times interpreted in `tz`, an
[IANA time zone](https://www.iana.org/time-zones) name, not UTC instants and
not offsets. An offset is a fact about one instant; a zone is a fact about a
place. A claim that resolves "tomorrow at 2" against an episode must compute
the offset at the instant referred to, which may lie across a daylight-saving
transition from the instant of utterance, and only a zone allows that. A date
alone (`2026-11-07`) is valid when the time is unknown.

`basis` says how the time is known. `recorded`: the harness observed it as it
happened, as with a conversation turn. `stated`: a source gave the time of the
happening itself, as with an email's `Date` header or a calendar event's
creation time. `inferred`: it was worked out, as with "last Tuesday" in a note
written today. A source can lie, and a clock can drift; `basis` lets a later
reader weigh the time accordingly instead of trusting all of them alike.

**`occurred` comes from the happening, never from a plan.** A writer MUST take
it from the happening the episode records, by one of the three bases above,
and MUST NOT copy it from a schedule, a plan or a time that was set aside. A
session planned for two that took place at four occurred at four; when it
took place is part of what a comparison of meant against done looks at, and a
copied time erases it. There is no `planned` basis for the same reason.

**Nothing is recorded before it happens.** A writer MUST NOT record an episode
whose `occurred.start` is later than its recording instant, `timestamp`, and
MUST NOT give an `occurred.end` later than it. Either would describe something
that has not happened yet, and episodes are never revised: a meeting recorded
in advance and then cancelled would stay in the record for good. An episode
can be recorded while its happening is still going on, as a conversation is at
its first turn, by leaving `end` out. The comparison interprets `occurred` in
its `tz`, at the offset in force at that local time; a date alone is compared
as a date, in `tz`, with the recording instant's date there.

A validator warns, naming the episode, when either bound is violated. It
warns rather than fails because it cannot tell a writer's mistake from clocks
that disagree by minutes, the writer's or a source's, in the same way it warns
on an id from later than now (see [Sharding](#sharding)).

#### `standpoint`

Every episode is someone's. An email is its sender's record of what they chose
to write. A conversation turn is its speaker's utterance. A calendar event is
the record, kept by the person whose calendar holds it, of what was arranged.
A note is its writer's
account, and when the note says what someone else thinks, the episode is still
the writer's: what Sarah thinks enters the family as a DKF claim reported from
the note, never as Sarah's episode.

`standpoint` is required because nothing downstream can recover it. A claim
consolidated from a conversation must distinguish what the person said from
what the assistant said or suggested, and the only place that distinction is
recorded is the standpoint of the turn it came from. A harness that records its
own turns as the person's has made its suggestions into the person's
statements, and every claim built on them inherits the error.

The standpoint is a reference, as defined under
[Source and timestamp](#source-and-timestamp). A harness speaking in a
conversation is a participant like any other and has a reference of its own.

#### `content`

Content has two modes, decided by whether the record has another home.

**Inline** is for content this workspace is the origin of: a conversation turn,
a typed note, a transcript the harness made itself. The episode is the only
copy, so it holds the text.

```yaml
content:
  mode: inline
  media_type: text/markdown
  derivation: verbatim     # verbatim | transcribed | ocr | rendered
  text: |
    …
```

`derivation` says how the text came to exist. `verbatim`: it is what was typed.
`transcribed`, `ocr`: a model produced it from audio or an image. `rendered`:
it was generated from structured data. The difference is load-bearing for
anything that cites the text. A speech recogniser's invention is a perfect
quote of words nobody said, and every check that a quote appears in its source
will pass. A claim citing a `transcribed` episode inherits that uncertainty,
and an implementation showing the source should play the audio rather than
display the transcript.

**Reference** is for content that lives elsewhere: an email in a mailbox, an
event in a calendar, a file in storage.

```yaml
content:
  mode: ref
  ref: gmail:msg_18f2c3a9b4d5e6f7
  version: "18f2c3a9b4d5e6f7"       # optional: the source's own version id
  hash: sha256:9f2a…                # optional: of the content as fetched
  media_type: message/rfc822        # optional
```

`ref` is a URI or an identifier meaningful to whatever can fetch it. `version`
is the source's own notion of a version where it has one: a calendar event's
sequence or ETag, a file's revision id. `hash` is what lets a later reader tell
that what the pointer now returns is not what was recorded.

**A reference episode records the happening its source witnesses.** For mail,
that is the sending: `occurred` is the `Date` header. For a file, it is the
upload or the writing. For a calendar event, it is the **arranging**: the
episode records that the event was put in the calendar, its `occurred` is when
that was done (the event's creation time, `basis: stated`), and it MUST NOT be
the event's scheduled time. The scheduled time stays where it lives, in the
referenced event, and `label` may carry the event's title as captured.

```yaml
# a meeting for next Tuesday, arranged yesterday, recorded today
kind: event
occurred: {start: 2026-11-07T16:02:00, tz: Australia/Melbourne, basis: stated}
label: Budget review with Jane
content:
  mode: ref
  ref: gcal:evt_7q2m4k9d0s1a
  version: "3"
```

A calendar is a record of what was arranged, not of what took place. A
meeting that was arranged and never held leaves the same calendar event as one
that was held, so an episode of the calendar is not evidence that the meeting
happened. That needs a record of the meeting itself: a turn, a note, a
transcript, attendance from the system that hosted it. Read this way, a
calendar episode is true when it is recorded and can be recorded at any time
after the arranging, including before the meeting.

`hash` is written `<algorithm>:<digest>`. It is taken over the content as
fetched, with CRLF sequences normalised to LF and *nothing else* altered: not
trailing whitespace, not Unicode normalisation form, not a final newline. Line endings are an artefact of transport and differ
by platform; everything else differs because someone changed the content, and
the check must see it. Writers MUST write `sha256`. Readers MUST accept any
`<algorithm>:<digest>` and MUST report an algorithm they do not implement as
unverified, never as invalid. (Informative: this is DKF's rule, so a DKF claim
and the episode it cites can carry the same hash.)

A reference episode MUST NOT carry `text`. That is the format's rule against
ingestion: an episode about an email is a trace of the email, not a copy of it,
and a mailbox remains the system of record for mail. Whatever cites the episode
carries the words it relies on as its own quote, so it stays verifiable without
the episode store holding the message. (Informative: in DKF that quote is
`source.document.quote`.)

`content: {mode: none}` is valid in exactly two cases: a container with nothing
of its own, such as a conversation whose turns are its children, and a
[self-attested act](#self-attested-acts) with nothing to hold its attestation.
Writers SHOULD write a container together with its first child, so that a
container is never seen without one.

#### Containment

`container` and `ordinal` model every case of one thing inside another with a
single mechanism: the turns of a conversation, the messages of a thread, the
attachments of an email, the pages of a scanned document. The parent is an
episode; each child is an episode whose `container` names it.

One episode holds at most one piece of content. An email with three
attachments is four episodes. This keeps a citation unambiguous: a claim that
cites an episode cites one text or one referenced thing, never "somewhere in
this email and its attachments".

A child inherits nothing it does not state. In particular `standpoint` is
stated on every turn of a conversation, because the speaker alternates and the
distinction is what consolidation depends on.

#### Self-attested acts

Much of what a person does leaves no record: a solo block of deep work, a run,
a phone call nobody logged. A **self-attested act** is the episode for one. It
records something its standpoint did, its `occurred` is when the act took
place, and its record is that person's own attestation that they did it.

```yaml
# episodes/2026-11/epi_01a1b875-0c28-7e19-a3d5-7c1b9f4e2a60.yaml
id: epi_01a1b875-0c28-7e19-a3d5-7c1b9f4e2a60
type: episode
kind: activity
occurred:
  start: 2026-11-08T09:00:00
  end: 2026-11-08T10:30:00
  tz: Australia/Melbourne
  basis: stated
standpoint: https://github.com/benfortuna
label: Deep work on the budget draft
content:
  mode: ref
  ref: epi_01a1b874-e130-7b2c-9d41-3f6a8e0c5b27   # the turn: "log ninety minutes of deep work from nine"
source:
  author: https://github.com/benfortuna
  harness: claude
timestamp: 2026-11-08T00:00:41Z
```

Its `content` takes one of two forms:

- **The attestation is an episode in the workspace,** such as the turn in which
  the person asked for the act to be logged, or a note they wrote:
  `{mode: ref, ref: <that episode's id>}`. A reader resolves an `epi_` ref in
  its own workspace. No `hash` is needed, because episodes are not revised.
- **Nothing holds the attestation,** as when the person presses a control whose
  only purpose is to log the act: `{mode: none}`.

**It is self-attestation only.** A self-attested act's `standpoint` MUST equal
its `source.author`. When its `content` refs an episode that resolves in the
workspace, that episode's `standpoint` MUST equal the act's. A ref that does
not resolve, because its episode was redacted, dropped or never copied, is
reported as unresolved and is not invalid. Someone else's act is never
recorded this way: what Jane says she did is in the episode in which she says
it, and is taken from there the way the [`standpoint`](#standpoint) section
describes for notes.

**It is recorded only on explicit attestation.** A writer MUST record a
self-attested act only when its standpoint explicitly attests it, by asking
for it to be recorded or through an action whose purpose is recording it, and
MUST NOT record one from what it infers. A passing "finally got the budget
done" is a turn and stays a turn; whatever is taken from it is an
interpretation, outside this format. (Informative: in the family, that is a
DKF claim citing the turn.) This keeps a harness a scribe and not an
interpreter. No validator can check it, so it is a rule for writers.

**It is recognised by shape, not by `kind`.** A validator treats as a
self-attested act every episode with `content.mode: none` that no episode
names as its `container`, and every episode whose `content.ref` is an episode
id, and applies the rules above to it whatever its `kind`. `activity` is the
recommended `kind` and stays descriptive. A container with `mode: none` is
valid whatever its standpoint.

**It is timed from the act.** `occurred` is when the act took place: `stated`
when the person gave the time, `inferred` when it was worked out, as with
"this morning". The rule that [nothing is recorded before it
happens](#occurred) applies: a block logged at ten as "nine to half past ten"
is recorded with its `start` and no `end`, or recorded once it is over.

### `source_status`

A reference episode points at something the format does not control. The thing
may be edited, moved, or deleted, or the harness may lose access to it.
`source_status` records what was last observed:

```yaml
source_status:
  state: gone                       # available | changed | unreachable | gone
  verified: 2026-11-02T09:00:00Z    # last time the state was checked
  detected: 2026-11-07T05:50:00Z    # when the current state was first seen
```

| State | Meaning |
|---|---|
| `available` | Fetched, and the hash (if any) matches. |
| `changed` | Fetched, and the hash or version no longer matches. Usual for calendar events and documents; mail does not change once sent. |
| `unreachable` | Could not be fetched for a reason that may pass: access revoked, a connector disconnected, a network failure. Reversible. |
| `gone` | Confirmed deleted at the source. |

The block is the one part of an episode that is rewritten in place, because it
is an observation about the world outside the workspace, not about what
happened. Its history is git's. It is never part of the index.

When a source goes, the episode keeps everything it was recorded with: its id,
kind, time, standpoint, participants, label, container, pointer and hash. It
gains a state and nothing else. Writers MUST NOT back-fill content when a
source is detected as changed or gone: it is usually too late, and it would
turn a trace into the copy the format refuses to keep. What survives of the
content is whatever quote each citing claim carries, which is why a claim
citing a `gone` episode is still verifiable against its own quote, and why its
reader should be told *source no longer available, quote retained* rather
than *retracted*.

A source being deleted is not a request to forget. People delete mail to tidy
an inbox. Forgetting is redaction, below, and is always explicit.

### Redaction

Redaction removes text from an episode and keeps the episode: its id, its place
in a container, and a record of who removed what, when and why. Every rule for
it is stated here. (Informative: the block has the shape of
[DKF's redaction](https://github.com/nodelogicau/particulars#redaction), and the
rules are DKF's adapted to episodes.)

```yaml
redacted:
  timestamp: 2026-11-07T06:30:00Z
  reason: Personal matter; the record is no longer wanted
  source: {author: https://github.com/benfortuna}
  fields: [label, content.text]
```

`timestamp`, `reason`, `source` and `fields` are all required, and the block is
written last in the file. `reason` MUST NOT restate what was removed; no tool
can check that, so it is a rule for whoever writes one.

Every path listed in `fields` is absent from the file. A field the format
otherwise requires (`content.text` on an inline episode, `content.ref` on a
reference episode) is valid when absent **only** because `fields` lists it.
That is how a validator tells a redacted episode from a malformed one: an
inline episode with no `text` and no `redacted` block listing it is rejected.

**What can be redacted is a closed set:** `label`, `participants`, `place`,
`content.text`, `content.ref`, `content.version`, `content.hash`. A writer
refuses any other path and a validator rejects a file listing one. The set is
closed because none of these is mirrored in the [index](#indexyaml), and sealed index segments never change, so a redaction
must never change an entry. `id`, `kind`, `occurred`, `container`, `ordinal`,
`standpoint` and `timestamp` cannot be redacted. That costs something, since
the fact that one person addressed another at a given time can itself be what
someone wants forgotten, and it is left to a later version that can mask index
entries.

**Redacting `content.text` withdraws an inline episode.** It carries no record,
so it is out of recall, and anything that quotes it can no longer be checked
against it. Redacting `content.ref` leaves a reference episode as a bare tombstone: it says that
something of this kind happened at this time from this standpoint, and no
longer where.

**It is irreversible and never implicit.** The block is never removed and a
redacted field is never restored. A file carries at most one `redacted` block;
redacting again replaces its `timestamp`, `reason` and `source` and makes
`fields` the union of old and new. Nothing redacts as a side effect: not a
source being deleted, not anything that cites the episode being withdrawn or
redacted.

**Redaction does not cascade.** Redacting an episode changes no other episode,
not its container and not its children, and no object outside the workspace.
(Informative: in a DKF workspace, claims citing a redacted episode become
unverifiable and are reported, so a person can decide whether to redact them
too. An implementation of both formats may offer "redact this episode and the
claims citing it" as one action, provided it writes a separate `redacted`
block on each object it changes. Redacting a claim changes no episode.)

**What redaction does not remove.** It removes text from the current file and
from what a conformant implementation reads, recalls, serves and embeds; an
implementation that keeps embeddings deletes those of a redacted field,
because an embedding can disclose what it was computed from. It does not
remove the text from version control, clones or earlier fetches. Inline
episodes are whole conversations, so in a git workspace the text of every
redacted turn stays in history, and an implementation whose store is a git
repository MUST say so when it redacts. An implementation whose store controls
access to earlier versions MAY restrict it; nothing in the format depends on
whether it does. Erasure from history is a property of the store, not of the
file.

### What a workspace does not say

A workspace is not an exhaustive record. Referenced content is recorded when
something needs it, an implementation may drop episodes nothing cites, and
much of what a person does leaves no record anywhere. An unrecorded happening
and a non-happening look the same.

A reader or consumer MUST NOT treat the absence of an episode as evidence that
something did not happen. A finding that something was not done, for an
interval in which it was planned or for any other, needs evidence of its own;
an empty interval in the workspace is not that evidence.

---

## Object Model

```
  mailbox · calendar · storage           harness conversations, notes
              ▲                                       │
              │ content.ref (trace)                   │ content.text (inline)
              │                                       ▼
          EPISODE ◀──── container ──── EPISODE (turn, message, attachment)
              ▲
              │  (informative: cited from outside the format)
              │
   DKF claim: source.document.ref = epi_…, quote = the words relied on
```

### Relation to other formats

*This section is informative. It describes how the sibling formats can use
episodes and places no requirement on an episodes implementation.*

An episode cites nothing outside its own workspace. The other formats cite it.
A DKF claim does so through `source.document`:

```yaml
source:
  author: https://github.com/benfortuna
  harness: claude
  document:
    ref: epi_01a1b4b2-3c1d-7e5a-9f02-6b8c4d2e1a37
    author: https://github.com/benfortuna    # the episode's standpoint
    quote: i assume conversations is a loop, with particulars and intentions as tools
```

`document.author` is the episode's standpoint, which is what lets DKF's
*reported from* relation work across formats: a claim citing a turn the
assistant spoke is reported from the assistant, not from the person. The
episode id is the `ref`; DKF already allows a `ref` that names something its
reader may be unable to fetch. A reader with the episodes workspace can
resolve it; one without can still read the quote.

An episode does not name the intention it realised, and intentions does not cite
episodes. That something happened in the place held for an intention, or
reported it done, or fulfilled it, is a judgement about the episode, so the
link between the two is a DKF claim citing both. This is where the family's
loop closes: intentions retires an intention as `fulfilled`, an episode
records what took place, and a claim citing the episode is the evidence that
turns a self-claim from aspiration into description. Recording an episode
changes no file in either of the other formats.

**Retiring as `fulfilled` is not evidence.** intentions records its own
judgement, `retired: {kind: fulfilled, …}`, and it is the person letting the
intention go: they consider it done, or done enough to stop holding. Its
`timestamp` is when the retirement was written, not when anything happened.
It need not agree with what claims make of the episodes, and when it does not,
nothing is in conflict: a claim that the intention was not really fulfilled
sits beside the retirement as one reading beside another. Whether a
retirement may point at the episodes it was decided on is a question for
intentions.

**A calendar hold is the plan, not its evidence.** A harness may write a busy
hold into a person's calendar from an intention's placement, and the hold stays
after the intention is retired. An episode of that hold records that the time
was set aside, as every calendar episode records an arrangement (see
[`content`](#content)). A claim that the intention was fulfilled which cites
only such an episode cites the plan as evidence for itself. The same holds for
an event imported from someone else's calendar.

### When an episode is recorded

The format says what an episode is, not when one must exist. Three practices
are expected, and all are implementation choices within the rules above:

- **Inline content is recorded as it happens.** A conversation has no other
  home, so a harness that wants to cite it later records every turn when it is
  spoken.
- **Referenced content is recorded on demand.** Most mail is not worth a
  record. An implementation can record a reference episode at the moment
  something durable first cites the thing it points at, such as a claim, an
  intention or an explicit request to keep it, and write the episode and the
  citing object together so that neither exists without the other.
- **A self-attested act is recorded when the person says so.** An act that left
  no record is written on its standpoint's explicit request, never from what a
  harness infers (see [Self-attested acts](#self-attested-acts)).

Whether an episode that nothing cites any longer is kept or dropped is likewise
the implementation's decision. Both practices leave gaps, which is why a
missing episode means nothing (see
[What a workspace does not say](#what-a-workspace-does-not-say)).

---

## File Layout

```
/episodes.yaml                 workspace marker and configuration
/episodes/
  2026-09/                     sealed: an id two months later exists
    …
  2026-11/
    epi_01a1b4b1-8a20-7d43-b6e1-0c9f5a7d3e12.yaml
    epi_01a1b4b2-3c1d-7e5a-9f02-6b8c4d2e1a37.yaml
  legacy/                      only if ids exist from which no month derives
/index.yaml                    derived cache: the open months
/index/
  2026-09.yaml                 sealed segments, one per sealed month
  legacy.yaml                  only if legacy/ exists
```

(Informative: the layout follows DKF's
[sharding](https://github.com/nodelogicau/particulars#sharding), adapted to a
format with one object type and no retractions. Every rule is stated below.)

### Sharding

**A file's path derives from its id and nothing else.** A UUIDv7 carries its
minting instant in its first 48 bits; the calendar month of that instant, in
UTC, is the shard. An episode minted on 2026-11-07 UTC lives at
`episodes/2026-11/<id>.yaml`, whatever its `occurred` or `timestamp` say. A
reader never guesses the layout from what it finds on disk: a file in a
directory its id does not derive is a validation failure naming the file and
the path its id derives.

**`legacy/` holds ids from which no month derives:** an identifier part that
is not a UUID, or a UUID of a version other than 7. Such an episode lives at
`episodes/legacy/<id>.yaml` and its index entry in `index/legacy.yaml`. A
UUIDv7 with an implausible instant still derives a month. Conformant writers
mint only UUIDv7, so a legacy id arrives only by copy, merge or a
non-conformant writer. The directory is never sealed.

**A month is sealed** once any id in the workspace was minted two or more
months after it. The newest id's month and the month before it are open. The
month of grace is what lets a branch minted on 28 November merge on 5
December, after the main line has minted in December, and it absorbs clock
skew of hours or days at a boundary. An implementation MUST NOT mint into a
sealed month.

**Sealing stops a month gaining files, not its files changing.** A file in any
month, open or sealed, may change in exactly two ways: its `source_status` is
rewritten, or it gains or extends a `redacted` block and loses the fields that
block lists. Neither changes an index entry. Any other change to an existing
file is non-conformant, in an open month and a sealed one alike.

**A late merge is detected by count.** Each sealed segment records `count`, the
number of files in its month's directory. A rebuild or validation compares a
directory listing against the count and parses nothing unless they differ. A
difference means a branch open across two or more month boundaries has added
files to a sealed month: validation fails naming the files, and the remedy is
to re-mint the branch's episodes before merging.

**A future id is a broken clock.** A validator warns, naming the episode, on any
id minted or `timestamp` dated later than now, and fails on an id minted two or
more months after its own current month, because such an id would seal the
month every correct writer is minting into.

### `episodes.yaml`

```yaml
format: episodes/0.1
workspace:
  id: 01a1b4b0-5f3a-7b08-a1d9-4e6c2b8f7a90   # bare UUIDv7
defaults:                                     # optional; writers only
  source:
    author: https://github.com/benfortuna
    harness: claude
```

`format` and `workspace.id` are required. A reader MUST refuse a workspace
whose `format` it does not implement, naming the version, rather than read
what it can. Unknown keys are ignored.

### `index.yaml`

The index is a cache of the files, never the reverse. The episode files are
the source of truth; the index MUST be fully reconstructible from them, and a
consumer MUST NOT return wrong results because the index is missing or stale
(it may be slower). Two branches that each add an episode both touch
`index.yaml`, and the conflict is resolved by regenerating it, never by hand.
The index stays committed because an HTTP consumer cannot list a directory, and
for it the index is how episodes are enumerated; it should treat the index as
possibly lagging the files.

The root, `index.yaml`, lists the segments and holds the entries for the open
months. Each sealed month, and `legacy`, has a segment holding its entries:

```yaml
# index.yaml
format: episodes/0.1
segments:
  - path: index/2026-09.yaml
    count: 412
entries:                       # minted in an open month
  - id: epi_01a1b4b2-3c1d-7e5a-9f02-6b8c4d2e1a37
    kind: message
    occurred: {start: 2026-11-07T14:24:00, tz: Australia/Melbourne, basis: recorded}
    container: epi_01a1b4b1-8a20-7d43-b6e1-0c9f5a7d3e12
    ordinal: 7
    standpoint: https://github.com/benfortuna
    timestamp: 2026-11-07T03:24:40Z
```

```yaml
# index/2026-09.yaml — a sealed segment
format: episodes/0.1
entries:
  - id: epi_…
    …
```

When a month seals, its entries leave the root for a new segment, and the root
gains that segment's `path` and `count`. A segment's `count` equals the number
of files in its month's directory, and a segment never changes once written.

Each entry mirrors exactly `id`, `kind`, `occurred`, `container`, `ordinal`,
`standpoint` and `timestamp`, which is what recall by time, by conversation and
by speaker needs, and is also exactly the set redaction cannot touch. Nothing
in `content`, `label`, `participants`, `place` or `source_status` enters the
index, so each of them stays redactable or rewritable without changing a
sealed segment.

---

## Design Principles

**Record, never interpret.** An episode says what happened, from whose
standpoint, when and where, and where the record is. Every judgement about it
is a claim in another format.

**Accumulation only.** Episodes are not revised. A better transcript is a new
episode, never an edit of the old one. The only in-place changes are an
observation about the source's reachability and a redaction.

**Point, don't copy.** What has a home elsewhere stays there. The format holds
text only when nothing else does.

**Standpoint is structural.** Who an episode belongs to is a required
reference, because every claim built from it depends on knowing, and nothing
downstream can recover it.

**Forgetting is explicit.** Nothing is redacted as a side effect, and the
format says plainly what redaction cannot reach.

**Compose by reference, in one direction.** Episodes cite no object in any
other format and depend on no other specification to be written, read or
validated. The other formats cite episodes, through fields they already have.

---

## Status

Early draft. Nothing is declared and no implementation exists. The object
model above is the first proposal; the open questions below are listed rather
than closed.

- **Derived renderings of referenced media.** A voice memo in storage is
  referenced, but its transcript is the harness's own work and has no other
  home. Is it a child episode with inline `transcribed` content, a second
  `content` block, or outside the format? And when a better transcript is made
  later, how does the new episode say which one it improves on?
- **Citing a span of a referenced source.** A claim's quote is checked by
  appearance, which survives a re-fetch. Whether the format should also define
  a fragment syntax for `ref` (a character range, a timecode, a page) is open,
  given that offsets into a fetched rendering break when the rendering changes.
- **Index masking.** `standpoint`, `participants` and `occurred` together say
  who spoke to whom and when. Redacting that fact needs an index that can mask
  entries, which DKF has also deferred.
- **Size of a conversation episode.** This draft makes a conversation a
  container and each turn an episode. Whether turns should instead be grouped
  into segments by topic, or a whole session be one inline episode, is open,
  and shapes how precisely a claim can cite a conversation.
- **A provenance spine.** `source`, ids, timestamps, the content hash,
  redaction and sharding are copied by agreement from DKF and restated here in
  full, so that this format stands alone. Copies can drift apart. *Forgetting*
  asks whether that shared shape should be its own specification; a third
  format sharpens the question, and standing alone means such a specification
  would have to be one this format restates or can do without.
- **Duplicate recordings.** Two episodes of one happening from different
  standpoints are not duplicates, and whether they are the same event is a DKF
  claim. The same recording made twice is: on-demand recording that runs again,
  two machines recording one email and merging cleanly under different ids, a
  replayed turn taking an `ordinal` already used. Recording "when something
  first cites" a thing implies a lookup by `content.ref`, which the index
  deliberately omits. Should `(container, ordinal)` be unique, should writers
  avoid a second `(standpoint, content.ref)`, and once a duplicate exists, can
  an appended, unindexed block say which episode it repeats? The same relation
  may answer how a better transcript names the one it improves on. Refs that
  alias one thing, such as a provider id and a `Message-ID`, are harder still.
- **A container's end.** An episode is never recorded before it happens, and
  never revised, so a conversation recorded at its first turn carries no
  `occurred.end` and can never gain one. Its end can be read from its last
  turn. Should a container instead be allowed an appended, unindexed
  observation of its end, as `source_status` is appended for a source?
- **A harness's own acts without a record.** A self-attested act is a
  person's. Most of what a harness does leaves a record, a message or a tool
  call, but not all of it. Whether a harness may attest its own acts, and
  how a `standpoint` URI and `source.harness` would then be matched, is open.

---

## References

**Standards borrowed as grammars.**
[RFC 9562](https://www.rfc-editor.org/rfc/rfc9562) UUID version 7 for ids ·
[RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) timestamps ·
the [IANA time zone database](https://www.iana.org/time-zones) for `occurred.tz` ·
[YAML 1.2](https://yaml.org/spec/1.2.2/) as the file format ·
[FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) SHA-256 for
`content.hash`.

**Models.**
[iCalendar](https://www.rfc-editor.org/rfc/rfc5545), whose `VJOURNAL`
component is the oldest open format for a dated record of what happened ·
[W3C PROV-O](https://www.w3.org/TR/prov-o/), which separates an activity from
the agents associated with it, as `standpoint` and `source` are separated here ·
[Activity Streams 2.0](https://www.w3.org/TR/activitystreams-core/), an
actor-centred record of what happened, shaped for feeds rather than memory.

**Conceptual sources.**
Søren Kierkegaard, *The Journals of Søren Kierkegaard*, tr. Alexander Dru
(1938), entry for 1843, on life understood backwards and lived forwards,
behind the division of the family between what happened, what is understood
and what is meant ·
Endel Tulving, "Episodic and semantic memory", in *Organization of Memory*
(1972), for the distinction itself: memory of events located in time and place,
as against facts detached from when they were learned ·
Martin Heidegger, *Being and Time* (1927), §65, on the three ecstases of
temporality, behind the division of the family's formats ·
Paul Ricoeur, *Memory, History, Forgetting* (2000), on the trace and on
testimony, behind treating a reference episode as a trace and every episode as
someone's ·
Marcia Johnson, Shahin Hashtroudi and D. Stephen Lindsay, "Source monitoring"
(1993), on how people keep what was said and lose who said it, behind
`standpoint` ·
Daryl Bem, "Self-perception theory" (1972), on people coming to know
themselves from what they observe themselves doing, behind the closing of the
loop with intentions.

**Ecosystem.**
[particulars](https://github.com/nodelogicau/particulars), semantic memory,
which cites episodes ·
[intentions](https://github.com/nodelogicau/intentions), prospective memory,
linked to episodes by DKF claims ·
[Forgetting](https://forgetting.fyi), the argument the family shares, which
identified this gap.

---

## License

The specification is released under [CC0 1.0 Universal](LICENSE). Reference
implementations are released under the MIT License.
