# occurred-time Specification

## Purpose

The grammar of `occurred.start` and `occurred.end`: RFC 9557 date-times with a required offset and an optional bracketed IANA zone, a date alone with an optional `tz`, no other suffixes, and quoted values. Introduced by change `adopt-web-standards`.
## Requirements
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

A writer given a value to record that carries suffixes it may not write SHALL act as follows:

- An elective suffix other than the time zone SHALL be dropped, and the rest of the value recorded.
- A value with a critical suffix other than the time zone SHALL be refused.
- A critical flag on the time zone SHALL be honoured by checking the offset against the zone's rules at that local time. When they agree, the writer SHALL record the value without the flag. When they disagree, or the writer does not know the zone, the writer SHALL refuse the value.

#### Scenario: Inconsistent offset and zone
- **WHEN** an episode's `start` is `"2026-01-15T10:00:00+10:00[Australia/Melbourne]"`, where the zone's offset at that time is `+11:00`
- **THEN** a validator warns, naming the episode, and readers take the instant from `+10:00`

#### Scenario: An elective calendar tag
- **WHEN** a reader meets `"2026-11-07T14:24:00+11:00[Australia/Melbourne][u-ca=gregory]"`
- **THEN** it ignores the `u-ca` tag and reads the instant and zone

#### Scenario: A writer given an elective calendar tag
- **WHEN** a writer is given `2026-11-07T14:24:00+11:00[Australia/Melbourne][u-ca=gregory]` to record
- **THEN** it writes `start: "2026-11-07T14:24:00+11:00[Australia/Melbourne]"`

#### Scenario: A writer given a critical calendar tag
- **WHEN** a writer is given `2026-11-07T14:24:00+11:00[Australia/Melbourne][!u-ca=hebrew]` to record
- **THEN** it refuses, naming the suffix, and writes nothing

#### Scenario: A critical zone that agrees with the offset
- **WHEN** a writer is given `2026-11-07T14:24:00+11:00[!Australia/Melbourne]` to record, and the zone's offset at that time is `+11:00`
- **THEN** it writes `start: "2026-11-07T14:24:00+11:00[Australia/Melbourne]"`

#### Scenario: A critical zone that disagrees with the offset
- **WHEN** a writer is given `2026-01-15T10:00:00+10:00[!Australia/Melbourne]` to record, where the zone's offset at that time is `+11:00`
- **THEN** it refuses, naming the disagreement, and writes nothing

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

### Requirement: The zone of a `recorded` time comes from the recording
The zone written with a `recorded` time SHALL be the zone in which the recording was made. A writer SHALL take it from the first of these that it has:

- the value it is given to record, when that value carries a zone;
- the device at which the person took part, as that device reports its zone at the time;
- `defaults.zone` in `episodes.yaml`.

A writer that has none of these SHALL write the offset alone. A writer SHALL NOT take the zone of a `recorded` time from anything else, including where the person lives or what the person has said about where they are.

`defaults.zone` SHALL be an optional key of `episodes.yaml` holding one IANA time zone name. It SHALL be read by writers only. A writer SHALL NOT apply it to a time whose basis is `stated` or `inferred`, and SHALL NOT apply it to a date alone.

#### Scenario: A zone in the value
- **WHEN** a writer is given `2026-11-07T14:24:00+11:00[Australia/Melbourne]` to record with `basis: recorded`, and `defaults.zone` is `Australia/Sydney`
- **THEN** it writes the value as given, with `Australia/Melbourne`

#### Scenario: A zone from the device
- **WHEN** a harness records a turn at the instant `2026-11-07T03:24:00Z`, and the device the person is typing on reports its zone as `Australia/Melbourne`
- **THEN** it writes `start: "2026-11-07T14:24:00+11:00[Australia/Melbourne]"`

#### Scenario: A zone from the default
- **WHEN** a writer is given `2026-11-07T14:24:00+11:00` to record with `basis: recorded`, has no zone from a device, and `defaults.zone` is `Australia/Melbourne`
- **THEN** it writes `start: "2026-11-07T14:24:00+11:00[Australia/Melbourne]"`

#### Scenario: No source for the zone
- **WHEN** a writer is given `2026-11-07T14:24:00+11:00` to record with `basis: recorded`, has no zone from a device, and `episodes.yaml` has no `defaults.zone`
- **THEN** it writes `start: "2026-11-07T14:24:00+11:00"`

#### Scenario: A stated time and a default zone
- **WHEN** a writer records an email whose `Date` header gives `+1100`, with `basis: stated`, and `defaults.zone` is `Australia/Melbourne`
- **THEN** it writes the offset alone

#### Scenario: What the person said
- **WHEN** the person has said in conversation that they live in Melbourne, and the writer has no zone from the value, the device or `defaults.zone`
- **THEN** it writes the offset alone

### Requirement: A writer does not write a zone that contradicts the offset
A writer SHALL NOT write a zone suffix whose offset, under the zone's rules at that instant, differs from the numeric offset it writes. It SHALL write the offset alone, unless the zone carries a critical flag, in which case it refuses the value. This SHALL hold whichever source the zone came from. A writer that does not have the rules of a zone cannot make the check, and SHALL leave that zone out.

A value written with `Z` gives no local offset and contradicts no zone. A writer that has a zone from the device and an instant with no local offset SHOULD write the local time, with the offset the zone gives at that instant. A writer SHALL NOT apply `defaults.zone` to a value that has no local offset.

#### Scenario: A default zone while travelling
- **WHEN** a writer is given `2026-11-07T12:24:00+09:00` to record with `basis: recorded`, and `defaults.zone` is `Australia/Melbourne`, whose offset at that instant is `+11:00`
- **THEN** it writes `start: "2026-11-07T12:24:00+09:00"`, with no zone

#### Scenario: A zone in the value that contradicts its offset
- **WHEN** a writer is given `2026-01-15T10:00:00+10:00[Australia/Melbourne]` to record, where the zone's offset at that time is `+11:00`
- **THEN** it writes `start: "2026-01-15T10:00:00+10:00"`, with no zone

#### Scenario: Two zones with one offset
- **WHEN** a writer is given `2026-07-07T14:24:00+10:00` to record with `basis: recorded` by a person in Brisbane, and `defaults.zone` is `Australia/Melbourne`, whose offset at that instant is also `+10:00`
- **THEN** it writes `[Australia/Melbourne]`, and is conformant, because the check compares offsets and cannot tell the two zones apart

#### Scenario: An instant with no local offset
- **WHEN** a writer is given `2026-11-07T03:24:00Z` to record with `basis: recorded`, has no zone from a device, and `defaults.zone` is `Australia/Melbourne`
- **THEN** it writes `start: "2026-11-07T03:24:00Z"`, with no zone

#### Scenario: A zone the writer has no rules for
- **WHEN** a writer is given a value whose zone suffix names a zone that is not in the writer's time zone data, with no critical flag
- **THEN** it writes the value with the offset alone
