## 1. Redacting `content.ref`

- [x] 1.1 In *Redaction* in README.md, after the paragraph on the closed set, add the rule:
  - a block that lists `content.ref` also lists each of `content.uid`, `content.version`, `content.hash` and `links` that the episode carries;
  - a writer redacts them in the same act;
  - a validator rejects a block that lists `content.ref` while any of the four is present;
  - each of the four stays redactable on its own.
- [x] 1.2 Rewrite the tombstone sentence under *Redacting `content.text` withdraws an inline episode* to say what a reference episode keeps: `id`, `kind`, `occurred`, `standpoint`, `container`, `ordinal`, `timestamp`, `content.mode`, `content.media_type`, and whichever of `label`, `participants`, `place` and `content.language` were not redacted as well.
- [x] 1.3 In *It is irreversible and never implicit*, add that redacting `content.ref` with the four fields is one redaction and not a side effect, because every field removed is named in `fields`.
- [x] 1.4 Say that an episode redacted before this rule is repaired by redacting the fields left behind.

## 2. Derived values

- [x] 2.1 In *What redaction does not remove*, replace the sentence on embeddings with the rule for every derived value:
  - embeddings, classifier and other model outputs, summaries and extractions, and search indexes, as examples;
  - deleted, or computed again without the redacted field;
  - a value is derived from a field when computing it again without that field could change it.
- [x] 2.2 Add that a derived value of a redacted field is not used, whether or not it has been deleted, and that this is decided from the episode file, with the pulled redaction as the reason.
- [x] 2.3 Add the informative note that an object of another format, such as a DKF claim citing the episode, is not a derived value and is governed by that format's redaction.

## 3. Finish

- [x] 3.1 Check that the reference `content` example and the *Redaction* example still agree with the rules.
- [x] 3.2 Proofread, and run `openspec validate redaction-completeness`.
- [x] 3.3 Raise the episodes-cli follow-up as an issue on nodelogicau/episodes-cli: `redact` and `validate` under the `content.ref` rule.
