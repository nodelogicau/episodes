## ADDED Requirements

### Requirement: Sorted strings are compared by Unicode code point
Wherever the specification requires a writer to sort strings, the writer SHALL compare them by Unicode code point, as written, with a string that is a prefix of another coming first. The specification SHALL state this once, and SHALL state that the order is that of the strings' UTF-8 bytes and is not the order of their UTF-16 code units.

#### Scenario: A character outside the Basic Multilingual Plane
- **WHEN** a writer sorts two references that differ first at U+FF5E in one and U+1F600 in the other
- **THEN** it writes the one with U+FF5E first, although a UTF-16 comparison would put it second

#### Scenario: Upper case before lower case
- **WHEN** a writer sorts `https://Example.com/a` and `https://example.com/a`
- **THEN** it writes `https://Example.com/a` first, because `E` is U+0045 and `e` is U+0065

### Requirement: `participants` is sorted, with exact duplicates removed
A writer SHALL write `participants` sorted by the code point comparison, and SHALL write each value once. Values SHALL be compared as written: a writer SHALL NOT normalise a reference, as a URI or otherwise, in order to compare or to remove it. A reader SHALL accept `participants` in any order and with repeated values. A validator MAY warn on `participants` that is unsorted or repeats a value, and SHALL NOT reject an episode for it.

#### Scenario: The example episode
- **WHEN** a writer records a turn whose participants are `https://github.com/benfortuna` and `https://claude.ai`
- **THEN** it writes `https://claude.ai` first

#### Scenario: A participant given twice
- **WHEN** a writer is given `https://claude.ai` twice among an episode's participants
- **THEN** it writes the value once

#### Scenario: Two spellings of one URI
- **WHEN** a writer is given `https://example.com/a` and `https://example.com/a/` among an episode's participants
- **THEN** it writes both, as given, in code point order

#### Scenario: An unsorted file
- **WHEN** a validator reads an episode whose `participants` are valid references in an order other than code point order
- **THEN** the episode is valid, and the validator may warn
