## Context

`content` says where the record of a happening lives and how its text came to
exist (`media_type`, `derivation`), but not what language it is in. Issue #12
proposed an optional `content.language` holding a BCP 47 tag, and asked three
questions: whether reference episodes may carry it, how it interacts with
`derivation: transcribed`, and whether it is redactable. The review comment on
the issue answered them, and this design records those answers.

Two existing rules bear on it:

- **Record, never interpret.** An episode says what happened. A judgement
  about it is a claim in another format.
- **The zone rule** in `occurred`: written whenever it is known, and never
  guessed.

## Goals / Non-Goals

**Goals:**

- Keep a language that a source states, or that a harness set, instead of
  losing it when the episode is written.
- Give the field one meaning on every episode that carries it: the language of
  that episode's content as recorded.
- Use BCP 47 as it stands, with no profile of its own.

**Non-Goals:**

- Detected languages. A detector's output is a judgement, and anything that
  needs a guess can make one from the text at read time.
- Translation. A recogniser that writes text in a language other than the
  audio's has translated it, and no `derivation` value says so. That is a
  separate question, listed under Open Questions.
- Indexing `language` for search. That would make it unredactable.
- Per-span or per-turn language within one episode's text.

## Decisions

### Known, never guessed

- A writer records `language` only when the source states it, or when the
  harness produced the text in a language it set: a recogniser told which
  language to expect, or text rendered from structured data in a known
  language.
- A writer MUST NOT record a language that a detector chose, its own or the
  source's.
- **Why.** It matches "Record, never interpret" and the zone rule. A stored
  guess would be read later as fact, while a consumer can always detect from
  inline text itself.
- **Alternatives considered.**
  - Allow detection with a `basis` beside it, as `occurred` has. That adds a
    field to carry a judgement the format exists not to make, and a
    `detected` value would be most of the values written.
  - Allow detection freely. Then the field could not be trusted for anything
    a consumer could not already do.

### On reference and inline episodes alike

- On a reference episode, `language` is the language the source stated when
  the episode was recorded, captured as `label` is. The referenced content can
  change afterwards; `version` and `hash` already say whether it did.
- Mail and calendars are where a stated language is most often available, so
  limiting the field to inline episodes would lose its main use.
- It does not require `media_type`. Unlike `uid`, a BCP 47 tag means the same
  thing whatever the format.
- `content: {mode: none}` has no content, so it MUST NOT carry `language`.

### A transcript's language is its text's

- `content.language` describes the episode's own `text`.
- The spoken language is a property of the audio. The audio's episode carries
  its own `language` if one is known, and the transcript already points to it
  with `via`. So both languages are recorded, each on the episode it
  describes, and neither field has two meanings.
- A recogniser told which language to expect makes the language stated. A
  recogniser that auto-detected it is a detector, and nothing is written.

### One tag

- `language` is one BCP 47 tag, for the content's main language.
- Mixed content uses `mul`, which BCP 47 reserves for multiple languages.
- `und` (undetermined) MUST NOT be written, because an absent field already
  means unknown, and two spellings of unknown would have to be treated alike
  everywhere.
- **Alternatives considered.** A list, as `Content-Language` allows. Lists
  are rare in practice, their order means nothing in RFC 3282, and every
  consumer would have to handle one. A writer whose source gives a list
  records its first tag if one is the main language, and `mul` otherwise.

### Case and validation

- Writers use the case RFC 5646 §2.1.1 recommends (`en-AU`, `zh-Hant-TW`).
  Readers compare tags without regard to case, as BCP 47 requires.
- A validator rejects a tag that is not well-formed under RFC 5646's syntax.
- A validator MAY warn on a subtag missing from the IANA Language Subtag
  Registry. It does not reject, so a validator need not ship the registry, and
  a tag registered after the validator was built still passes.

### Redactable and unindexed

- `content.language` joins the closed set of redactable fields. It can
  disclose something about a person, such as a minority language.
- It is not mirrored in the index, which is what keeps it redactable.
- Nothing redacts as a side effect, so a writer withdrawing `content.text`
  lists `content.language` explicitly if it should go too.

## Risks / Trade-offs

- **Few writers will have a stated language for typed turns.** A chat
  interface rarely knows the language of what was typed, and its locale is not
  that language. → Accepted: the field stays absent, and consumers detect from
  the text, as they do today.
- **Search cannot filter by language from the index.** → Accepted. That is the
  cost of keeping the field redactable, and the trade-off the index already
  makes for all of `content`.
- **A source can state the wrong language.** A mail client may stamp its
  user's locale on every message. → The field records what the source
  stated, like `basis: stated` for time, and a claim can disagree with it.
- **Collapsing a list to one tag loses detail.** → Accepted for simplicity;
  the referenced content still carries its full header.

## Migration Plan

There is none. The change is additive and the format is a draft.

## Open Questions

- **Translated transcripts.** Should `derivation` gain a `translated` value,
  or should a translation be recorded some other way? Added to Status in the
  README and best taken up in its own issue.
