## 1. `occurred` as RFC 9557

- [x] 1.1 Rewrite the `occurred` section of README.md to cover:
  - the RFC 9557 grammar: an offset is required, and a bracketed IANA zone is written when it is known;
  - offset-only values, from sources that give only an offset;
  - a date alone with an optional `tz`;
  - the same form for `start` and `end`;
  - no critical flag and no other suffixes;
  - the rule that the offset governs, with a warning when it disagrees with the zone;
  - quoting.
- [x] 1.2 Replace the zone-versus-offset rationale with the case for having both. The offset fixes the instant, including in the repeated hour, and the zone is what lets "tomorrow at 2" be resolved.
- [x] 1.3 Restate the "Nothing is recorded before it happens" comparison:
  - compare the instant the offset fixes;
  - compare a date alone in `tz` where present, otherwise in UTC with one day's allowance.
- [x] 1.4 Update every `occurred` example in README.md: quoted values, offset plus zone, and no `tz`. This covers the EPISODE example, the calendar example, the self-attested act example and the `index.yaml` example.
- [x] 1.5 Update the "Source and timestamp" sentence that calls `occurred` the exception to the timestamp rule.

## 2. `links`

- [x] 2.1 Add `links` to the EPISODE field table, in canonical order after `ordinal` and before `content`.
- [x] 2.2 Add a `#### Links` section covering:
  - RFC 8288 `rel` (an IANA-registered relation or an absolute URI) and `href` (an episode id or a URI);
  - sorting;
  - no rejection for an unknown `rel`;
  - written once, and an episode target must be recorded earlier;
  - unresolved targets are reported, not invalid;
  - the episode meanings of `via` and `predecessor-version`, with the transcript example;
  - no restating `container`;
  - provenance, not judgement.
- [x] 2.3 Add `links` to the closed redactable set in Redaction. Note that redacting it removes the whole list, and that the index never mirrors it.
- [x] 2.4 State in the `content` section that `content.ref` MUST NOT be an episode id, and that relations between episodes are links.

## 3. Self-attested acts

- [x] 3.1 Rewrite the Self-attested acts section:
  - `content: {mode: none}` always;
  - the attestation is a `via` link;
  - the standpoint check applies to the `via` target, and an unresolved target is reported;
  - the single shape test.
- [x] 3.2 Update the self-attested example to `content: {mode: none}` with a `via` link.
- [x] 3.3 Update the `content` field-table row and the `content: {mode: none}` paragraph in the `content` section.

## 4. Status, references and consistency

- [x] 4.1 Update the Status open questions:
  - derived renderings: say in part how `via` and `predecessor-version` answer it;
  - duplicate recordings: links are where a later version could mark a repeat;
  - add a question on uncertain and approximate dates (EDTF / ISO 8601-2).
- [x] 4.2 Add RFC 9557, RFC 8288, the IANA Link Relations registry, RFC 4287 (`via`) and RFC 5829 (`predecessor-version`) to References.
- [x] 4.3 Update the Object Model diagram if it shows relations between episodes.
- [x] 4.4 Proofread the README:
  - check that no `tz` remains beside a date-time and no unquoted `occurred` value remains;
  - check that every `content.ref` example is not an episode id;
  - check that the standalone-conformance wording still holds.
- [x] 4.5 Run `openspec validate adopt-web-standards`.
