## Context

The format says what an episode is and how a workspace is laid out. It
defines no operations. The index is described as serving "recall by time, by
conversation and by speaker", and that is all the draft says about finding
an episode.

DKF has a full section, *Recall by query*, written for claims. Six issues
asked how much of it carries over. Most does. Four things about episodes
force a difference:

```
                         DKF                     episodes
 resolves to             particulars             episodes
 text held               every claim             inline only; references
                                                 point at content elsewhere
 scope                   on every object         none
 redaction               whole content           one field at a time
```

Three other proposed changes supply rules this one leans on:
`redaction-completeness` (a derived value of a redacted field is not used),
`duplicate-recordings` (which bytes `content.hash` covers) and
`settle-edge-cases` (a withdrawn episode is not returned as content).

## Goals / Non-Goals

**Goals:**

- Two implementations with no model return the same episodes, in the same
  order, for one query over one workspace.
- A cache of any kind can cost recall or speed, and can never return
  something a redaction removed.
- Nothing derived from a person's conversations or mail enters the
  workspace, version control or another host by default.
- The format still stands alone.

**Non-Goals:**

- Requiring a query operation. An implementation that reads, writes and
  validates is conformant without one.
- A request or response syntax. The section says what is returned, and
  leaves parameter names and transport to the implementation.
- Order within `semantic`, or which model to use.
- A scope field, or any sharing feature.
- Putting `participants` in the index. That waits on index masking.
- A shared specification for the family. #43 stays open under *A provenance
  spine*.
- Citing a span of an episode. Spans in a cache are private to it.

## Decisions

### A query resolves to episodes

DKF resolves to particulars so that a query landing on a superseded claim
returns its subject, with the current synthesis first. Episodes are never
superseded, and there is nothing above an episode that plays the part of a
particular.

Resolving to containers was the alternative: return the conversation and
mark the turns that matched. Against it:

- A container can hold thousands of turns, and a result that is "this
  conversation" does not answer the question.
- Not every episode has a container, so there would be two kinds of result.
- Every result already carries `container`, in the index. A reader that
  wants to group by conversation can, with no file opened.

So a container is a result only when it matched itself, usually by `label`.

### The baseline is DKF's, on `label` and inline text

The term rules are copied without change: split on whitespace, trim
punctuation from the edges, fold case, combine by OR, substring match. They
were worked out against real questions from agents, and an implementation of
both formats should be able to share the code.

What differs is the text:

- **`label`,** on every episode that has one.
- **`content.text`,** on inline episodes.
- **Not the content of a reference episode.** The workspace does not hold
  it, and a baseline that fetched every mail on every query would not be a
  baseline.
- **Not `participants`.** A person's name is rarely in a reference such as
  `mailto:` or a profile URL, and a substring match on URLs gives poor
  results. Participants get a filter of their own.

### `content.uid` matches exactly, and has its own `resolution`

"Find `mid:…`" is a common lookup, and a Message-ID survives the mail being
moved. So a term that equals `content.uid` matches.

- **Equality, not substring.** A substring match on identifiers would return
  every mail from one host for a query that names the host.
- **No folding.** Identifiers are compared as written everywhere else in the
  format.
- **Before or after trimming.** A Message-ID can end in punctuation that is
  part of it, and a question can end in punctuation that is not. Trying both
  covers each.

It gets its own `resolution` value, `uid`, ranked first. Under `lexical` an
identifier match would count as one term matched, and could sort below a
turn that merely mentions two words of the question. The value plays the
part that `label` and `alias` play in DKF: the query named the thing.

### The order is fixed down to the id

When `limit` cuts, two implementations must cut in the same place.

- **By `resolution`,** so that anything a model proposed comes after
  everything found without one.
- **By distinct terms matched, most first.** This is where precision comes
  from, since OR refuses nothing. Terms are counted after trimming and
  folding, so a repeated word counts once.
- **By id, latest first.** Ids are UUIDv7, so this is close to recording
  order, newest first, and needs nothing parsed.

`occurred.start` descending was considered. It needs instants compared
across offsets, mixes dates with date-times, and is only as good as the
source's clock.

Order within `semantic` is left alone. It depends on the model, and two
implementations with different models cannot agree anyway.

### Filters run last, against the files

This is DKF's safety argument, restated: every filter runs after the stages
and reads the index and the files. Nothing a stage gets wrong can put a
filtered-out episode in the result.

Episodes add one check that DKF does not need. A redaction can remove
`label` and leave the episode valid and recallable. A stale vector of the
old label would then bring the episode back for exactly the query that
matches the removed text. So a match counts only while the file carries the
field it matched on. `redaction-completeness` states that rule for every
derived value. Here it is applied to recall.

### Recall by participant is a filter

`participants` is kept out of the index so that it can be redacted. The
cost is that "what did I discuss with X" opens every file. The section says
so plainly, as DKF does for its baseline, and names the cache as the remedy.

The filter compares references as written. That matches `canonical-form`,
which sorts `participants` without normalising them. Knowing that two
references name one person is DKF's work.

### One set of rules for three caches

