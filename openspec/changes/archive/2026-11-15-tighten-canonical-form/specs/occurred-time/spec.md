## MODIFIED Requirements

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
