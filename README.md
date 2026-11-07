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

The formats are coupled only by reference. A DKF claim cites an episode as its
evidence; an episode may name the intention it was the occasion of. Neither
format validates the others, and an episodes workspace is useful on its own.

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
specified fields. Canonical order is what makes two implementations produce
byte-identical files for identical episodes, and so what makes a workspace
reviewable as a diff.

### Source and timestamp

Every episode carries a `source` block and a `timestamp`, in the shape DKF and
intentions share:

```yaml
source:
  author: https://github.com/benfortuna   # on whose behalf this was recorded
  harness: claude                          # optional: the harness that recorded it
  model: claude-opus-5-5                   # optional: the model
timestamp: 2026-11-07T06:09:18Z            # recording time, RFC 3339 UTC
```

`source` says who **recorded** the episode. It MUST contain at least one of
`author` or `harness`; a harness recording a conversation on its own is a valid
source. `author` is a reference to a particular, written as a URI where one is
known, as in DKF.

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
| `kind` | yes | What sort of happening this is: `conversation`, `message`, `email`, `event`, `note`, `upload`, `call`, or another short lowercase word. **Descriptive only**: it drives display and filtering, never which fields are valid. A reader MUST NOT reject an unknown `kind`. |
| `occurred` | yes | When it happened, below. |
| `standpoint` | yes | The particular whose act, utterance or experience this records, below. |
| `participants` | no | Particulars present or addressed, as URIs or ids, sorted. May include the standpoint. |
| `place` | no | A particular for where it happened. |
| `label` | no | A short human-readable name for the episode, such as an email's subject or an event's title, captured when it is recorded. Not a summary. |
| `container` | no | The episode this one is part of: a conversation for its turns, a thread for its messages, an email for its attachments. |
| `ordinal` | no | Position within `container`, an integer from 1. Required when `container` is present and order is meaningful. |
| `content` | yes | Where the record of it lives, below. A container with no content of its own carries `content: {mode: none}`. |
| `occasion` | no | The intentions object this episode was the occasion of, as `{id, version}`, below. |
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
happened, as with a conversation turn. `stated`: a source gave it, as with an
email's `Date` header or a calendar event's start. `inferred`: it was worked
out, as with "last Tuesday" in a note written today. A source can lie, and a
clock can drift; `basis` lets a later reader weigh the time accordingly
instead of trusting all of them alike.

#### `standpoint`

Every episode is someone's. An email is its sender's record of what they chose
to write. A conversation turn is its speaker's utterance. A calendar event is
the record of the person whose calendar holds it. A note is its writer's
account, and when the note says what someone else thinks, the episode is still
the writer's: what Sarah thinks enters the family as a DKF claim reported from
the note, never as Sarah's episode.

`standpoint` is required because nothing downstream can recover it. A claim
consolidated from a conversation must distinguish what the person said from
what the assistant said or suggested, and the only place that distinction is
recorded is the standpoint of the turn it came from. A harness that records its
own turns as the person's has made its suggestions into the person's
statements, and every claim built on them inherits the error.

The standpoint is a reference to a particular. A harness speaking in a
conversation is a participant like any other and has a URI.

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
sequence or ETag, a file's revision id. `hash` follows DKF's definition
(SHA-256 over the content with CRLF normalised to LF and nothing else changed),
and is what lets a later reader tell that what the pointer now returns is not
what was recorded.

A reference episode MUST NOT carry `text`. That is the format's rule against
ingestion: an episode about an email is a trace of the email, not a copy of it,
and a mailbox remains the system of record for mail. The evidence a claim needs
travels with the claim, in DKF's `source.document.quote`, so a claim stays
verifiable without the episode store holding the message.

A container with nothing of its own, a conversation whose turns are its
children, carries `content: {mode: none}`.

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

#### `occasion`

```yaml
occasion: {id: int_01a06d20-5a3b-7e88-b1c4-7d9e0f2a4c66, version: 4}
```

An episode MAY name the intentions object it was the occasion of: the session
of writing that an intention was placed for, the meeting a commitment held a
place for. It is a factual link, recorded when the harness creates the episode
from the placement itself, and it says only *this happened in the place that
was held for that*. Whether the intention was thereby fulfilled, done well, or
done at all is a judgement, and so a DKF claim citing both.

