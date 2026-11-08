## Why

An implementor should be able to build an episodes store without reading, implementing or deploying DKF or intentions. Today they can't. The draft points at intentions data through `occasion`, takes its hash, redaction and sharding rules from DKF's README by reference ("follows DKF's…", "in every rule this section does not change"), and defines `author` and `standpoint` as references to a DKF *particular*. That contradicts the draft's own principle, "an episodes workspace is useful on its own".

## What Changes

- **BREAKING** Remove `occasion` from `EPISODE`, its section, the field table, the object-model diagram and "How the other formats cite an episode". The link between an episode and an intention becomes something other formats record, such as a DKF claim citing both. Episodes then reference no other format's objects.
- Define what `author`, `standpoint`, `participants` and `place` hold (a URI or an identifier naming a person, agent or place) without relying on DKF's *particular*.
- Restate in full the content hash rule now taken from DKF: SHA-256 over the content with CRLF normalised to LF and nothing else changed, plus the `<algorithm>:<digest>` reading rule.
- Restate in full the redaction rules now inherited from DKF: which absent required fields a redaction makes valid, the single-block rule, irreversibility, non-cascade, and the store caveat.
- Restate in full the sharding and index rules now inherited from DKF: month derivation, `legacy/`, sealing with one month of grace, which changes a sealed month allows, segment `count` and late-merge detection, future-id validation, and the shape of the root index and its segments.
- Add a conformance statement: the format is complete on its own. Text about DKF and intentions is **informative**, describing how those formats may use episodes, and places no requirement on an episodes implementation.
- Keep every mention of the sibling formats that is motivation or example, marked or phrased as informative.

## Capabilities

### New Capabilities
- `standalone-conformance`: the format is implementable from this specification alone. It has no references to other formats' objects, no rules defined by reference to another specification, and an explicit split between normative and informative text.

### Modified Capabilities
<!-- None: openspec/specs/ is empty; the format's normative text lives in README.md. -->

## Impact

- `README.md` is the specification and is the only file that changes. Affected sections: Purpose, Source and timestamp, `EPISODE` (field table, `standpoint`, `content`, `occasion`), Redaction, Object Model, How the other formats cite an episode, File Layout, `index.yaml`, Design Principles, Status.
- Removing `occasion` breaks any draft episode that carries it. No implementation exists, so nothing deployed breaks.
- Open issues #1, #5, #6, #7 and #8 are about `occasion` alone, and this change makes them moot. #3, #4, #9 and #10 contain points that still apply without `occasion` (not recording before something happened; a calendar hold is a trace of a plan; a missing episode is not evidence; what `fulfilled` means). They stay open and are out of scope here.
- The intentions and DKF READMEs may describe `occasion` or depend on it. Updating them is out of scope, but someone should check whether either needs a matching change. In particular, can a DKF claim cite both an episode and an intention?
