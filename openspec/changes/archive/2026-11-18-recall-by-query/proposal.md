## Why

The draft defines no way for a free-text question to find an episode. The
index serves "recall by time, by conversation and by speaker", and the only
mention of embeddings is one sentence under redaction. Other long-term memory
stores are queried by text, and usually by vector similarity, so an
implementation that wants the same has no rules to work to:

- Two implementations will differ on what a query returns (#38).
- Each will decide for itself where vectors of private conversations are
  kept, and whether text may be sent to another host to be embedded (#39).
- Nothing says whether the content of a mail or a document, which the
  workspace points at and does not hold, may be embedded at all (#40).
- A long inline text does not fit one vector (#41).
- "What did I discuss with X?" has no bounded answer when X is a participant
  and not the standpoint, because `participants` is not in the index (#42).

DKF answers most of this for claims in *Recall by query*. Its rules carry
over, with four differences that episodes force: there are no particulars to
resolve to, episodes have no scope, a redaction can remove one field and
leave the episode, and reference episodes point at content the workspace
does not hold.

Issues #38, #39, #40, #41, #42 and #43, and the review comments on each.

## What Changes

A new section, *Recall by query*, restated in full so that the format stands
alone. It applies to an implementation that answers a free-text query. An
implementation need not offer one.

- **A query resolves to episodes.** Each result is one episode. A container
  is returned when its own text matches, not because a child matched. A
  reader may group results by `container`, which every result carries.
- **A baseline that needs no model, run on every query.** It is DKF's:
  terms are runs of non-whitespace, trimmed of leading and trailing
  punctuation, compared under Unicode case folding, and combined by OR. It
  matches against `label` and inline `content.text`. A term that equals a
  reference episode's `content.uid` as written also matches, so that
  `mid:…` finds its mail.
- **Other stages only add.** A semantic stage MAY add episodes and MUST NOT
  remove one the baseline found.
- **`resolution` on every result:** `uid`, `lexical` or `semantic`, the
  first that applies.
- **A fixed order,** so that two implementations return the same episodes
  when `limit` cuts: by `resolution`, then within `uid` and `lexical` by
  the number of distinct terms matched, most first, then by id, latest
  first. Order within `semantic` is the implementation's own.
- **Filters run afterwards, against the files and the index:** time,
  `container`, `standpoint`, `kind` and participant. A withdrawn episode is
  not returned. A match on a field counts only while the episode's file
  still carries that field, which is the rule `redaction-completeness`
  states for every derived value.
- **Recall by participant is a filter, and is not bounded.** It reads
  episode files, so it is linear in history. The text says so.
- **Derived caches are allowed, under one set of rules.** A semantic cache,
  a full-text index and a participants cache are each optional. Each:
  - is stored outside the workspace directory tree, and is never committed,
    published or served;
  - is not read by validators or source checks;
  - records, for every entry, the episode id and the field it was computed
    from;
  - only proposes episodes, each checked against its file before it is
    returned;
  - may be missing, partial or stale, which MAY lower recall or speed and
    MUST NOT cause an episode to be returned that the baseline and filters
    would not allow.
- **A full-text index may stand in for the baseline scan** only where it
  returns what the scan would.
- **A semantic cache records the model that produced it,** and is not
  consulted when that differs from the model in use. It MAY hold more than
  one vector for an episode, each recording the span of `content.text` it
  covers and a hash of that span.
- **Referenced content may be embedded, and only in the cache.** The vector
  records the `content.hash` it was computed against, and is consulted only
  while the episode carries that hash. An implementation that fetches
  content to embed it and finds a different hash has made a source check,
  and records `changed` as any check would. A vector of a source that is
  `changed` or `gone` is not consulted, and is deleted no later than the
  cache's next update. A reference episode with no `hash` has only its
  `label` embedded.
- **Remote embedding is off unless configured on the machine.** Episodes
  have no scope, so when it is on it covers every episode, unless the
  machine's configuration narrows it by `standpoint`, `kind` or
  `source.harness`. Sending fetched content of a reference episode to
  another host needs its own setting, off by default. No scope field is
  added to the format.
- **The section names the DKF text it was restated from,** so that a fix to
  one copy shows as a difference to check in the other. *Status* notes,
  under *A provenance spine*, that recall by query is one more shared shape.

## Capabilities

### New Capabilities

- `recall-by-query`: what an implementation that answers a free-text query
  returns:
  - the baseline, its text and its terms;
  - that other stages only add;
  - `resolution` and the order of results;
  - the filters, including participant, and that they run against the
    files.
- `derived-caches`: the rules for a semantic cache, a full-text index and a
  participants cache:
  - where they are kept, and what does not read them;
  - what each entry records;
  - that a cache only proposes;
  - more than one vector for an episode;
  - vectors of referenced content, and what happens on `changed` and
    `gone`.
- `remote-embedding`: when text may be sent to another host to be embedded,
  with no scope in the format.

### Modified Capabilities

None. `standalone-conformance` requires the document to stand without DKF,
and the new section is restated in full, so that requirement holds as it is.

## Impact

- `README.md`:
  - a new section, *Recall by query*, after *`index.yaml`*;
  - *What redaction does not remove*: the sentence on embeddings points to
    the new section;
  - *`index.yaml`*: the sentence on what recall the index serves notes that
    recall by participant and by query read the files;
  - *Status*: *A provenance spine* and *Index masking*.
- Nothing is added to an episode, to `episodes.yaml` or to the index. No
  valid workspace becomes invalid. Machine configuration for remote
  embedding lives outside the workspace and is not specified beyond what it
  must be able to say.
- This change builds on four that are proposed and not yet applied:
  - `redaction-completeness`, for the rule that a derived value of a
    redacted field is not used;
  - `duplicate-recordings`, for which bytes `content.hash` covers;
  - `acts-and-containers`, for the `attested` mode and what a container is;
  - `settle-edge-cases`, for a withdrawn episode not being returned.
  It should be applied after them.
- episodes-cli has no query command. One would be a new change there, to be
  raised as an issue.
- Closes #38, #39, #40, #41 and #42. #43 is answered by restating, and stays
  open as part of the provenance spine question.
