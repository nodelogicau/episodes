## 1. Sorting

- [ ] 1.1 In *Field order* in README.md, add the comparison: strings the format sorts are compared by Unicode code point as written, which is the order of their UTF-8 bytes and not of their UTF-16 code units.
- [ ] 1.2 In the `EPISODE` example, put `https://claude.ai` before `https://github.com/benfortuna` in `participants`.
- [ ] 1.3 In the `participants` row of the field table, say:
  - sorted by the comparison in *Field order*;
  - each value written once, compared as written with no normalisation;
  - a reader accepts any order, and a validator may warn but does not reject.
- [ ] 1.4 In `links`, say the sort by `rel` and then `href` uses the same comparison.
- [ ] 1.5 Check every other example in README.md that shows `participants` or `links` is in order.

## 2. `occurred` suffixes

- [ ] 2.1 Extend the *No other suffixes* bullet with what a writer does when given:
  - an elective suffix other than the zone: drop it and record the rest;
  - a critical suffix other than the zone: refuse;
  - a critical flag on the zone: record without the flag when the offset agrees with the zone, and refuse when it disagrees or the zone is not known.

## 3. `content.language`

- [ ] 3.1 In the *Case* bullet, say that well-formed means the RFC 5646 §2.1 grammar, checked without the registry, with `en_AU` as an ill-formed example and `english` as a well-formed one that may be warned on.

## 4. `links`

- [ ] 4.1 Replace "A `rel` that is neither is invalid" with:
  - a writer MUST NOT write a `rel` that is neither registered nor an absolute URI;
  - a validator warns on a `rel` of the RFC 8288 registered form that its copy of the registry lacks;
  - only a `rel` that is neither of that form nor an absolute URI is invalid.

## 5. Finish

- [ ] 5.1 Proofread, and run `openspec validate tighten-canonical-form`.
- [ ] 5.2 Raise the three episodes-cli follow-ups as issues on nodelogicau/episodes-cli: elective suffixes in `record`, unregistered `rel` in `validate`, and the language check.
