## Why

The format has nowhere to say what language an episode's content is in.
Recall, search, embedding and transcription all work better when they know,
and so does a reader deciding how to display a quote.

Sources often state the language themselves:

- mail's `Content-Language` header
  ([RFC 3282](https://www.rfc-editor.org/rfc/rfc3282));
- iCalendar's `LANGUAGE` parameter
  ([RFC 5545](https://www.rfc-editor.org/rfc/rfc5545));
- HTTP `Content-Language` and HTML `lang`.

A harness that transcribes or renders text often sets the language itself.
Today that knowledge is lost when the episode is written.

Issue #12, and the review comment on it.

## What Changes

- New optional field `content.language` on inline and reference episodes. It
  holds one [BCP 47](https://www.rfc-editor.org/info/bcp47) language tag
  (`en-AU`, `ja`), meaning the language of the content as recorded.
- **Known, never guessed.** A writer records `language` only when the source
  states it or the harness produced the text in a set language. A writer MUST
  NOT record a language a detector chose. This follows "Record, never
  interpret" and the time-zone rule.
- On a reference episode, `language` is the language as the source stated it
  when recorded, like `label`. It does not require `media_type`.
- On a transcript, `language` is the language of the episode's own `text`. The
  spoken language belongs to the audio's episode, which the transcript already
  points to with `via`.
- One tag, for the main language. Mixed content uses `mul`. Writers MUST NOT
  write `und`, because leaving the field out already means unknown.
- `content: {mode: none}` MUST NOT carry `language`.
- Writers use the standard case (RFC 5646 §2.1.1), and readers compare without
  regard to case. A validator rejects a tag that is not well-formed, and MAY
  warn on subtags not in the IANA Language Subtag Registry.
- `content.language` joins the closed set of redactable fields and is not
  mirrored in the index.
- References gain BCP 47 and RFC 3282. The RFC 5545 entry mentions `LANGUAGE`.

## Capabilities

### New Capabilities

- `content-language`: `content.language` covering:
  - its value (one well-formed BCP 47 tag, `mul` for mixed content, never
    `und`);
  - the rule that it is recorded only when known;
  - its meaning on reference episodes and on transcripts;
  - where it may not appear;
  - case and validation;
  - redaction, and its exclusion from the index.

### Modified Capabilities

None. The redaction requirement in `standalone-conformance` requires the
closed set to be stated, not its members, so adding a member changes no
requirement. The `content-identity` and `episode-evidence` requirements are
unchanged.

## Impact

- `README.md`:
  - the `content` section, with `language` in both examples and a new
    paragraph defining it;
  - Redaction;
  - Status, with an open question on translated transcripts;
  - References.
- The change is additive. No existing field changes meaning.
- Closes #12.
