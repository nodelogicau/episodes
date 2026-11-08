## Why

Four open issues (#3, #4, #9, #10) are the same mistake from different angles: treating a plan, or the absence of a record, as evidence of what happened. The draft lets an episode be written before its happening, lets `occurred` be copied from a scheduled time, treats a calendar event's start as when something happened, and says nothing about what a gap in the record means. Episodes are accumulation-only, so each of these mistakes leaves a permanent false record.

## What Changes

- **#3: Nothing is recorded ahead of time.** An episode MUST NOT be recorded before its `occurred.start`. If `occurred.end` is given, it MUST NOT be later than the recording instant. `occurred` MUST come from the happening (observed, stated by a source about the happening, or inferred) and never be copied from a plan. A validator warns where `occurred` is later than `timestamp`.
- **#4: A calendar event records an arrangement.** **BREAKING** (draft semantics). A reference episode to a calendar event records that the event was arranged. Its `occurred` is when the arrangement was made (the event's creation time, `basis: stated`), not the scheduled time; the scheduled time stays in the referenced content. Change `basis`'s `stated` example from "a calendar event's start" to the event's creation time. Add an informative note: a calendar hold written from a plan is a trace of that plan, and a claim that a meeting took place needs evidence other than the calendar.
- **#9: A workspace is not exhaustive.** State normatively that a missing episode is not evidence that something did not happen, and that a consumer MUST NOT treat it as non-occurrence.
- **#10: What `fulfilled` means for episodes.** Informative text in Relation to other formats: an intention retired as `fulfilled` is the person letting it go, not evidence that it was done, and it need not agree with what claims make of the episodes.

## Capabilities

### New Capabilities
- `episode-evidence`: what an episode attests to and what it does not. Episodes record only what has happened, at the time it happened; a calendar episode records an arrangement; the absence of an episode means nothing.

### Modified Capabilities
<!-- None. `standalone-conformance` is unchanged: every intentions/DKF mention this change adds is informative. -->

## Impact

- `README.md` only. Affected sections: `occurred` (rules and `basis`), `content` or a new note on calendar events, Core Object Types (a new completeness subsection), Relation to other formats, When an episode is recorded, Status.
- Recording on demand no longer allows a reference episode for a future meeting dated at the meeting. It records the arrangement instead. A harness that wants evidence a meeting took place records something else: a turn, a note, or attendance data.
- The `standalone-conformance` requirements must still hold. New references to intentions or DKF are informative only.
- Once implemented, issues #3, #4, #9 and #10 can be closed.
