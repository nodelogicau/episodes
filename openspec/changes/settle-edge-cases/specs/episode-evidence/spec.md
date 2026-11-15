## MODIFIED Requirements

### Requirement: Nothing is recorded before it happens
A writer SHALL NOT record an episode whose `occurred.start` is later than its recording instant (`timestamp`). If `occurred.end` is present, it SHALL NOT be later than the recording instant. A date-time SHALL be compared as the instant its offset fixes. A date alone SHALL be compared as a date with the recording instant's date, taken in `tz` where `tz` is present, and otherwise in UTC with one day's allowance.

Where `occurred.basis` is `stated`, a date-time SHALL be allowed to be up to five minutes later than the recording instant. A writer MAY record such an episode, and SHALL record the time as the source stated it. The allowance SHALL NOT apply where the basis is `recorded` or `inferred`, and SHALL NOT add to the allowance for a date alone.

A validator SHALL warn, naming the episode, wherever either bound is violated by more than the allowance that applies.

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

#### Scenario: Mail from a clock that runs ahead
- **WHEN** a writer at `2026-11-07T03:24:10Z` records an email whose `Date` header gives `2026-11-07T03:24:40Z`, with `basis: stated`
- **THEN** it may write the episode with `start` as the header gives it, and a validator does not warn

#### Scenario: A stated time beyond the allowance
- **WHEN** an episode with `basis: stated` has a `start` six minutes later than its `timestamp`
- **THEN** a conformant writer refuses to write it, and a validator that meets it warns, naming the episode

#### Scenario: The writer's own clock
- **WHEN** an episode with `basis: recorded` has a `start` thirty seconds later than its `timestamp`
- **THEN** a validator warns, because the allowance covers a source's clock and not the writer's
