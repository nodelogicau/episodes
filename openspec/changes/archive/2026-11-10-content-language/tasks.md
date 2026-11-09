## 1. `content.language`

- [x] 1.1 Add `language` to the inline `content` example in README.md, and to the reference example with a comment noting it is optional.
- [x] 1.2 Add a paragraph to the `content` section defining `language`:
  - one well-formed BCP 47 tag, the language of the content as recorded;
  - recorded only when the source states it or the harness set it, never from detection;
  - on a reference episode, as stated when recorded, with no `media_type` requirement;
  - on a transcript, the language of its `text`, with the spoken language on the audio's episode, linked by `via`;
  - `mul` for mixed content, `und` never written, absent for unknown;
  - not on `content: {mode: none}`;
  - case per RFC 5646 §2.1.1, compared without regard to case;
  - ill-formed tags rejected, unregistered subtags at most warned on.

## 2. Redaction and index

- [x] 2.1 Add `content.language` to the closed redactable set.
- [x] 2.2 Check that the `index.yaml` exclusion sentence ("Nothing in `content` …") already covers `language`, and change nothing if it does.

## 3. Status and references

- [x] 3.1 Add a *Translated transcripts* open question to Status: whether `derivation` needs a `translated` value.
- [x] 3.2 Add BCP 47 and RFC 3282 (`Content-Language`) to References, and mention iCalendar's `LANGUAGE` parameter beside RFC 5545.
- [x] 3.3 Proofread, and run `openspec validate content-language`.
