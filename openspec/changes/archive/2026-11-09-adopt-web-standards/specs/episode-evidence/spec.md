## MODIFIED Requirements

### Requirement: Nothing is recorded before it happens
A writer SHALL NOT record an episode whose `occurred.start` is later than its recording instant (`timestamp`). If `occurred.end` is present, it SHALL NOT be later than the recording instant. A date-time SHALL be compared as the instant its offset fixes. A date alone SHALL be compared as a date with the recording instant's date, taken in `tz` where `tz` is present, and otherwise in UTC with one day's allowance. A validator SHALL warn, naming the episode, wherever either bound is violated.

#### Scenario: Recording a meeting before it starts
- **WHEN** a harness at 09:00 tries to record an episode with `occurred.start` 14:00 the same day, in the same zone
- **THEN** a conformant writer refuses to write it

#### Scenario: Recording during a conversation
- **WHEN** a container episode is recorded at its first turn, with `occurred.start` equal to that turn and no `end`
- **THEN** the episode is valid

#### Scenario: An end in the future
- **WHEN** an episode recorded at 10:00 UTC states an `occurred.end` of 11:00 UTC
- **THEN** a validator warns, naming the episode

#### Scenario: The repeated hour
- **WHEN** an episode recorded at `2026-04-04T15:45:00Z` has `start: "2026-04-05T02:30:00+10:00[Australia/Melbourne]"` (16:30 UTC)
- **THEN** a validator warns, because the offset puts the start after the recording, although the first 02:30 (`+11:00`, 15:30 UTC) would not have

#### Scenario: A date alone with no zone
- **WHEN** an episode recorded at `2026-11-07T22:00:00Z` has `start: "2026-11-08"` and no `tz`
- **THEN** a validator does not warn, because the date is within one day of the recording's UTC date
