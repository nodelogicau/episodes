## 1. `anchor`

- [ ] 1.1 Confirm that `tighten-canonical-form` and `redaction-completeness` have been applied to README.md, and stop if either has not.
- [ ] 1.2 In *Links* in README.md, change "Each link has exactly `rel` and `href`" to allow an optional `anchor`, and add:
  - a link with no `anchor` is about the episode, and one with `anchor` is about the content the episode refers to;
  - the value of `anchor` equals `content.ref` exactly, and a validator rejects any other;
  - `anchor` appears only on an episode that carries `content.ref`;
  - no other use of `anchor` is admitted.
- [ ] 1.3 Extend the sort rule: a link with no `anchor` comes before one with the same `rel` and `href` that has one.

## 2. `memento`

- [ ] 2.1 Change "Two registered relations have a meaning between episodes" to introduce a third, about the referenced content, and add `memento` (RFC 7089):
  - with `anchor`, an archived snapshot of the content as it was when the episode was recorded;
  - its `href` is a URI, never an episode id;
  - without `anchor` it is invalid;
  - an episode may carry more than one.
- [ ] 2.2 Add an example of a reference episode for a web page with a `memento` link.
- [ ] 2.3 Under *Links are written once*, add that a snapshot is linked only at recording, and is one the writer had made then or an existing one it has compared with the content it fetched.
- [ ] 2.4 Add the rule that a writer MUST NOT cause content to be archived unless the person explicitly asks, and that recording is not such a request.

## 3. Readers

- [ ] 3.1 In *`source_status`*, beside the rule against back-filling, add:
  - a reader may fetch a snapshot when the source is `changed`, `unreachable` or `gone`, and presents it as an archive's copy;
  - `source_status` is unchanged by that;
  - a writer does not copy a snapshot's content into the episode.
- [ ] 3.2 Add that a snapshot need not match `content.hash`, and that a mismatch is reported as unverified.

## 4. Finish

- [ ] 4.1 In *Design Principles*, check that *Point, don't copy* still reads correctly, and add a clause on snapshots only if it needs one.
- [ ] 4.2 Add RFC 7089 and Robust Links to References.
- [ ] 4.3 Proofread, and run `openspec validate web-content`.
- [ ] 4.4 Raise the episodes-cli follow-up as an issue on nodelogicau/episodes-cli: anchored links in `record ref` and `validate`.
