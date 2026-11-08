## ADDED Requirements

### Requirement: `occurred` date-times are RFC 9557 values
A date-time in `occurred.start` or `occurred.end` SHALL be an RFC 3339 `date-time` with a numeric offset or `Z`, optionally followed by one RFC 9557 time-zone suffix holding an IANA time zone name. The offset SHALL fix the instant. A writer SHALL write the zone suffix whenever the zone is known. When the source gives only an offset, the writer SHALL write the offset alone and SHALL NOT guess a zone.

#### Scenario: A conversation turn
- **WHEN** a harness in Melbourne records a turn spoken at 14:24 local time on 2026-11-07
- **THEN** it writes `start: "2026-11-07T14:24:00+11:00[Australia/Melbourne]"`

#### Scenario: The repeated hour
- **WHEN** an episode occurred at the second 02:30 in Melbourne on 2026-04-05, after clocks went back
- **THEN** its `start` is `"2026-04-05T02:30:00+10:00[Australia/Melbourne]"`, and it is distinguishable from the first 02:30, which is `+11:00`

#### Scenario: A mail header with an offset only
- **WHEN** an email's `Date` header is `Sat, 7 Nov 2026 14:24:00 +1100`
- **THEN** the writer records `start: "2026-11-07T14:24:00+11:00"` with no zone suffix, and the episode is valid

### Requirement: No critical flag and no other suffixes
A writer SHALL NOT write the RFC 9557 critical flag (`!`) or any suffix other than the time zone. A reader SHALL ignore elective suffix tags it does not implement. When the offset disagrees with the zone's rules at that local time, the offset SHALL govern, and a validator SHALL warn, naming the episode. A reader SHALL treat a critical suffix it cannot honour as making the episode invalid.

#### Scenario: Inconsistent offset and zone
- **WHEN** an episode's `start` is `"2026-01-15T10:00:00+10:00[Australia/Melbourne]"`, where the zone's offset at that time is `+11:00`
- **THEN** a validator warns, naming the episode, and readers take the instant from `+10:00`

#### Scenario: An elective calendar tag
- **WHEN** a reader meets `"2026-11-07T14:24:00+11:00[Australia/Melbourne][u-ca=gregory]"`
- **THEN** it ignores the `u-ca` tag and reads the instant and zone

### Requirement: A date alone stays valid, with an optional `tz`
`occurred.start` and `occurred.end` SHALL each be either a date (`YYYY-MM-DD`) or a date-time, and both SHALL take the same form. `occurred.tz`, an IANA zone name, SHALL be permitted only when `start` is a date. A writer SHALL NOT write `tz` beside a date-time.

#### Scenario: An inferred date
- **WHEN** a note written today says "last Tuesday" and the harness infers the date
- **THEN** it may write `start: "2026-11-03"`, `tz: Australia/Melbourne`, `basis: inferred`

#### Scenario: `tz` beside a date-time
- **WHEN** an episode has `start: "2026-11-07T14:24:00+11:00"` and `tz: Australia/Melbourne`
- **THEN** a validator rejects it, naming the field

#### Scenario: Mixed forms
- **WHEN** `start` is a date and `end` is a date-time
- **THEN** a validator rejects the episode

### Requirement: `occurred` values are quoted strings
A writer SHALL write `occurred.start` and `occurred.end` as double-quoted YAML strings, in episode files and in the index alike.

#### Scenario: The index in flow style
- **WHEN** an index entry writes `occurred: {start: "2026-11-07T14:24:00+11:00[Australia/Melbourne]", basis: recorded}`
- **THEN** a YAML parser reads `start` as a single string, with the brackets intact
