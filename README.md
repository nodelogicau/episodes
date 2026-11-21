# Episodes Format

An open format for episodic memory: what happened, when and where, from whose
standpoint, and where the record of it lives. Designed to be written by
harnesses and connectors, reviewed by people through git, and cited by the
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

Where this format has a writer sort strings, as it does for `participants`
and `links`, the writer compares them by Unicode code point, as written, and
a string that is a prefix of another comes first. That is the order of the
strings' UTF-8 bytes. It is not the order of their UTF-16 code units, which
is what Java and JavaScript compare by default: the two differ for characters
above U+FFFF.

### Source and timestamp

Every episode carries a `source` block and a `timestamp`. (Informative: this is
the same shape DKF and intentions use, so one harness can write all three.)

```yaml
source:
  author: https://github.com/benfortuna   # on whose behalf this was recorded
  harness: claude                          # optional: the software that recorded it
  model: claude-opus-5-5                   # optional: only when a model took part
timestamp: 2026-11-07T06:09:18Z            # recording time, RFC 3339 UTC
```

`source` says who **recorded** the episode. It MUST contain at least one of
`author` or `harness`; a harness recording a conversation on its own is a valid
source. `author` is a **reference**: the person or agent on whose behalf the
episode was recorded.

`harness` names the software that recorded the episode, whether an AI harness
or a connector such as `gmail-sync`. `model` is present only when a model took
part in recording the episode, and a writer MUST NOT write it otherwise: a
harness that records a calendar event by parsing it, with no model call,
writes `harness` and no `model`. (Informative: a connector is a writer that
parses a source, such as a mailbox or a calendar, deterministically. Recording
a reference episode needs no model: a job that reads a message's headers and
writes an episode from them is a conformant writer.)

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
precision. `occurred` is the exception: it keeps the local offset and zone of
the happening, below.

### `EPISODE`

