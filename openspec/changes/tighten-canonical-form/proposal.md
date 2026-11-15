## Why

The draft says canonical output is "what makes two implementations produce
byte-identical files for identical episodes". Building the reference
implementation, episodes-cli, found four places where two careful
implementations would still write different files, or disagree about whether a
file is valid:

- `participants` is "sorted", but the draft does not say by what, and its own
  `EPISODE` example is not sorted (#35).
- A writer handed an RFC 9557 suffix it may not write is told not to write it,
  but not whether to drop it or refuse the input (#28).
- The `content.language` scenario rejects `english`, which is well-formed
  under the RFC 5646 grammar, so the scenario contradicts the rule it
  illustrates (#36).
- Whether a `rel` is valid depends on which copy of the IANA registry a
  validator carries, so validity changes with the date a validator was built
  (#26).

None of these changes what an episode means. Each one decides a case the draft
leaves open, so the fix is small now and costly once files exist.

Issues #26, #28, #35 and #36, and the review comments on #35 and #36.

## What Changes

- **One comparison for every sorted list.** Where the format sorts strings,
  it sorts by Unicode code point. That is the same order as the UTF-8 bytes,
  and it differs from the UTF-16 order that Java and JavaScript sort by
  default. This is stated once, under *Field order*.
- **`participants` is sorted by that comparison, with exact duplicates
  removed.** Values are compared as written, with no URI normalisation. The
  `EPISODE` example is corrected, so `https://claude.ai` comes first.
- **`links` uses the same comparison,** by `rel` and then by `href`. The rule
  is already there; this names the comparison.
- **A writer drops an elective RFC 9557 suffix it is handed** and records the
  value without it. A calendar tag such as `[u-ca=gregory]` carries no meaning
  under this format. A writer MUST refuse a value with a critical suffix other
  than the zone, because the source has said the value cannot be read
  correctly without it. A critical flag on the zone itself is honoured by
  checking that the offset agrees with the zone: if it does, the writer
  records the value without the flag, and if it does not, the writer refuses.
- **The ill-formed language example becomes `en_AU`.** "Well-formed" keeps
  meaning exactly the RFC 5646 §2.1 grammar, which needs no registry. The text
  says so in as many words, and says that `english` is therefore well-formed
  and at most warned on.
- **An unregistered `rel` is a warning, not an error.** Writers still MUST use
  a registered relation or an absolute URI. A validator warns on a `rel` that
  has the form of a registered relation (RFC 8288 `reg-rel-type`: lowercase
  letters, digits, `.` and `-`, starting with a letter) but is missing from
  its copy of the registry. Only a `rel` that is neither of that form nor an
  absolute URI is invalid. **BREAKING** for a validator that reports an
  unregistered `rel` as an error: `rel: answers` is now valid with a warning.

## Capabilities

### New Capabilities

- `canonical-form`: how canonical output orders lists of strings:
  - the comparison (Unicode code point order of the strings as written);
  - `participants` sorted by it, with exact duplicates removed;
  - no normalisation of references before comparing.

### Modified Capabilities

- `episode-links`: in *`links` follows RFC 8288*,
  - the sort by `rel` then `href` uses the `canonical-form` comparison;
  - an unregistered `rel` of registered form is valid, and a validator warns;
  - the scenario *A non-URI unregistered relation* changes from rejected to
    warned on, and a new scenario covers a `rel` of neither form.
- `occurred-time`: in *No critical flag and no other suffixes*, what a writer
  does when handed an elective suffix, a critical suffix, or a critical flag
  on the zone.
- `content-language`: in *`content.language` holds one BCP 47 tag*,
  - "well-formed" is stated to mean the RFC 5646 §2.1 grammar;
  - the scenario *An ill-formed tag* uses `en_AU`;
  - a new scenario records that `english` is well-formed.

## Impact

- `README.md`:
  - *Field order*, with the comparison;
  - the `EPISODE` example and the `participants` row of its table;
  - `occurred`, the *No other suffixes* bullet;
  - `content`, the *Case* bullet under `language`;
  - `links`, the paragraph defining `rel`.
- No field is added or removed, and no valid episode written by a conformant
  writer becomes invalid. An episode whose `participants` are unsorted stays
  readable, since readers accept any order.
- episodes-cli follows in three places, each to be raised as an issue there:
  - `record` refuses an elective suffix today, and would drop it;
  - `validate` reports an unregistered `rel` as an error, and would warn;
  - its language check rejects a primary subtag of four or more letters, which
    goes beyond the grammar, and would stop.
  Its `participants` order already matches.
- Closes #26, #28, #35 and #36.