A semantic cache, a full-text index and a participants cache differ in what
they hold and not in what can go wrong with them. One set of rules covers
all three:

- **Outside the workspace tree.** A directory inside it that is ignored by
  version control is still one `git add -f` or one archive away from being
  published. Vectors can disclose the text they came from.
- **Each entry records its episode and field.** This is what makes the
  check against the file possible.
- **A cache only proposes.** The file is read before anything is returned.
  That read was already needed for the filters.
- **Stale is safe.** A redaction made on another machine arrives through
  git, with no signal to this machine's cache. Deleting on redaction is
  still required, by `redaction-completeness`. It cannot be the only
  defence.

A full-text index has one more rule, because it serves the baseline and the
baseline must not vary: it may replace the scan only where it gives the
scan's answer. An implementation that cannot tell whether its index is
current scans. In practice an index can be checked against the directory
listing and the index entries, as a late merge is.

### More than one vector for an episode

A turn can hold a pasted document. One vector for it retrieves poorly, and
may exceed the model's input. The cache may hold several, each with its span
and a hash of the span.

Spans stay valid because `content.text` changes only by being redacted
whole. They are private to the cache: the format has no way to cite part of
an episode, and this does not add one.

### Referenced content may be embedded, tied to its hash

Finding a mail by meaning needs its body. The body is not in the workspace,
and *Point, don't copy* says it should not be.

A vector is allowed as the one derivative of referenced content an
implementation may keep, on three conditions:

- **Only in the cache,** and the fetched content itself is not kept.
- **Tied to `content.hash`.** The vector records the hash it was computed
  against and is used only while the episode carries that hash. A vector of
  different bytes describes something the episode does not point at.
- **Dropped when the source is `changed` or `gone`.** The recorded version
  can no longer be fetched, so the vector cannot be checked or rebuilt, and
  would be the only surviving copy of something. "A source being deleted is
  not a request to forget" protects the episode. It does not license a copy.

An episode with no `hash` has nothing to tie a vector to, so only its
`label` is embedded. Keying on `version` was considered. A `version` says a
source changed, but not that the bytes fetched are the bytes recorded.

Fetching to embed is a source check, whether or not it was meant as one.
The implementation has the bytes and the recorded hash. If they differ it
writes `source_status`, as any check would, and does not quietly skip.

### No scope, and remote embedding decided by the machine

DKF limits remote embedding by scope. Episodes have none, and #39 asked
whether to add one.

A per-episode scope cannot work here. Episodes change only by
`source_status` and redaction, so a scope written at recording could never
be widened or narrowed. The field that most needs to change would be the
one that cannot.

So the limit is the machine's:

- **Off by default,** and nothing in a workspace can turn it on. A cloned
  workspace must not be able to cause text to leave the machine.
- **All or narrowed.** When on, it covers every episode, unless the
  configuration narrows it by `standpoint`, `kind` or `source.harness`.
  Those are fixed at recording, and the first two are in the index.
- **Fetched content separately.** A mail body sits behind the mailbox's own
  access control, and the episode records only that it exists. Sending it
  elsewhere is a larger step than sending a label, so it has its own
  setting.

The format says what the configuration must be able to express, and not
where it is kept or what it looks like.

### Restated, with the source named

*Conformance* requires the format to stand without DKF, so the rules are
written out. The section names the DKF section it came from, informatively,
so that a fix to one shows up as something to check in the other.

### Three capabilities

`recall-by-query` is what is returned. `derived-caches` is what may be kept
to return it faster or better. `remote-embedding` is what may leave the
machine. An implementation can adopt the first alone.

## Risks / Trade-offs

- **The baseline is linear, and conversations are large.** → Stated in the
  text. A full-text index is allowed, under the rule that it gives the
  scan's answer.
- **Substring matching returns noise for short terms.** `a` matches almost
  everything. → Order puts episodes matching more terms first, and `limit`
  cuts. Stopwords would make the baseline depend on a language.
- **The check against the file costs a read per proposed episode.** → The
  filters already read it. A semantic stage proposes a bounded number.
- **Requiring `hash` leaves much mail unembedded.** Provider APIs often give
  no raw bytes, and `duplicate-recordings` then forbids a hash. → The label
  is still embedded and still matched by the baseline. A vector that cannot
  be tied to what the episode points at is worse than none.
- **Dropping vectors on `gone` loses recall of things the person may still
  want found.** → The episode remains, with its label, time and
  participants. Anything worth keeping about its content belongs in a claim
  that quotes it.
- **"Outside the workspace tree" is awkward for a hosted store** with no
  directory. → The rule that matters is the second half: not committed,
  published or served with the workspace.
- **The DKF copy can drift.** → Named in the text, and left with #43.

## Migration Plan

Nothing in a workspace changes. The change is applied to README.md after
the four it builds on, since the new section refers to rules they add.

episodes-cli has no query command. Adding one is a new change there, to be
raised as an issue once this is merged.

## Open Questions

- **Should the filter by `occurred` be defined?** The section requires one
  and does not say how a range meets an episode with a `start` and no `end`,
  or a date alone. Recall by time has the same gap today.
- **Recall by query for the family** (#43), with the provenance spine.