```yaml
# episodes/2026-11/epi_01a1b4b2-3c1d-7e5a-9f02-6b8c4d2e1a37.yaml
id: epi_01a1b4b2-3c1d-7e5a-9f02-6b8c4d2e1a37
type: episode
kind: message
occurred:
  start: "2026-11-07T14:24:00+11:00[Australia/Melbourne]"
  basis: recorded
standpoint: https://github.com/benfortuna
participants:
  - https://claude.ai
  - https://github.com/benfortuna
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
| `participants` | no | References to those present or addressed. May include the standpoint. Writers sort them by the comparison in [Field order](#field-order) and write each value once. Values are compared as written: a writer MUST NOT normalise a reference in order to compare or remove it, so `https://example.com/a` and `https://example.com/a/` are both kept. A reader MUST accept any order and repeated values; a validator MAY warn on either, and MUST NOT reject an episode for it. |
| `place` | no | A reference to where it happened. |
| `label` | no | A short human-readable name for the episode, such as an email's subject or an event's title, captured when it is recorded. Not a summary. |
| `container` | no | The episode this one is part of: a conversation for its turns, a thread for its messages, an email for its attachments. |
| `ordinal` | no | Position within `container`, an integer from 1. Required when `container` is present and order is meaningful. How a writer chooses one, and how readers order by it, is under [Containment](#containment). |
| `links` | no | Typed links to earlier episodes or to outside resources, below. |
| `content` | yes | Where the record of it lives, below. A container with no content of its own carries `content: {mode: none}`, and a self-attested act `content: {mode: attested}`. |
| `source` | yes | Who recorded it. |
| `timestamp` | yes | When it was recorded. |
| `source_status` | no | Whether referenced content can still be reached, below. |
| `redacted` | no | A redaction block, below. |

#### `occurred`

```yaml
occurred:
  start: "2026-11-07T14:24:00+11:00[Australia/Melbourne]"
  end: "2026-11-07T15:10:00+11:00[Australia/Melbourne]"    # optional
  basis: stated                  # recorded | stated | inferred
```

A date-time in `start` or `end` is an
[RFC 9557](https://www.rfc-editor.org/rfc/rfc9557) value: an RFC 3339
`date-time` with its local offset (or `Z`), followed by a suffix naming an
[IANA time zone](https://www.iana.org/time-zones) in brackets. The offset and
the zone say different things, and both are needed. An offset is a fact about
one instant: it fixes when the episode happened, including in the hour that
happens twice when daylight saving ends, where in Melbourne on 2026-04-05
`02:30+11:00` and `02:30+10:00` are an hour apart. A zone is a fact about a
place: a claim that resolves "tomorrow at 2" against an episode must compute
the offset at the instant referred to, which may lie across a daylight-saving
transition from the instant of utterance, and only a zone allows that.

- **The offset is required and governs.** The instant is the one the offset
  fixes. When the offset disagrees with the zone's rules at that local time, a
  validator warns, naming the episode, and readers still take the instant from
  the offset.
- **The zone is written whenever it is known, and never guessed.** A source
  that gives only an offset, as a mail `Date` header does, is recorded with the
  offset alone: `"2026-11-07T14:24:00+11:00"`.
  - **The zone of a `recorded` time is the zone in which the recording was
    made.** A writer takes it from the first of these that it has: the value
    it is given, when that carries a zone; the device at which the person
    took part, as that device reports its zone at the time; and
    `defaults.zone` in [`episodes.yaml`](#episodesyaml). A writer with none
    of these writes the offset alone. Where the person lives, or says they
    are, is not a source: it says nothing about where this turn was typed.
  - **A zone that contradicts the offset is left out.** A writer MUST NOT
    write a zone whose offset under the zone's rules at that instant differs
    from the offset it writes; it writes the offset alone, whichever source
    the zone came from. A zone with a critical flag is never dropped this
    way: where it disagrees, the value is refused (see *No other suffixes*,
    below). A zone with no flag that the writer has no rules for cannot be
    checked, and is left out. The offset still fixes the
    instant, so nothing about when is lost.
  - **A value in `Z` has no local offset,** so there is nothing to check
    `defaults.zone` against, and a writer MUST NOT apply it to such a value.
    A zone from the device is different, since the device reports where it
    is: a writer SHOULD write the local time, with the offset that zone gives
    at that instant, and the zone.
  - **`defaults.zone` is never applied to a `stated` or `inferred` time,** or
    to a date alone. Those take their zone from the source or the evidence,
    or go without.
- **No other suffixes.** Writers MUST NOT write RFC 9557's critical flag (`!`)
  or any suffix but the zone. Readers MUST ignore an elective suffix they do
  not implement, such as `[u-ca=gregory]`, and MUST treat as invalid an episode
  with a critical suffix they cannot honour. A writer given a value that
  carries a suffix it may not write does one of three things:
  - **An elective suffix other than the zone** is dropped, and the rest of
    the value is recorded. Given
    `2026-11-07T14:24:00+11:00[Australia/Melbourne][u-ca=gregory]`, a writer
    records `"2026-11-07T14:24:00+11:00[Australia/Melbourne]"`.
  - **A critical suffix other than the zone,** such as `[!u-ca=hebrew]`, is
    refused. The writer MUST NOT record the value, because the source has
    said it cannot be read correctly without the suffix.
  - **A critical flag on the zone,** as in `[!Australia/Melbourne]`, is
    honoured by checking the offset against the zone's rules at that local
    time. When they agree, the writer records the value without the flag.
    When they disagree, or the writer does not know the zone, it MUST refuse
    the value.
- **A date alone is valid** when the time is unknown: `"2026-11-03"`. RFC 9557
  gives a date no suffix, so a date alone MAY be accompanied by `tz`, an IANA
  zone name, saying where the date is reckoned. `tz` MUST NOT appear beside a
  date-time, whose zone is its suffix. `start` and `end` take the same form,
  both dates or both date-times.
- **Values are quoted.** Writers MUST write `start` and `end` as double-quoted
  YAML strings, in episode files and in the index. `[` and `]` are flow
  indicators in YAML, and some parsers turn an unquoted date-time into a
  timestamp type that loses the zone.

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
its first turn, by leaving `end` out. A date-time is compared as the instant
its offset fixes. A date alone is compared as a date with the recording
instant's date, reckoned in `tz` where `tz` is present, and otherwise in UTC
allowing one day, since the date's own zone is unknown.

**A stated time may be up to five minutes ahead.** Where `basis` is `stated`,
a date-time in `start` or `end` may be up to five minutes later than
`timestamp`. A writer MAY record such an episode, and records the time as the
source stated it, not moved back to `timestamp`. A source's clock and the
writer's can disagree, as when a mail server's clock runs thirty seconds
ahead, and the writer cannot correct a time a source stated: a time it moved
would be one no source gave, under a basis that says a source gave it. The
allowance does not apply to a `recorded` or `inferred` time, which comes from
the writer's own clock or reasoning, the same clock that supplies `timestamp`.
It does not add to the allowance for a date alone.

A validator warns, naming the episode, when either bound is violated by more
than the allowance that applies: none for a `recorded` or `inferred`
date-time, five minutes for a `stated` one, and one day for a date alone with
no `tz`. It warns rather than fails because it cannot tell a writer's mistake
from clocks that disagree, the writer's or a source's, in the same way it
warns on an id from later than now (see [Sharding](#sharding)).

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

A container with nothing of its own, one with `content: {mode: none}`, is its
keeper's: its `standpoint` is the person or agent whose record the container
is. That is the person for a conversation with a harness, and the mailbox
owner for a mail thread. It says nothing about who spoke or acted within the
container: each child states its own `standpoint`, and a reader that finds a
conversation under a person's standpoint does not conclude that the person
spoke every turn in it. A container with content of its own keeps the
standpoint its content gives it: an email that contains its attachments is
its sender's, as any email is.

#### `content`

Content has four modes, each an answer to where the record of the happening
lives: `inline`, it is here; `ref`, it is elsewhere; `none`, the episode has
no record of its own because its children do; `attested`, the record is the
standpoint's own word.

**Inline** is for content this workspace is the origin of: a conversation turn,
a typed note, a transcript the harness made itself. The episode is the only
copy, so it holds the text.

```yaml
content:
  mode: inline
  media_type: text/markdown
  derivation: verbatim     # verbatim | transcribed | ocr | rendered
  language: en-AU          # optional: only when known
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
  uid: mid:CAF3x9q@mail.example.com # optional: the content's own identifier
  version: "18f2c3a9b4d5e6f7"       # optional: the source's own version id
  hash: sha256:9f2a…                # optional: of the representation media_type names
  media_type: message/rfc822        # optional; required with uid
  language: en                      # optional: as the source stated it
```

`ref` is a URI or an identifier meaningful to whatever can fetch it, and
MUST NOT be an episode id: what a reference episode points at lives outside the
workspace, and a relation between episodes is a [link](#links). `version`
is the source's own notion of a version where it has one: a calendar event's
sequence or ETag, a file's revision id. `hash` is what lets a later reader tell
that what the pointer now returns is not what was recorded.

**`uid` is what the content is; `ref` is where to fetch it.** A provider id
names one copy in one account: it stops resolving when a mailbox moves, and
two connectors recording one email give it two refs. `uid` is the identifier
the content's own format assigns, which survives both. A writer records it
whenever the source exposes one, and MUST write it as follows:

- **Mail:** the `Message-ID` header
  ([RFC 5322](https://www.rfc-editor.org/rfc/rfc5322)) as a `mid:` URI
  ([RFC 2392](https://www.rfc-editor.org/rfc/rfc2392)), with the angle brackets
  removed and the value percent-encoded as RFC 2392 requires:
  `Message-ID: <CAF3x9q@mail.example.com>` is `uid: mid:CAF3x9q@mail.example.com`.
- **iCalendar:** the `UID` property
  ([RFC 5545](https://www.rfc-editor.org/rfc/rfc5545)), verbatim. A `UID` is
  often not a URI (`7q2m4k9d0s1a@google.com`), and no URI scheme exists for it.
- **Any other format** that assigns its content an identifier: that identifier,
  as a URI where the format defines a URI form, and verbatim otherwise.

`media_type` is required when `uid` is present, because it says which format's
identifier `uid` is. A file or a web page has no identifier of its own format,
and is recorded without `uid`; its `hash` is what says whether two copies are
the same. `uid` never replaces `ref` as a locator, and `ref` is never taken as
an identity. An inline episode MUST NOT carry `uid`: its identity is its
episode id.

`uid` is identity, not proof of it. A broken mailer can reuse a `Message-ID`,
and every instance of a recurring event shares its series' `UID`, including an
instance arranged on its own, which iCalendar tells apart only by
`RECURRENCE-ID`. So episodes sharing a `uid` are possibly, never certainly, of
one thing. A validator MAY report reference episodes that share `standpoint`,
`media_type` and `uid` as possible duplicates, and MUST NOT reject them: both
recordings are valid, and episodes are never revised to merge them. Episodes
from different standpoints that share a `uid` are not duplicates; they are two
people's records of one message.

**A writer avoids a second recording of the same content.** A writer that can
see the workspace SHOULD NOT record a reference episode whose `standpoint`,
`media_type` and `uid` all equal those of an existing reference episode,
unless it is told explicitly that the content is a distinct thing, as an
instance of a recurring event is. The writer does not judge that for itself:
its caller says so. A writer that declines SHOULD name the existing episode,
so that whatever asked can cite it. This is a SHOULD and not a MUST because
`uid` is not in the index, so finding a match means reading episode files,
and because two machines cannot see each other's writes. A second such
episode stays valid.

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
occurred: {start: "2026-11-07T16:02:00+11:00[Australia/Melbourne]", basis: stated}
label: Budget review with Jane
content:
  mode: ref
  ref: gcal:evt_7q2m4k9d0s1a
  uid: 7q2m4k9d0s1a@google.com
  version: "3"
  media_type: text/calendar
```

A calendar is a record of what was arranged, not of what took place. A
meeting that was arranged and never held leaves the same calendar event as one
that was held, so an episode of the calendar is not evidence that the meeting
happened. That needs a record of the meeting itself: a turn, a note, a
transcript, attendance from the system that hosted it. Read this way, a
calendar episode is true when it is recorded and can be recorded at any time
after the arranging, including before the meeting.

`hash` is written `<algorithm>:<digest>`. It is taken over the representation
that `media_type` names:

- **`message/rfc822`:** the complete raw message, headers and body, as the
  mailbox stores it.
- **`text/calendar`:** the iCalendar object that holds the event, as the
  calendar store returns it.
- **Any other media type:** the bytes of the content in that representation.
- **No `media_type`:** the bytes that `ref` returns. A writer SHOULD write
  `media_type` whenever it writes `hash`.

**A writer without those bytes writes no `hash`.** A writer that holds only a
provider's own rendering of the content, such as an API's JSON for a message,
MUST NOT write a hash of it. It leaves `hash` out, and records `version`
where the source has one. A hash exists to be compared with a later fetch,
and a hash of other bytes would make every reader that checks it see a change
that never happened.

**A hash identifies one stored copy.** It is of the copy the episode's `ref`
points at. Copies of one message held by different people differ, because
each mailbox adds its own `Received` headers on delivery, so their hashes
differ too. A reader MUST NOT conclude from differing hashes that episodes
with different standpoints record different content: across copies, the
identity is `uid`.

The bytes are hashed with CRLF sequences normalised to LF and *nothing else*
altered: not trailing whitespace, not Unicode normalisation form, not a final
newline. Line endings are an artefact of transport and differ by platform;
everything else differs because someone changed the content, and the check
must see it. Writers MUST write `sha256`. Readers MUST accept any
`<algorithm>:<digest>` and MUST report an algorithm they do not implement as
unverified, never as invalid. (Informative: this is DKF's rule, so a DKF claim
and the episode it cites can carry the same hash.)

A reference episode MUST NOT carry `text`. That is the format's rule against
ingestion: an episode about an email is a trace of the email, not a copy of it,
and a mailbox remains the system of record for mail. Whatever cites the episode
carries the words it relies on as its own quote, so it stays verifiable without
the episode store holding the message. (Informative: in DKF that quote is
`source.document.quote`.)

**None** is a container with nothing of its own, such as a conversation whose
turns are its children, and means only that (see
[Containment](#containment)). Writers SHOULD write a container together with
its first child, so that a container is not seen without one.

**Attested** is a [self-attested act](#self-attested-acts): the record is the
standpoint's own attestation that they did it. Its `content` is exactly
`{mode: attested}`, with no other key.

Content with `mode: none` or `mode: attested` MUST NOT carry `language`.

**`language` is the language of the content as recorded,** on an inline or a
reference episode. It is one language tag, well-formed under
[BCP 47](https://www.rfc-editor.org/info/bcp47): `en-AU`, `ja`, `zh-Hant-TW`.

- **Known, never guessed.** A writer records `language` only when the source
  states it, as mail's `Content-Language` header
  ([RFC 3282](https://www.rfc-editor.org/rfc/rfc3282)), iCalendar's
  `LANGUAGE` parameter or HTML's `lang` do, or when the harness produced the
  text in a language it set: a recogniser told which language to expect, or
  text rendered in a known language. A writer MUST NOT record a language that
  language detection chose. A detected language is a judgement, and anything
  that needs one can detect it from the text when it reads it. An interface's
  locale is not the language of what was typed in it.
- **On a reference episode,** `language` is the language the source stated
  when the episode was recorded, captured as `label` is, and is not rewritten
  if the source later says otherwise. It does not require `media_type`.
- **On a transcript,** `language` is the language of the episode's own
  `text`, not of the audio or image it was made from. The audio's language
  belongs on the audio's own episode, which the transcript names as `via`. A
  language the recogniser detected for itself is not recorded.
- **One tag.** Content in more than one language is `mul`. A writer whose
  source gives a list records its main language, or `mul` if none is. `und`
  (undetermined) MUST NOT be written: a language that is not known is left
  out.
- **Case.** Writers MUST use the case
  [RFC 5646 §2.1.1](https://www.rfc-editor.org/rfc/rfc5646#section-2.1.1)
  recommends; readers MUST compare tags without regard to case. A validator
  rejects a tag that is not well-formed, and MAY warn on, but MUST NOT reject,
  a subtag missing from the
  [IANA Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/).
  Well-formed means that the tag matches the grammar of
  [RFC 5646 §2.1](https://www.rfc-editor.org/rfc/rfc5646#section-2.1), which
  is checked without the registry. `en_AU` is not well-formed, and is
  rejected. `english` is well-formed, as a primary language subtag of seven
  letters, though it names no language: it is valid, and a validator MAY warn
  on it.

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

**A container with nothing of its own carries `content: {mode: none}`.** It
is valid whatever its `standpoint`, and whether or not any episode names it
as `container`. A validator warns, naming the episode, on one that no episode
in the workspace names as `container`, and MUST NOT reject it. A container is
not meant to stay empty, but a crash or a partial copy can leave one so, and
the remedy is to write a child, which changes no existing file.

**A container is recorded before its children.** A writer MUST record a
container before any episode that names it as `container`. A validator warns,
naming the child, when the child's id and its container's id are both UUIDv7
and the container's sorts later, and makes no check when either id is not a
UUIDv7. It warns rather than fails because clocks on two machines can
disagree.

**A `container` that does not resolve is reported, not invalid.** A
`container` whose episode id does not resolve in the workspace, because the
container was dropped or never copied, is reported as unresolved and does not
make the episode invalid, as for [links](#links). A turn is still a turn
without its conversation.

**A self-attested act may be a container.** Notes written during a logged
meeting can name the [act](#self-attested-acts) as their `container`. It is
still an act, and each child is an ordinary episode with its own standpoint
and content.

**A writer does not reuse an `ordinal`.** A writer MUST NOT write an episode
whose `container` and `ordinal` both equal those of another episode it can
see in the workspace. Two turns cannot both be seventh. A writer asked for
one refuses, naming the existing episode.

**An `ordinal` is the source's position, or the next one.** Where the source
gives its parts positions, as the pages of a document or the attachments of
an email do, a writer MUST write those positions, counted from 1: page 5 of a
scan is `ordinal: 5` whether or not pages 3 and 4 were recorded. Otherwise a
writer MUST write one more than the highest `ordinal` held by an episode in
the container, and 1 when none holds one. It is the highest and not the count
of children, which after a gap could land on an `ordinal` in use. Gaps are
valid.

**A repeated `ordinal` is reported, not invalid.** A validator warns, naming
both episodes, when two episodes share a `container` and an `ordinal`, and
MUST NOT reject either. Two branches can each record the next turn of one
conversation with the same `ordinal`, and they merge without conflict because
each turn is its own file. Episodes are never revised, so nothing could
repair the result if it were invalid.

**Children are ordered by `ordinal`, then by id.** A reader that presents the
children of a container in order MUST order them by ascending `ordinal`, and
those that share an `ordinal` by id, compared as in
[Field order](#field-order). Children with no `ordinal` follow those with
one, ordered by id. Every reader then shows the same order, including where
an `ordinal` repeats.

#### Links

`links` says how an episode, or the content it points at, relates to other
episodes or to resources outside the workspace, using [Web Linking](https://www.rfc-editor.org/rfc/rfc8288)
(RFC 8288):

```yaml
links:
  - rel: predecessor-version
    href: epi_01a1b6c0-2d14-7a3e-8b52-9e0f1c7d4a26   # the transcript this one improves on
  - rel: via
    href: epi_01a1b6a2-7e31-7c08-a4d9-5b2e8f0c3d17   # the voice memo it was made from
```

Each link has `rel` and `href`, may have `anchor`, and has no other key. `rel`
is a relation type registered in
the [IANA Link Relations registry](https://www.iana.org/assignments/link-relations/),
written in lowercase and used in its registered meaning, or an absolute URI,
which is how RFC 8288 lets anyone define a relation without a registry.
`href` is an episode id, resolved within the workspace, or a URI. Writers sort
`links` by `rel` and then by `href`, each by the comparison in
[Field order](#field-order), and write a link with no `anchor` before one with
the same `rel` and `href` that has one. A reader MUST NOT reject an episode
for a `rel` it does not know, and gives it no meaning.

**`anchor` says a link is about the referenced content.** In RFC 8288 a link
runs from a context to a target, and `anchor` names the context. A link with
no `anchor` is about the episode. A link with `anchor` is about the content
the episode refers to, and its value MUST equal the episode's `content.ref`,
character for character; a validator rejects any other value, naming the
link. So `anchor` appears only on an episode that carries `content.ref`, and
a validator rejects it on any other. No other use of `anchor` is admitted: an
episode makes no statements about resources other than itself and what it
points at. `anchor` repeats `ref`, and is removed with it, since
[redacting `content.ref`](#redaction) also redacts `links`.

Whether a relation is registered depends on which copy of the registry is
consulted, so validity does not turn on it:

- A writer MUST NOT write a `rel` that is neither registered nor an absolute
  URI. A mistyped relation is refused when it is written, which is when it
  can be fixed.
- A validator warns on, and MUST NOT reject, a `rel` that has the form RFC
  8288 gives a registered relation type (a lowercase letter followed by
  lowercase letters, digits, `.` or `-`) and is missing from its copy of the
  registry. The warning names the link.
- Only a `rel` that is neither of that form nor an absolute URI is invalid:
  `Answers`, or `my relation`.

Two registered relations have a meaning between episodes:

- **`via`** ([RFC 4287](https://www.rfc-editor.org/rfc/rfc4287)): this episode
  records something taken from the target. A transcript is `via` the episode of
  the recording it was made from; a [self-attested act](#self-attested-acts) is
  `via` the turn in which it was attested.
- **`predecessor-version`** ([RFC 5829](https://www.rfc-editor.org/rfc/rfc5829)):
  this episode supersedes the target as a rendering of the same thing, as a
  better transcript supersedes an earlier one. The earlier episode is not
  changed and stays citable.

A third has a meaning for the content a reference episode points at:

- **`memento`** ([RFC 7089](https://www.rfc-editor.org/rfc/rfc7089)): with
  `anchor`, the target is an archived snapshot of the content as it was when
  the episode was recorded. Its `href` is a URI, never an episode id. A
  `memento` link with no `anchor` is invalid, since an episode has no
  snapshot, and a validator rejects it, naming the link. An episode may carry
  more than one, as when two archives each hold a snapshot.

Together with `content.ref` and the episode's time, a `memento` link records
what the [Robust Links](https://robustlinks.mementoweb.org/) convention does
on the web: the original URL, when the link was made, and where a snapshot
of it is kept.

```yaml
# a web page, with a snapshot made when it was recorded
kind: document
links:
  - rel: memento
    href: https://web.archive.org/web/20261107031500/https://example.com/report
    anchor: https://example.com/report
content:
  mode: ref
  ref: https://example.com/report
  hash: sha256:…
  media_type: text/html
```

Any relation may be anchored, so `canonical` or `alternate` can be said of
the referenced page. The format gives a meaning to `memento` alone, and a
reader gives other anchored relations none, as for any relation it does not
know.

**Links are written once.** A writer writes `links` when it records the episode
and never adds, removes or changes one afterwards, except by redaction. A link
to an episode names one recorded before it, so nothing ever needs adding later:
the newer episode carries the relation. A link whose episode id does not
resolve, because the target was redacted, dropped or never copied, is reported
as unresolved and does not make the episode invalid.

A snapshot is therefore linked only when the episode is recorded, and a
snapshot made later is never added: it may be of a later page. The writer
links a snapshot it caused to be made while recording, or an existing one it
has compared with the content it fetched and found to be the same content.
An older snapshot of a page that has since changed is not linked.

**Archiving is explicit.** Submitting content to an archive discloses it to
the archive, and for a public archive publishes it. A writer MUST NOT cause
content to be archived unless the person on whose behalf it records has
explicitly asked for that content to be archived, and recording an episode is
not such a request. Linking a snapshot that already exists submits nothing.
No validator can check this, so it is a rule for writers.

**Links do not restate containment.** `container` and `ordinal` are the
format's containment, mirrored in the index, and a writer MUST NOT also write
it as a link. A validator warns, naming the episode, on an `up` or `collection`
link whose target is the episode's own `container`.

**Links record provenance, not judgement.** A link says what was known when
the episode was recorded: where its record came from, what it supersedes.
That an episode fulfilled a plan, or contradicts another, is a judgement, and
belongs outside the format. No relation this specification defines targets an
object of another format. (Informative: in the family, such a judgement is a
DKF claim citing the episodes.)

Links are never mirrored in the [index](#indexyaml), so `links` can be
redacted.

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
  start: "2026-11-08T09:00:00+11:00[Australia/Melbourne]"
  end: "2026-11-08T10:30:00+11:00[Australia/Melbourne]"
  basis: stated
standpoint: https://github.com/benfortuna
label: Deep work on the budget draft
links:
  - rel: via
    href: epi_01a1b874-e130-7b2c-9d41-3f6a8e0c5b27   # the turn: "log ninety minutes of deep work from nine"
content:
  mode: attested
source:
  author: https://github.com/benfortuna
  harness: claude
timestamp: 2026-11-08T00:00:41Z
```

Its `content` is exactly `{mode: attested}`, with no other key: the act
itself left no record, and what stands for one is the person's word.

**It names its attestation whenever the writer recorded one.** When an act is
attested in an episode the writer records, which includes every attestation
made in a conversation the writer is recording, the writer MUST record that
episode and MUST link the act to it with a [`via` link](#links). A writer
MUST NOT omit the link by leaving the attesting episode unrecorded. When
nothing the writer records holds the attestation, as when the person presses
a control whose only purpose is to log the act, the act has no `via` link.
The rule does not depend on `source.harness`: a "log my run" button is a
dedicated control whether a harness or a connector implements it. No
validator can check this in general, so it is a rule for writers.

**It is self-attestation only.** A self-attested act's `standpoint` MUST equal
its `source.author`. When it links `via` an episode that resolves in the
workspace, that episode's `standpoint` MUST equal the act's. A `via` link that
does not resolve, because its episode was redacted, dropped or never copied, is
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

**It is recognised by its mode, not by `kind` or by shape.** A validator
treats as a self-attested act every episode with `content.mode: attested`,
and no other, and applies the rules above to it whatever its `kind` and
whether or not any episode names it as its `container`. `activity` is the
recommended `kind` and stays descriptive.

An earlier draft gave an act `content: {mode: none}` and recognised it by
having no children. An act written that way now reads as a container with no
children: it is valid, a validator warns on it, and the rules of this section
no longer apply to it. Episodes are not rewritten, so no conversion is
defined.

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
| `gone` | Confirmed deleted at the source: not found by `ref`, nor by `uid` where the episode has one. |

A reader whose `ref` no longer resolves MAY search the source by `uid`, as
after a move to a new mailbox. Content found that way is `available`, or
`changed` if its hash or version differs, and is never `gone`. The episode's
`ref` is not rewritten, since episodes are not revised; an implementation may
keep its own map from `uid` to the new location, outside the format.

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

**A snapshot is a fallback, not a copy.** A reader that cannot fetch the
content as recorded, because the source is `changed`, `unreachable` or
`gone`, MAY fetch the `href` of a [`memento` link](#links) in its place, and
presents what it fetched as an archive's copy, not as the source.
`source_status` is unchanged by that, because it describes the source: a
`gone` page with a snapshot is still `gone`. The rule against back-filling
holds here too, and a writer MUST NOT copy a snapshot's content into the
episode. The workspace keeps a second pointer, and no content.

**A snapshot is not proof.** An archive may serve a page with changes of its
own, such as rewritten links or a banner, so a snapshot need not match
`content.hash`. A reader MAY compare them. It reports a snapshot that does not
match as unverified, and does not treat the episode as invalid or the source
as `changed` on that account, since the snapshot is not the source.

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

**`fields` lists only what was removed.** A path in `fields` records that the
episode carried the field and that it was removed. A writer asked to redact a
path the episode does not carry MUST refuse the whole request, naming the
path, unless the block already lists it, in which case the request changes
nothing for that path. A request for a field that is not there is most likely
a mistake about which episode or which field, and a path listed for a field
that never existed would say something false in a block that is never
removed. Once a field is gone, a file that had it and a file that never did
look the same, so no validator can check this; it is a rule for writers.

**What can be redacted is a closed set:** `label`, `participants`, `place`,
`links`, `content.text`, `content.ref`, `content.uid`, `content.version`,
`content.hash`, `content.language`.
`links` is redacted whole, never one link at a time. A writer
refuses any other path and a validator rejects a file listing one. The set is
closed because none of these is mirrored in the [index](#indexyaml), and sealed index segments never change, so a redaction
must never change an entry. `id`, `kind`, `occurred`, `container`, `ordinal`,
`standpoint` and `timestamp` cannot be redacted. That costs something, since
the fact that one person addressed another at a given time can itself be what
someone wants forgotten, and it is left to a later version that can mask index
entries.

**Redacting `content.ref` redacts everything that locates or identifies the
content.** A `redacted` block that lists `content.ref` MUST also list each of
`content.uid`, `content.version`, `content.hash` and `links` that the episode
carries, and each is absent from the file. A writer asked to redact
`content.ref` redacts them in the same act. A validator rejects a file whose
block lists `content.ref` while any of the four is present, naming the field.
Each of them can lead back to the content:

- **`content.uid`** is how the content is found again when `ref` stops
  resolving.
- **`content.version`** is the source's own id for a version, and is often
  the id that `ref` carries.
- **`content.hash`** lets anyone holding a candidate confirm that it is the
  content.
- **`links`** can hold the location as an `href`, as a link to an archived
  copy does, and is redacted whole.

Each of the four stays redactable on its own, without `content.ref`. The cost
of the rule is a link that disclosed nothing, lost now and then.

An episode whose `content.ref` was redacted under an earlier draft, and which
still carries one of the four, is repaired by redacting the fields left
behind: redacting again adds them to the block.

**Redacting `content.text` withdraws an inline episode.** It carries no record,
so it is out of recall, and anything that quotes it can no longer be checked
against it. Out of recall means that a reader MUST NOT return the episode as
content in answer to recall: a search for what was said does not find it. A
reader MAY show that the episode exists and where it stands in its container,
as a placeholder at its position in a thread, using only the fields that
cannot be redacted (`id`, `kind`, `occurred`, `container`, `ordinal`,
`standpoint` and `timestamp`). These are in the index already, so showing them
discloses nothing new, and leaving the position out would make the next turn
read as a reply to the wrong one. A reader MUST NOT show anything that was
redacted, from any copy it holds, and leaves out a `label` that was kept,
since a later redaction could remove it.

**Redacting `content.ref` leaves a reference episode as a tombstone.** It says
that something of this kind happened at this time from this standpoint, and
no longer where. The episode keeps its `id`, `kind`, `occurred`,
`standpoint`, `container`, `ordinal` and `timestamp`, its `content.mode` and
`content.media_type`, and whichever of `label`, `participants`, `place` and
`content.language` were not redacted as well. Those four are redacted only
when the person lists them: a `label` can say where a document is, and
whether it does is theirs to judge.

**It is irreversible and never implicit.** The block is never removed and a
redacted field is never restored. A file carries at most one `redacted` block;
redacting again replaces its `timestamp`, `reason` and `source` and makes
`fields` the union of old and new. Nothing redacts as a side effect: not a
source being deleted, not anything that cites the episode being withdrawn or
redacted. The fields that go with `content.ref` are not a side effect either.
They are one redaction with a defined extent, and every field it removes is
named in `fields`.

**Redaction does not cascade.** Redacting an episode changes no other episode,
not its container and not its children, and no object outside the workspace.
(Informative: in a DKF workspace, claims citing a redacted episode become
unverifiable and are reported, so a person can decide whether to redact them
too. An implementation of both formats may offer "redact this episode and the
claims citing it" as one action, provided it writes a separate `redacted`
block on each object it changes. Redacting a claim changes no episode.)

**What redaction does not remove.** It removes text from the current file and
from what a conformant implementation reads, recalls, serves and embeds.

That reaches every value derived from a redacted field, because a derived
value can disclose what it was computed from. An implementation that keeps
values derived from an episode's fields MUST, when a field is redacted,
delete each value derived from it or compute the value again without it.
Derived values include embeddings, classifier and other model outputs,
summaries and extractions, and search indexes. ([Recall by
query](#recall-by-query) says where such caches are kept and how a query
uses them.) A value is derived from a
field when computing it again without that field could change it: a summary
computed from `label` and `content.text` is derived from both, and a count of
an episode's children is derived from no redactable field and is kept.

An implementation MUST NOT read, return, rank by or otherwise use a value
derived from a field that the episode's file lists as redacted, whether or
not the value has been deleted yet. It decides this from the episode file,
not from the state of its own stores. A redaction made on one machine reaches
another as a changed file, before that machine's stores are updated, and in
that interval a query must not return an episode on the strength of an
embedding of its redacted label.

(Informative: a judgement written as an object of another format, such as a
DKF claim citing the episode, is not a derived value under these rules. It is
a record with its own author and its own redaction, governed by that format,
which is why redaction does not cascade.)

Redaction does not remove the text from version control, clones or earlier
fetches. Inline
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
           ▲    ▲
           │    └─────── links ─────── EPISODE (transcript, self-attested act)
           │
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

Recording is the first of three steps, and the only one that belongs to this
format:

- **Recording** writes an episode from a source. It is parsing, and needs no
  model.
- **Selection** decides which episodes merit interpretation.
- **Consolidation** turns the selected episodes into another format's
  objects, such as DKF claims.

A message does not have to pass through a model to become an episode, and an
implementation that records episodes and does nothing else with them conforms.

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
to re-mint the branch's episodes before merging. A rebuild of the index MUST
NOT rewrite a segment that exists. It fails as validation does, naming each
file with no entry in the segment and each entry with no file, since `count`
can be wrong either way, and leaves the segment as it was. A rebuild that
absorbed the late files would make re-minting optional, and every cached copy
of the segment wrong with nothing reported.

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
  zone: Australia/Melbourne
```

`format` and `workspace.id` are required. A reader MUST refuse a workspace
whose `format` it does not implement, naming the version, rather than read
what it can. Unknown keys are ignored.

`defaults.zone` is optional and holds one IANA time zone name. Like every
default it is read by writers only: it is the last source a writer consults
for the zone of a `recorded` time, and is written only where it agrees with
the offset (see [`occurred`](#occurred)).

### `index.yaml`

The index is a cache of the files, never the reverse. The episode files are
the source of truth; in a workspace with no late merge (see
[Sharding](#sharding)) the index MUST be fully reconstructible from them, and a
consumer MUST NOT return wrong results because the index is missing or stale
(it may be slower). A rebuild writes the root and any segment that is missing
altogether, and rewrites no segment that exists; a late merge is repaired by
re-minting, not by rebuilding. Two branches that each add an episode both touch
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
    occurred: {start: "2026-11-07T14:24:00+11:00[Australia/Melbourne]", basis: recorded}
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
A sealed month with no files has no segment and no entry in `segments`, and a
validator does not report one as missing. A segment with nothing in it would
carry nothing, and would make the index depend on how many months passed
between two episodes, so that two indexes of the same files could differ.

Each entry mirrors exactly `id`, `kind`, `occurred`, `container`, `ordinal`,
`standpoint` and `timestamp`, which is what recall by time, by conversation and
by speaker needs, and is also exactly the set redaction cannot touch. Recall
by participant and [by query](#recall-by-query) read the episode files as
well. Nothing
in `content`, `label`, `participants`, `place`, `links` or `source_status`
enters the index, so each of them stays redactable or rewritable without
changing a sealed segment.

### Recall by query

An implementation need not answer free-text queries: one that reads, writes
and validates episodes conforms without doing so. An implementation that
does answer them follows the rules in this section. (Informative: they are
restated from DKF's
[*Recall by query*](https://github.com/nodelogicau/particulars#recall-by-query),
adapted to episodes, so that a fix to one copy shows as a difference to check
in the other.)

**A query resolves to episodes.** Each result is one episode. An episode is
never returned because another matched, so a container is a result only when
its own text matched or a stage proposed it, and not because one of its
children did. Every result carries `container`, from the index, so a reader
that wants results grouped by conversation can group them with no file
opened.

**The baseline.** Every implementation that answers a query resolves it
without a model, as follows, on every query:

- Whitespace, by the Unicode `White_Space` property, is trimmed from the
  edges of the query. The query's terms are its runs of non-whitespace
  characters.
- From each term, and from the whole query, the leading and trailing
  characters of Unicode general category P (punctuation) are removed, as
  written and before folding. Interior characters are kept: `timeout?`
  becomes `timeout`, and `v1.2.3.` becomes `v1.2.3`, while `o'brien` and
  `auth/session` stay as written.
- A term that is empty after trimming is ignored. A query that is empty
  after trimming, such as `?!`, resolves nothing, and that is not an error.
- A text matches when the trimmed whole query, or any one trimmed term,
  occurs in it under Unicode case folding. Terms combine by OR, since AND
  would make `what is the session timeout` find nothing.
- The texts are an episode's `label`, and the `content.text` of an inline
  episode. The content of a reference episode is not among them: the
  workspace does not hold it, and a baseline that fetched every mail on every
  query would not be one. `participants` is not among them either: a name is
  rarely in a reference such as a `mailto:` or a profile URL, and it has a
  filter of its own, below.
- An episode also matches when a term, before or after trimming, equals its
  `content.uid` exactly, with no folding, so that `mid:…` finds its mail. A
  Message-ID can end in punctuation that is part of it, and a question in
  punctuation that is not, and trying both covers each. The match is
  equality and not substring, because identifiers are compared as written
  everywhere else in the format, and a substring would match every mail from
  one host.

The baseline applies no stemming, no stopwords and no other change to terms:
`dog's` does not find "the dog barked". It is linear in history, since it
reads every label and every inline text.

**Other stages only add.** An implementation MAY run other stages, such as a
semantic stage. A stage other than the baseline MAY add episodes and MUST
NOT remove one the baseline found. Embeddings are weak at exact identifiers,
a ticket number or a surname, and the union means that a word the workspace
holds always finds its episode.

**`resolution`.** Each result carries `resolution`, the first of these that
applies:

- `uid`, when a term equalled the episode's `content.uid`;
- `lexical`, when the baseline matched otherwise;
- `semantic`, when only another stage proposed the episode.

An episode found both by the baseline and by a semantic stage is `lexical`.
An implementation MAY also report which field, and which span of
`content.text`, matched.

**Order.** Results are ordered so that two implementations with no semantic
stage return the same episodes in the same order, and a `limit` cuts them in
the same place:

1. by `resolution`: `uid`, then `lexical`, then `semantic`;
2. within `uid` and within `lexical`, by the number of the query's distinct
   trimmed terms, compared under case folding, that matched the episode,
   most first, so `timeout Timeout timeout?` has one distinct term;
3. then by `id`, in descending order by the comparison in
   [Field order](#field-order). Ids are UUIDv7, so this is close to
   recording order, newest first.

Order within `semantic` is the implementation's own, since it depends on a
model. A `limit` is applied last, after the filters and the ordering.

**Filters run afterwards, against the files and the index.** An
implementation applies every filter after the stages, reading the index and
the episode files and not any cache, so that nothing a stage gets wrong can
put a filtered-out episode in the result. It MUST support filtering by
`occurred`, `container`, `standpoint` and `kind`, and MAY support others. Two
rules apply whatever the filters:

- A [withdrawn](#redaction) episode, an inline episode whose `content.text`
  is redacted, is not returned.
- A match on a field counts only while the episode's file carries that
  field. A stale vector of a `label` since redacted does not bring the
  episode back, though the episode is still returned if its text matched.
  This is the rule of [*What redaction does not
  remove*](#redaction), applied to recall.

**Recall by participant reads the files.** An implementation MAY filter by
participant, with a query or without one. The filter matches an episode
whose `participants`, in its file, holds the reference given, compared as
written, as a writer compares [`participants`](#episode) without normalising them:
`mailto:Alex@example.org` does not match `mailto:alex@example.org`. Knowing
that two references name one person is a judgement, outside the format.
`participants` is kept out of the index so that it can be redacted, so the
filter opens every file and is linear in history. A participants cache, below,
is the remedy.

**Derived caches.** An implementation MAY keep derived caches to serve
recall: a semantic cache of vectors, a full-text index, and a participants
cache. Each is optional, and each:

- is stored **outside the workspace directory tree**, and is never
  committed, published or served. A directory inside the tree that version
  control ignores is still one forced add or one archive away from being
  published, and a vector can disclose the text it came from. (For a hosted
  store with no directory, what matters is the second half: it is never
  committed, published or served with the workspace.)
- is not read by a validator, or by a check of a source. A workspace is
  valid, and recall correct, with no cache present.
- records, for each entry, the id of the episode and the field it was
  computed from. An entry computed from content the workspace does not hold
  records `content.ref` as its field.
- only proposes. Before an episode is returned on the strength of a cache
  entry, the implementation reads the episode's file and confirms that it
  carries the entry's field, and for a participants cache that
  `participants` still holds the reference asked for. That read was already
  needed for the filters.
- may be missing, partial or stale, which MAY lower recall or speed and MUST
  NOT cause an episode to be returned that the baseline and filters would
  not allow. A redaction made on another machine arrives as a changed file,
  with no signal to this machine's caches; deleting derived values on
  redaction is still required, and the check against the file is what holds
  in the meantime.

**A full-text index stands in for the scan only where it agrees.** An
implementation MAY answer the baseline from a full-text index instead of
scanning the files, only where the index returns exactly the episodes the
scan would, whatever it does with tokens: a query for `auth/session` still
returns what the substring match returns. Where it cannot establish that the
index is current, as after a merge, it scans.

**The semantic cache.** It records the identifier of the model that produced
its vectors, and a vector produced by a model other than the one in use is
not consulted. A vector of `label` or `content.text` never needs recomputing
under the same model, since those change only by redaction. The cache MAY
hold more than one vector for an episode, as for a turn holding a pasted
document longer than the model's input. Each vector of part of
`content.text` records the span it covers and a hash of that span. Spans are
internal to the cache: they are not a way to cite part of an episode, two
implementations need not agree on them, and a match on a span still
resolves to the episode.

**Referenced content may be embedded, only in the cache.** Finding a mail by
meaning needs its body, which the workspace does not hold. An implementation
MAY fetch the content a reference episode points at and embed it, on these
terms:

- The vector is kept only in the semantic cache. The fetched content itself
  is not kept, which is what [*Point, don't copy*](#design-principles) asks.
- The vector records the `content.hash` it was computed against, and is
  consulted only while the episode's file carries that `content.hash`. A
  vector of different bytes describes something the episode does not point
  at.
- A reference episode with no `content.hash` has nothing to tie a vector to,
  so its content is not embedded, and only its `label` is.
- Fetching to embed is a check of the source, whether or not it was meant as
  one. Where the content fetched does not match `content.hash`, the
  implementation embeds nothing, and records what it observed in
  [`source_status`](#source_status) as any check does.
- A vector of an episode whose `source_status` is `changed` or `gone` is not
  consulted, and is deleted no later than the cache's next update. The
  recorded version can no longer be fetched, so the vector could not be
  checked or rebuilt, and would be the only surviving copy of something. A
  source being deleted is not a request to forget the episode; nor is it a
  licence to keep a copy of the content.

**Remote embedding is off unless configured on the machine.** An
implementation MUST NOT send any text of an episode to an embedding service
on another host unless the machine it runs on is configured to. That
configuration lives outside the workspace, and nothing in the workspace can
turn it on: a cloned workspace must not be able to cause text to leave the
machine, and a key in `episodes.yaml` that asks for it is ignored, as unknown
keys are. Episodes carry no scope, and none is added on this account, since
a scope written at recording could never be widened or narrowed. So where
remote embedding is on, it covers every episode the configuration does not
exclude. The configuration MAY narrow it to episodes selected by
`standpoint`, `kind` or `source.harness`, which are fixed at recording, and
an implementation that offers such limits applies them from the episode's
own fields.

Content fetched for a reference episode is sent to another host only where
the machine's configuration allows that by a separate setting, off by
default. A mail body sits behind its mailbox's own access control, and
sending it elsewhere is a larger step than sending a label.

The format says what the machine's configuration must be able to say, and
not where it is kept or what it looks like.

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

Early draft. Nothing is declared. The object model above is the first
proposal; the open questions below are listed rather than closed.

[`episodes-cli` v0.2.0](https://github.com/nodelogicau/episodes-cli/releases/tag/v0.2.0)
is a reference implementation of this draft. Where the draft left a behaviour
undecided, it decided and recorded the decision in
[`SPEC-FEEDBACK.md`](https://github.com/nodelogicau/episodes-cli/blob/main/SPEC-FEEDBACK.md);
the points still open there are tracked as issues on this repository.

- **Derived renderings of referenced media.** A voice memo in storage is
  referenced, but its transcript is the harness's own work and has no other
  home. [Links](#links) answer part of this: the transcript can be its own
  inline `transcribed` episode, `via` the memo's episode, and a better one
  later names it as `predecessor-version`. Whether a transcript should instead
  be a child of the memo's episode, or a second `content` block, is still
  open.
- **Translated transcripts.** A recogniser can write text in a language other
  than the audio's, as Whisper's translate mode does. The text is then a
  translation, which no `derivation` value says, and its
  [`language`](#content) differs from the audio's episode. Whether
  `derivation` should gain a `translated` value, or a translation be recorded
  some other way, is open.
- **Citing a span of a referenced source.** A claim's quote is checked by
  appearance, which survives a re-fetch. Whether the format should also define
  a fragment syntax for `ref` (a character range, a timecode, a page) is open,
  given that offsets into a fetched rendering break when the rendering changes.
- **Index masking.** `standpoint`, `participants` and `occurred` together say
  who spoke to whom and when. Redacting that fact needs an index that can mask
  entries, which DKF has also deferred. Masking would also let `participants`
  be indexed, so that [recall by participant](#recall-by-query) need not open
  every file.
- **Size of a conversation episode.** This draft makes a conversation a
  container and each turn an episode. Whether turns should instead be grouped
  into segments by topic, or a whole session be one inline episode, is open,
  and shapes how precisely a claim can cite a conversation.
- **A provenance spine.** `source`, ids, timestamps, the content hash,
  redaction and sharding are copied by agreement from DKF and restated here in
  full, so that this format stands alone. [Recall by query](#recall-by-query)
  is one more such shape, adapted from DKF's. Copies can drift apart. *Forgetting*
  asks whether that shared shape should be its own specification; a third
  format sharpens the question, and standing alone means such a specification
  would have to be one this format restates or can do without.
- **Duplicate recordings.** Two episodes of one happening from different
  standpoints are not duplicates, and whether they are the same event is a DKF
  claim. The same recording made twice is. A writer avoids one where it can
  see it: it does not reuse an `ordinal` (see [Containment](#containment)),
  and it avoids a second reference episode with the same `standpoint`,
  `media_type` and `uid` (see [`content`](#content)). Two questions remain:
  - **How an existing duplicate is marked.** Two machines can each record one
    email and merge cleanly under different ids, and a validator can report
    the pair. A [link](#links) is where a writer that knows it is repeating
    an episode could say so, but no registered relation fits (`duplicate`
    means byte-identical representations), and episodes are never revised to
    add a link later.
  - **Content with no `uid`.** A file or a web page has only its `ref` and
    its `hash`, and neither is in the index. What a writer does about a
    second recording of one is open.
- **Uncertain and approximate dates.** `basis: inferred` with a date alone
  covers "last Tuesday", but not "some time in March", "around 2019" or "the
  week of the 9th". [EDTF](https://www.loc.gov/standards/datetime/) (ISO
  8601-2) can write uncertainty, approximation and unspecified digits; whether
  `occurred` should admit it, and what "nothing is recorded before it happens"
  then means for an approximate date, is open.
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
[RFC 2392](https://www.rfc-editor.org/rfc/rfc2392) `mid:` URIs for the
[RFC 5322](https://www.rfc-editor.org/rfc/rfc5322) `Message-ID` in
`content.uid` ·
[RFC 9557](https://www.rfc-editor.org/rfc/rfc9557) date-times with a time-zone
suffix for `occurred` ·
the [IANA time zone database](https://www.iana.org/time-zones) for its zones ·
[RFC 8288](https://www.rfc-editor.org/rfc/rfc8288) Web Linking and the
[IANA Link Relations registry](https://www.iana.org/assignments/link-relations/)
for `links`, with `via` from [RFC 4287](https://www.rfc-editor.org/rfc/rfc4287)
and `predecessor-version` from [RFC 5829](https://www.rfc-editor.org/rfc/rfc5829) ·
[RFC 7089](https://www.rfc-editor.org/rfc/rfc7089) Memento for the `memento`
relation, and the [Robust Links](https://robustlinks.mementoweb.org/)
convention for recording a snapshot beside the original URL ·
[YAML 1.2](https://yaml.org/spec/1.2.2/) as the file format ·
[FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) SHA-256 for
`content.hash` ·
[BCP 47](https://www.rfc-editor.org/info/bcp47) language tags for
`content.language`, with the
[IANA Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/) ·
[RFC 3282](https://www.rfc-editor.org/rfc/rfc3282) `Content-Language`, one
source of a stated language.

**Models.**
[iCalendar](https://www.rfc-editor.org/rfc/rfc5545), whose `VJOURNAL`
component is the oldest open format for a dated record of what happened, and
whose `UID` is a calendar event's `content.uid` and whose `LANGUAGE`
parameter can state its `content.language` ·
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
