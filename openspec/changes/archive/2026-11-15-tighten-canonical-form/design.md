## Context

*Field order* says canonical order "is what makes two implementations produce
byte-identical files for identical episodes, and so what makes a workspace
reviewable as a diff". The reference implementation, episodes-cli, was built
against the draft and recorded each place where the text left a choice. Four
of those are about canonical output or validity, and each got an issue: #26,
#28, #35 and #36.

In each case episodes-cli had to pick an answer to ship. Three of its answers
are stricter than the text allows:

| Issue | The draft | episodes-cli today |
|---|---|---|
| #35 | `participants` is "sorted" | Sorts by code point, removes exact duplicates |
| #28 | A writer MUST NOT write an elective suffix | Refuses the input |
| #36 | A scenario rejects `english` | Rejects a primary subtag of four or more letters |
| #26 | An unregistered `rel` is invalid | Reports an error from a dated registry snapshot |

## Goals / Non-Goals

**Goals:**

- Two writers given the same episode write the same bytes for `participants`
  and `links`.
- A writer given the same `occurred` value does the same thing with it.
- Two validators agree about whether an episode is valid, whatever registry
  copies they carry. They may differ only in warnings.
- Every scenario agrees with the requirement it illustrates.

**Non-Goals:**

- Normalising references. Whether two URIs name the same person is a
  judgement, and the format does not resolve references.
- Making field order a MUST. Writers SHOULD emit canonical order and readers
  accept any, and that stays.
- Canonical forms for anything else, such as YAML scalar styles or line
  width.
- The informative notes in #14, #15 and #32.

## Decisions

### Code point order, stated once

Strings are compared by Unicode code point. The alternatives were a locale
collation and a case-folded comparison. Both depend on tables that change
between Unicode versions, and a collation depends on the locale as well, so
neither gives the same bytes everywhere.

Code point order is the same as the order of the UTF-8 bytes, which is what
Go, Rust and C compare by default. It is not the order of UTF-16 code units,
which is what Java and JavaScript compare by default: the two differ for
characters above U+FFFF. The text says so, because that is the mistake an
implementor in those languages would make without noticing. References are
mostly ASCII, where every order agrees, so a wrong comparison would pass most
tests.

The rule goes under *Field order*, and `participants` and `links` refer to
it. A future sorted list gets the same comparison without restating it.

### Compared as written

Duplicates are removed only when they are identical strings, and nothing is
normalised first. `https://example.com/a` and `https://example.com/a/` both
stay. Normalising would need a rule for every scheme, and writers with
different rules would remove different values. It would also rewrite what the
source said, against "Record, never interpret".

### An unsorted `participants` is not invalid

A reader accepts `participants` in any order and with repeats. A validator
may warn and does not reject. This follows *Field order*, where a reader MUST
NOT reject a file for its arrangement. An episode written before this change,
or by hand, stays valid.

### A writer drops an elective suffix

The issue proposed that a writer MAY strip an elective suffix. That would
still allow two behaviours, a file or a refusal, from one input. The rule is
that a writer drops it.

Dropping loses nothing the format keeps. RFC 9557 defines an elective suffix
as one a recipient may ignore, and a reader of this format already must. The
commonest case is `[u-ca=gregory]` from a library that always prints the
calendar, and refusing it would make such a library's output unrecordable.

### A critical suffix is refused, except on the zone

A critical flag means the value must not be acted on unless the suffix is
understood. Two cases:

- **On any suffix but the zone,** the format has no way to keep the suffix,
  so recording the value without it would act on it while ignoring the flag.
  The writer refuses.
- **On the zone,** RFC 9557 gives the flag a specific meaning: an offset that
  disagrees with the zone is an error and not something to resolve silently.
  A writer can honour that by checking. If the offset agrees with the zone's
  rules, the demand is met and the value is recorded without the flag. If
  they disagree, or the writer does not know the zone, it refuses.

The alternative was to refuse every critical flag. That is simpler, but it
refuses values that are correct, and the check is one a validator already
makes to warn on a disagreement.

Without the flag, the existing rule stands: the offset governs and a
validator warns.

### `english` is well-formed

The scenario changes and the rule does not. The alternative, from the issue,
was a fixed rule rejecting a primary subtag longer than three letters. No
such subtag is registered today, but RFC 5646 reserves five to eight letters
for future registration, so the rule would reject valid tags if one were
registered. It would also contradict the sentence beside it, that a validator
MUST NOT reject a subtag missing from the registry.

The text now says that well-formed means the §2.1 grammar, and a scenario
records that `english` passes. A validator with the registry may warn.

### An unregistered `rel` warns

"Registered" cannot be checked without a copy of the registry, and copies
differ by date. Under the draft, an episode using a relation registered last
month is invalid to an older validator and valid to a newer one, while every
reader must accept it.

The line between valid and invalid moves to something the text alone
decides: the form of the value. RFC 8288 gives a registered relation type the
form `LOALPHA *( LOALPHA / DIGIT / "." / "-" )`. A `rel` of that form, or an
absolute URI, is valid. A `rel` of that form that a validator's copy lacks
gets a warning.

Writers are still held to the registry. A writer MUST NOT write an
unregistered `rel`, so a typo such as `predecesor-version` is refused when it
is written, which is when it can be fixed.

### A new capability for the comparison

No existing capability covers how lists are ordered. `canonical-form` holds
the comparison and the `participants` rule. The `links` sort stays in
`episode-links` and names the comparison.

## Risks / Trade-offs

- **A typo in `rel` in a hand-written file is now a warning.** Writers refuse
  it, and a validator still reports it. → The warning names the link.
- **Checking a critical zone needs time zone data.** A writer without it
  refuses every critical zone. → That is safe: it writes nothing wrong, and
  the caller can resend the value without the flag.
- **A writer's zone data may be older than the value's.** An offset that is
  correct under new rules would be refused under old ones. → Only with the
  critical flag, which few sources write.
- **Existing workspaces may hold unsorted `participants`.** → They stay
  valid. Episodes are not rewritten, so the old order remains.

## Migration Plan

Nothing in a workspace changes. Three behaviours in episodes-cli change, each
to be raised as an issue there once this is merged: `record` drops an
elective suffix where it refused, `validate` warns on an unregistered `rel`
where it reported an error, and the language check stops rejecting long
primary subtags.

## Open Questions

None.
