## 1. Recording time bounds `occurred` (#3)

- [x] 1.1 In `#### occurred`, add the writer rules: no episode before `occurred.start`; no `occurred.end` later than the recording instant; compare in `tz`, with a date-only value compared as a date
- [x] 1.2 Add the rule that `occurred` comes from the happening (`recorded`, `stated` about the happening, or `inferred`) and is never copied from a plan, schedule or placement
- [x] 1.3 Add the validator warning, naming the episode, when either bound is violated, with the reason it warns rather than fails (clock skew), matching the future-id rule

## 2. A calendar episode records an arrangement (#4)

- [x] 2.1 Change the `basis: stated` example from "a calendar event's start" to "a calendar event's creation time"
- [x] 2.2 Add the general rule to `#### content` (reference mode): a reference episode records the happening its source witnesses (mail: the sending; a calendar: the arranging), with a calendar example whose `occurred` is the creation time and whose scheduled time stays in the referenced content
- [x] 2.3 Check the `standpoint` paragraph ("A calendar event is the record of the person whose calendar holds it") and the `source_status` table still read correctly
- [x] 2.4 Add an informative note to Relation to other formats: a calendar hold written from a plan is a trace of the plan, and a claim that a meeting took place needs other evidence

## 3. A workspace is not exhaustive (#9)

- [x] 3.1 Add `### What a workspace does not say` to Core Object Types: a workspace is not exhaustive, and a reader or consumer MUST NOT treat a missing episode as evidence that something did not happen
- [x] 3.2 Cross-reference it from When an episode is recorded

## 4. Fulfilment (#10)

- [x] 4.1 Add an informative paragraph to Relation to other formats: `retired: fulfilled` is letting the intention go, not evidence; its `timestamp` is when it was written; a disagreeing claim conflicts with nothing; whether a retirement may point at an episode is a question for intentions

## 5. Verify

- [x] 5.1 Check against `openspec/specs/standalone-conformance`: every new mention of intentions or DKF is informative or says only what an episode does not hold
- [x] 5.2 Check that the `EPISODE` example and the index example still satisfy the new `occurred` rules
- [x] 5.3 Add a Status open question on whether a container may gain an appended observation of its `end`
- [x] 5.4 Run `openspec validate record-happenings-not-plans`
