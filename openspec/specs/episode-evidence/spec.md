# episode-evidence Specification

## Purpose

What an episode attests to and what it does not: episodes record only what has already happened, timed from the happening rather than a plan; a calendar episode records an arrangement; and the absence of an episode is not evidence. Introduced by change `record-happenings-not-plans`.

## Requirements

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

### Requirement: `occurred` comes from the happening
A writer SHALL take `occurred` from the happening the episode records: observed as it happened (`recorded`), stated by a source as the time of that happening (`stated`), or worked out from evidence (`inferred`). A writer SHALL NOT copy `occurred` from a plan, schedule or placement.

#### Scenario: A time copied from a schedule
- **WHEN** a harness records that a planned session took place and copies its `occurred` from the time that was planned
- **THEN** the writer is non-conformant

#### Scenario: A time given by the person
- **WHEN** the person says "I finished it at four" and the harness records an episode with `occurred.start` 16:00 and `basis: inferred`
- **THEN** the episode is conformant

### Requirement: A calendar episode records the arrangement
A reference episode whose content is a calendar event SHALL record that the event was arranged. Its `occurred` SHALL be when the arrangement was made, as stated by the source (`basis: stated`). It SHALL NOT be the event's scheduled time. The scheduled time remains in the referenced content.

#### Scenario: Recording a future meeting on demand
- **WHEN** a claim cites a calendar event for next Tuesday, created yesterday, and the harness records a reference episode for it
- **THEN** the episode's `occurred.start` is yesterday's creation time and the episode is valid today

#### Scenario: The calendar as evidence that the meeting took place
- **WHEN** a consumer reads a calendar episode
- **THEN** the specification has told it that the episode attests that the event was arranged, not that it took place

### Requirement: The absence of an episode is not evidence
The specification SHALL state normatively that a workspace is not an exhaustive record. A reader or consumer SHALL NOT treat the absence of an episode as evidence that something did not happen.

#### Scenario: A gap in the record
- **WHEN** a consumer finds no episode in a period in which something was planned
- **THEN** it does not conclude that the planned thing did not happen

### Requirement: Fulfilment is described informatively
The Relation to other formats section SHALL say, informatively, that an intention retired as `fulfilled` records the person letting the intention go. It is not evidence that the intention was done, and it need not agree with claims citing episodes. No requirement on an episodes implementation SHALL depend on intentions data.

#### Scenario: A retirement and a claim disagree
- **WHEN** an intention is retired as `fulfilled` and a DKF claim citing episodes says it was not done
- **THEN** nothing in the episodes specification treats either as invalid

#### Scenario: Standalone conformance still holds
- **WHEN** an implementor builds episodes from the normative sections only
- **THEN** none of this change's requirements needs DKF or intentions data
