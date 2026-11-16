## 1. Who writes episodes

- [x] 1.1 In the opening paragraph of README.md, change "Designed to be written by AI harnesses" to "Designed to be written by harnesses and connectors".
- [x] 1.2 In *Source and timestamp*:
  - say `harness` names the software that recorded the episode, an AI harness or a connector, with `gmail-sync` as an example;
  - say `model` is present only when a model took part;
  - update the comments in the `source` example to match;
  - add an informative sentence that a connector parses a source deterministically and that recording a reference episode needs no model.
- [x] 1.3 In *When an episode is recorded*, add an informative note separating recording, selection and consolidation, and saying only recording belongs to this format.

## 2. `mode: attested`

- [x] 2.1 In `content`, say there are four modes, and add `attested`: the record is the standpoint's own attestation, and `content` has no other key.
- [x] 2.2 Replace "`content: {mode: none}` is valid in exactly two cases" with: `mode: none` is a container with nothing of its own.
- [x] 2.3 Extend "Content with `mode: none` MUST NOT carry `language`" to `mode: attested`.
- [x] 2.4 Update the `content` row of the `EPISODE` field table.
- [x] 2.5 In *Self-attested acts*:
  - change the example to `mode: attested`;
  - change "Its `content` is always `{mode: none}`";
  - replace the paragraph *It is recognised by shape, not by `kind`* with recognition by mode, whatever the `kind` and whether or not it has children;
  - say how an act written with `mode: none` under the earlier draft now reads.
- [x] 2.6 In the same section, rewrite the attestation rule: an attestation made in an episode the writer records, including any made in conversation, is recorded and linked `via`; a dedicated control has no `via`; the rule does not depend on `source.harness`.

## 3. Containers

- [x] 3.1 In *Containment*, add:
  - a `mode: none` container is valid with or without children, and a validator warns on one with none;
  - a writer records a container before its children, and a validator warns when both ids are UUIDv7 and the container's sorts later;
  - a `container` that does not resolve is reported as unresolved and is not invalid;
  - an act may be a container.
- [x] 3.2 In *`standpoint`*, add whose a container with nothing of its own is, that it says nothing about who spoke within it, and that a container with content keeps its content's standpoint.

## 4. Finish

- [x] 4.1 Search README.md for every remaining `mode: none` and "self-attested" and check each against the new rules.
- [x] 4.2 Proofread, and run `openspec validate acts-and-containers`.
- [x] 4.3 Raise the two episodes-cli follow-ups as issues on nodelogicau/episodes-cli: `act` writes `mode: attested`, and `validate` keys the act rules on the mode and warns on a childless container.
