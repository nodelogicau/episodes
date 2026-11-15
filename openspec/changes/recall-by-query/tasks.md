## 1. The section

- [ ] 1.1 Add a section *Recall by query* to README.md after *`index.yaml`*, opening with:
  - an implementation need not answer free-text queries, and one that does follows these rules;
  - an informative note naming DKF's *Recall by query* as the text these rules were restated from.
- [ ] 1.2 State the baseline:
  - the terms, the trimming of whitespace and of punctuation, and the empty query;
  - case folding, substring match, and OR;
  - the texts: `label`, and `content.text` of an inline episode;
  - a term equal to `content.uid`, before or after trimming, with no folding;
  - no stemming or stopwords, and that the baseline is linear in history.
- [ ] 1.3 State that other stages MAY add episodes and MUST NOT remove one the baseline found.
- [ ] 1.4 State that a query resolves to episodes, that a container is returned only when it matched itself, and the three values of `resolution`.
- [ ] 1.5 State the order: by `resolution`, then distinct terms matched, then id descending, with `semantic` left to the implementation, and `limit` applied last.
- [ ] 1.6 State the filters:
  - they run after the stages, against the index and the files;
  - `occurred`, `container`, `standpoint` and `kind`;
  - a withdrawn episode is not returned;
  - a match on a field counts only while the file carries the field.
- [ ] 1.7 State the participant filter, that it compares references as written, and that it is linear in history.

## 2. Derived caches

- [ ] 2.1 Add the rules common to a semantic cache, a full-text index and a participants cache:
  - outside the workspace directory tree, never committed, published or served;
  - not read by validators or source checks;
  - each entry records its episode id and field;
  - a cache only proposes, and the file is read before an episode is returned;
  - a missing, partial or stale cache may lower recall or speed and returns nothing the baseline and filters would not allow.
- [ ] 2.2 Add that a full-text index replaces the scan only where it returns what the scan would.
- [ ] 2.3 Add the semantic cache rules:
  - it records its model, and is not consulted under another;
  - more than one vector per episode, each with its span and a hash of the span;
  - spans are internal to the cache.
- [ ] 2.4 Add the rules for referenced content:
  - it may be embedded, the vector is kept only in the cache, and the fetched content is not kept;
  - the vector records `content.hash` and is consulted only while the episode carries it;
  - no `hash`, no vector of the content;
  - a mismatch on fetch is recorded in `source_status`;
  - a vector of a `changed` or `gone` source is not consulted, and is deleted by the cache's next update.

## 3. Remote embedding

- [ ] 3.1 Add that remote embedding is off unless configured on the machine, that nothing in a workspace can turn it on, and that episodes carry no scope.
- [ ] 3.2 Add that the configuration may narrow it by `standpoint`, `kind` or `source.harness`.
- [ ] 3.3 Add the separate setting for fetched content, off by default.

## 4. The rest of the document

- [ ] 4.1 In *What redaction does not remove*, point the sentence on embeddings at the new section.
- [ ] 4.2 In *`index.yaml`*, after "recall by time, by conversation and by speaker", note that recall by participant and by query read the files.
- [ ] 4.3 In *Status*:
  - under *A provenance spine*, add recall by query as one more shape restated from DKF;
  - under *Index masking*, note that it would also let `participants` be indexed.
- [ ] 4.4 Add the new section to the table of contents, if the document has one.

## 5. Finish

- [ ] 5.1 Check that the section reads correctly against the text added by `redaction-completeness`, `duplicate-recordings`, `acts-and-containers` and `settle-edge-cases`.
- [ ] 5.2 Proofread, and run `openspec validate recall-by-query`.
- [ ] 5.3 Raise a query command for episodes-cli as an issue on nodelogicau/episodes-cli.
