## Context

`README.md` is the specification, and it now stands alone (see `openspec/specs/standalone-conformance`). Several of its passages let a plan pass for something that happened:

- `basis: stated` gives "a calendar event's start" as its example. That is a scheduled time, not an observed one.
- Nothing stops a writer from recording an episode before its `occurred.start`. Episodes cannot be revised, so recording a meeting that is then cancelled leaves a false record permanently.
- Recording referenced content on demand, together with the freedom to drop uncited episodes, means a workspace is sparse by design. The draft never says so, so the obvious reading ("no episode means it didn't happen") is unchecked.
- Issue #10's question about intentions' `retired: fulfilled` belongs to the relation between formats, which is now informative.

## Goals / Non-Goals

**Goals:**
- No conformant writer can produce an episode that asserts something happened before it did.
- A calendar episode has a meaning that is true at the moment it is recorded.
- Readers and consumers are told what a gap in the record does and does not mean.
- The family-level reading of `fulfilled` is stated, informatively.

**Non-Goals:**
- Recording acts that left no record (#2). That is a separate change.
- Any requirement involving intentions or DKF data. Standalone conformance must still hold.
- Changing the DKF or intentions READMEs. The intentions draft paragraph on `fulfilled` is cited, not edited.

## Decisions

**1. Recording time bounds `occurred`, with a writer MUST and a validator warning.**
Writers MUST NOT record an episode before `occurred.start`, and MUST NOT state an `occurred.end` later than the recording instant. Either would describe something that has not happened yet. A validator converts `occurred` to an instant using `tz` and compares it with `timestamp`. A date-only `occurred` is compared as a date. The validator **warns** rather than fails, because a writer's clock and the source of a `stated` time can each be off by minutes. This follows the existing rule for future ids, which warns on anything later than now.
Alternative: fail. Rejected, because the validator cannot tell clock skew from a real violation, and a hard failure on skew would teach people to ignore the check.
Consequence: a conversation container recorded at its first turn carries no `end`, and since episodes cannot be revised it cannot gain one later. The end of a conversation can be read from its last turn. Whether a container should say more is noted in Status.

**2. A calendar episode records the arrangement, not the meeting.**
Three options were considered:
- (a) `occurred` is when the event was created. The episode says "this was arranged". It is true when recorded, can be recorded at any time after creation, and is compatible with decision 1.
- (b) `occurred` is the scheduled time, and readers are told not to trust it. This collides with decision 1: a future meeting could not be recorded until it starts, and once it starts the episode still doesn't show it happened.
- (c) Forbid calendar episodes. Too blunt, since an arrangement is itself something that happened and a claim may cite it.

**Chosen: (a).** The scheduled time stays where it lives, in the referenced event. The episode's `label` may carry the title as captured. The general rule behind it is that a reference episode records the happening its source witnesses. For mail, that is the sending. For a calendar, it is the arranging. `basis` is unchanged; its `stated` example becomes "a calendar event's creation time".

**3. The completeness statement is normative and goes in Core Object Types.**
A short subsection, "What a workspace does not say", states that a workspace is not exhaustive, and that a reader or consumer MUST NOT treat the absence of an episode as evidence that something did not happen. It sits in a normative section because it constrains readers. Every format-neutral consumer, not only a DKF one, has to obey it. The "When an episode is recorded" section (informative) gets a cross-reference.

**4. `fulfilled` is informative and short.**
Add a paragraph to Relation to other formats:
- Retiring an intention as `fulfilled` is the person letting it go, not evidence that it was done.
- The retirement's `timestamp` is when it was written, not when anything happened.
- A claim that finds an intention was not really fulfilled conflicts with nothing in either format.
- Whether a retirement should point at an episode is a question for intentions.

## Risks / Trade-offs

- [The calendar decision surprises readers who expect an `event` episode to be the meeting] → State it plainly in the `content` and `basis` text, and give an example contrasting the arrangement with evidence of the meeting.
- [A warning-only validator lets real violations through] → The writer MUST is the main guard. The warning catches harness bugs in review, the same way future ids are caught in pull requests.
- [The two `occurred` rules make it impossible to record a span that is still going on] → Accepted. Record at the start without `end`, or record when it finishes. Status notes containers that cannot later gain an `end`.

## Migration Plan

None. The format is a draft and nothing is deployed.

## Open Questions

- Should a container be allowed an appended, unindexed observation of its `end`, like `source_status`? It is recorded as a Status question, not decided here.
- Should the calendar treatment extend to other sources whose timestamps are plans, such as a task's due date? Probably yes, through the general rule in decision 2. Check while implementing whether the text should name more examples.
