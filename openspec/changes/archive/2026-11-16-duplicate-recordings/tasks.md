## 1. Ordinals

- [x] 1.1 In *Containment* in README.md, add:
  - a writer MUST NOT write an `ordinal` that another episode it can see holds in the same `container`;
  - a writer uses the source's positions where it has them, and otherwise one more than the highest `ordinal` in the container, starting at 1;
  - gaps are valid;
  - a validator warns, naming both episodes, on a repeated `ordinal`, and rejects neither, with the two-branch merge as the reason;
  - readers order children by `ordinal` and then by id, with children that have no `ordinal` last.
- [x] 1.2 Update the `ordinal` row of the `EPISODE` field table to point at those rules.

## 2. A second recording

- [x] 2.1 In `content`, after the paragraph on possible duplicates, add the writer rule:
  - a writer that can see the workspace SHOULD NOT record a second reference episode with the same `standpoint`, `media_type` and `uid`;
  - unless told explicitly that the content is distinct, as an instance of a recurring event is;
  - a writer that declines names the existing episode;
  - why it is a SHOULD: `uid` is unindexed, and two machines cannot see each other.

## 3. `hash`

- [x] 3.1 Replace "taken over the content as fetched" in the paragraph defining `hash` with the bytes per media type:
  - `message/rfc822`: the complete raw message as the mailbox stores it;
  - `text/calendar`: the iCalendar object holding the event, as the calendar store returns it;
  - any other type: the bytes of that representation;
  - no `media_type`: the bytes `ref` returns, and a writer SHOULD write `media_type` with `hash`.
- [x] 3.2 Add that a writer without those bytes MUST NOT write `hash`, and records `version` where the source has one.
- [x] 3.3 Add that a hash identifies one stored copy, that copies held by different people differ, and that hashes are not compared across standpoints.
- [x] 3.4 Update the comment on `hash` in the reference `content` example ("of the content as fetched").

## 4. Status

- [x] 4.1 Rewrite the *Duplicate recordings* entry to what remains open: how an existing duplicate is marked, and content with no `uid`.

## 5. Finish

- [x] 5.1 Proofread, and run `openspec validate duplicate-recordings`.
- [x] 5.2 Raise the two episodes-cli follow-ups as issues on nodelogicau/episodes-cli: the bytes a caller supplies for `hash`, and the order of children in `list`.
