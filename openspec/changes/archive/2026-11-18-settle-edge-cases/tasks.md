## 1. A clock that runs ahead

- [x] 1.1 In `occurred` in README.md, under *Nothing is recorded before it happens*, add:
  - where `basis` is `stated`, a date-time may be up to five minutes later than `timestamp`;
  - a writer MAY record such an episode, and records the time as the source stated it;
  - the allowance does not apply to `recorded` or `inferred` times, and does not add to the allowance for a date alone;
  - why: a source's clock and the writer's can disagree, and the writer cannot correct a time a source stated.
- [x] 1.2 Rewrite the paragraph on what a validator warns on, so that it warns beyond the allowance that applies.

## 2. Where the zone comes from

- [x] 2.1 In `occurred`, under *The zone is written whenever it is known*, add for a `recorded` time:
  - the zone is the one in which the recording was made;
  - a writer takes it from the value, then the device at which the person took part, then `defaults.zone`;
  - a writer with none of these writes the offset alone;
  - where the person lives, or says they are, is not a source.
- [x] 2.2 Add that a writer does not write a zone that contradicts the offset:
  - it writes the offset alone, whichever source the zone came from;
  - a critical flag still means refuse, with a pointer to *No other suffixes*;
  - a zone the writer has no rules for is left out;
  - a value in `Z` has no local offset, so `defaults.zone` is not applied to it, and a zone from the device is written with the local time.
- [x] 2.3 Add that `defaults.zone` is never applied to a `stated` or `inferred` time, or to a date alone.
- [x] 2.4 In *`episodes.yaml`*, add `zone: Australia/Melbourne` under `defaults` in the example, and a sentence saying it is one IANA zone name, optional, and read by writers only.

## 3. Redaction

- [x] 3.1 In *Redaction*, after the paragraph on `fields`, add:
  - a path in `fields` records that the episode carried the field and that it was removed;
  - a writer refuses a path the episode does not carry, naming it, unless the block already lists it;
  - a validator cannot check this, so it is a rule for writers.
- [x] 3.2 Rewrite *Redacting `content.text` withdraws an inline episode* to define "out of recall":
  - a reader does not return the episode as content;
  - a reader MAY show that it exists and where it stands, using only the fields that cannot be redacted;
  - a reader MUST NOT show anything that was redacted.

## 4. The index

- [x] 4.1 In *Sharding*, under *A late merge is detected by count*, add that a rebuild does not rewrite an existing segment and fails as validation does, naming each file with no entry and each entry with no file.
- [x] 4.2 In *`index.yaml`*, say that the index is reconstructible from the files in a workspace with no late merge, and that a rebuild writes the root and any missing segment.
- [x] 4.3 In the paragraph on a month sealing, add that a sealed month with no files has no segment and no entry in `segments`.

## 5. Finish

- [x] 5.1 Proofread, and run `openspec validate settle-edge-cases`.
- [x] 5.2 Raise the two episodes-cli follow-ups as issues on nodelogicau/episodes-cli: the five-minute allowance in `record`, and leaving the zone out when it contradicts the offset or the value has no local offset.