This is where the family's loop closes. intentions retires an intention as
`fulfilled`; an episode records what took place; a claim citing the episode is
the evidence that turns a self-claim from aspiration into description.

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
in a container, and a record of who removed what, when and why. It follows
[DKF's redaction](https://github.com/nodelogicau/particulars#redaction) in shape
and in every rule this section does not change.

```yaml
redacted:
  timestamp: 2026-11-07T06:30:00Z
  reason: Personal matter; the record is no longer wanted
  source: {author: https://github.com/benfortuna}
  fields: [label, content.text]
```

`timestamp`, `reason`, `source` and `fields` are all required. `reason` MUST
NOT restate what was removed.

**What can be redacted is a closed set:** `label`, `participants`, `place`,
`content.text`, `content.ref`, `content.version`, `content.hash`. A writer
refuses any other path and a validator rejects a file listing one. The set is
closed for the reason DKF's is: none of these is mirrored in the
[index](#indexyaml), and sealed index segments never change, so a redaction
must never change an entry. `id`, `kind`, `occurred`, `container`, `ordinal`,
`standpoint` and `timestamp` cannot be redacted. That costs something, since
the fact that one person addressed another at a given time can itself be what
someone wants forgotten, and it is left to a later version that can mask index
entries.

**Redacting `content.text` withdraws an inline episode.** It carries no record,
so it is out of recall and makes every claim citing it unverifiable. Redacting
`content.ref` leaves a reference episode as a bare tombstone: it says that
something of this kind happened at this time from this standpoint, and no
longer where.

**It is irreversible and never implicit.** The block is never removed and a
redacted field is never restored. A file carries at most one `redacted` block;
redacting again replaces its `timestamp`, `reason` and `source` and makes
`fields` the union. Nothing redacts as a side effect: not a source being
deleted, not a claim being retracted or redacted.

**Redaction does not cascade, in either direction.** Redacting an episode
changes no claim; the claims citing it become unverifiable and are reported, in
DKF's terms, so a person can decide whether to redact them too. An
implementation MAY offer "redact this episode and the claims citing it" as one
action, provided it writes a separate `redacted` block on each object it
changes. Redacting a claim changes no episode.

**What redaction does not remove.** As in DKF, it removes text from the
current file and from what a conformant implementation reads, recalls, serves
and embeds. It does not remove it from version control, clones or earlier
fetches. That caveat is sharper here than in DKF, because inline episodes are
whole conversations: in a git workspace the text of every redacted turn stays
in history, and an implementation whose store is a git repository MUST say so
when it redacts. Erasure from history is a property of the store, not of the
file.

---

## Object Model

```
  mailbox · calendar · storage           harness conversations, notes
              ▲                                       │
              │ content.ref (trace)                   │ content.text (inline)
              │                                       ▼
          EPISODE ◀──── container ──── EPISODE (turn, message, attachment)
              ▲   │
              │   └── occasion ──▶ intentions object (id, version)
              │
   DKF claim: source.document.ref = epi_…, quote = the words relied on
```

### How the other formats cite an episode

A DKF claim cites an episode through `source.document`:

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

intentions does not cite episodes. An episode names the intention it was the
occasion of, by `occasion`, an outbound reference from the episode, so no
intentions file changes when an episode is recorded.

### When an episode is recorded

The format says what an episode is, not when one must exist. Two practices are
expected, and both are implementation choices:

- **Inline content is recorded as it happens.** A conversation has no other
  home, so a harness that wants to cite it later records every turn when it is
  spoken.
- **Referenced content is recorded on demand.** Most mail is not worth a
  record. An implementation can record a reference episode at the moment
  something durable first cites the thing it points at, such as a claim, an
  intention or an explicit request to keep it, and write the episode and the
  citing object together so that neither exists without the other.

Whether an episode that nothing cites any longer is kept or dropped is likewise
the implementation's decision.

---

## File Layout

```
/episodes.yaml                 workspace marker and configuration
/episodes/
  2026-11/
    epi_01a1b4b1-8a20-7d43-b6e1-0c9f5a7d3e12.yaml
    epi_01a1b4b2-3c1d-7e5a-9f02-6b8c4d2e1a37.yaml
  legacy/                      only if ids exist from which no month derives
/index.yaml                    derived cache: the open months
/index/
  2026-11.yaml                 sealed segments, one per earlier month
```

The layout follows DKF's [sharding](https://github.com/nodelogicau/particulars#sharding):
a file's path is derived from its id alone, the month being the UTC month of
the id's minting instant, and a month is sealed once an id two or more months
later exists. A file in a sealed month may change only by having its
`source_status` rewritten or gaining a `redacted` block.

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

The index is a cache of the files, never the reverse. Each entry mirrors
exactly `id`, `kind`, `occurred`, `container`, `ordinal`, `standpoint` and
`timestamp`, which is what recall by time, by conversation and by speaker needs,
and is also exactly the set redaction cannot touch. Nothing in `content`,
`label`, `participants`, `place`, `occasion` or `source_status` enters the
index, so each of them stays redactable or rewritable without changing a sealed
segment.

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

**Compose by reference.** Episodes depend on no DKF or intentions object to
exist or validate, and are cited by them through fields those formats already
have.

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
- **A provenance spine.** `source`, ids and timestamps are copied by agreement
  from DKF and intentions. *Forgetting* asks whether that shared shape should
  be its own specification; a third format sharpens the question.

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
themselves from what they observe themselves doing, behind `occasion` and the
closing of the loop with intentions.

**Ecosystem.**
[particulars](https://github.com/nodelogicau/particulars), semantic memory,
which cites episodes ·
[intentions](https://github.com/nodelogicau/intentions), prospective memory,
which episodes name as their occasion ·
[Forgetting](https://forgetting.fyi), the argument the family shares, which
identified this gap.

---

## License

The specification is released under [CC0 1.0 Universal](LICENSE). Reference
implementations are released under the MIT License.
