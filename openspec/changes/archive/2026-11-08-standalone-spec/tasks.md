## 1. Remove `occasion`

- [x] 1.1 Delete the `occasion` row from the `EPISODE` field table and the `#### occasion` section
- [x] 1.2 Remove the `occasion` arrow from the Object Model diagram
- [x] 1.3 Remove `occasion` from the list of fields kept out of the index in `### index.yaml`
- [x] 1.4 Rewrite the loop-closing paragraph ("This is where the family's loop closes…") as informative text in Relation to other formats: the link between an episode and an intention is recorded by another format, typically a DKF claim citing both
- [x] 1.5 Add one sentence (under Field order or the field table) saying a reader ignores and gives no meaning to fields the format doesn't define, such as an `occasion` left over from a draft

## 2. Define identities without DKF

- [x] 2.1 In Source and timestamp, define `author` as a URI where one is known, otherwise a string identifier; resolving it is outside the format. Replace "a reference to a particular … as in DKF"
- [x] 2.2 Update the `standpoint` section and the `participants` and `place` table rows the same way. Add an informative note that a DKF workspace may treat these values as particulars

## 3. Restate the content hash

- [x] 3.1 In `#### content`, replace "`hash` follows DKF's definition" with the full rule: SHA-256, CRLF→LF only, nothing else changed, `<algorithm>:<digest>`; writers write `sha256`; readers report unknown algorithms as unverified, not invalid
- [x] 3.2 Add an informative note that the rule matches DKF's

## 4. Restate redaction

- [x] 4.1 Replace the opening "follows DKF's redaction in shape and in every rule…" with a self-contained introduction, keeping an informative "matches DKF's" note
- [x] 4.2 State that a required field (`content.text` on an inline episode, `content.ref` on a reference episode) is valid when absent only because `redacted.fields` lists it, and that this is how a validator tells a redaction from a malformed file
- [x] 4.3 Check that the closed set, single-block and merge rule, irreversibility, non-cascade and git-store MUST are each stated in full in the section, and reword any that still say "as DKF" or "DKF's terms"

## 5. Restate sharding and the index

- [x] 5.1 Replace "The layout follows DKF's sharding" with the full rules:
  - path from the id alone, UTC month of minting;
  - `legacy/` for ids with no derivable month;
  - sealing with one month of grace;
  - a sealed month allows only rewriting `source_status` and gaining or extending `redacted`
- [x] 5.2 Add late-merge detection: segment `count` equals that month's file count; a mismatch fails validation naming the files; the remedy is re-minting before merge
- [x] 5.3 Add future-id validation: warn on an id or timestamp later than now; fail on an id two or more months ahead of the validator's current month
- [x] 5.4 In `### index.yaml`, give the root index shape (`format`, `segments` with `path` and `count`, `entries`) and the sealed segment shape (`format`, `entries`) with a short example. State that the index is a derived cache that can always be rebuilt from the files, and that a missing or stale index must not produce wrong results
- [x] 5.5 Compare 5.1–5.4 side by side against DKF's *Sharding* and *index.yaml* sections and confirm no rule's meaning changed beyond the adaptations in design.md decision 5

## 6. Mark what is normative

- [x] 6.1 Add a `## Conformance` section before Core Object Types: RFC 2119/8174 key words; Core Object Types and File Layout are normative; every other section is informative; the format is complete on its own and implementing it needs no DKF or intentions code or data
- [x] 6.2 Rename "How the other formats cite an episode" to "Relation to other formats", mark it informative, and leave out the intentions paragraph that relied on `occasion`
- [x] 6.3 Change the Purpose sentence "an episode may name the intention it was the occasion of" to match the removal
- [x] 6.4 Update Design Principles ("Compose by reference") so that episodes cite no other format and are cited by them

## 7. Verify

- [x] 7.1 Search the normative sections for `DKF`, `intentions`, `particular` and `follows`. Every hit is either labelled informative or says only what an episode does not hold
- [x] 7.2 Search the whole README for `occasion`. No hits remain except a Status or informative mention of the removal, if any
- [x] 7.3 Read the normative sections start to finish, as an implementor who has never seen DKF, and fix anything that can't be implemented from the text alone
- [x] 7.4 Update Status if needed, for example by noting in the provenance-spine question that the shared rules are now duplicated
