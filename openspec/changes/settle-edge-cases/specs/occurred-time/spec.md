## ADDED Requirements

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
