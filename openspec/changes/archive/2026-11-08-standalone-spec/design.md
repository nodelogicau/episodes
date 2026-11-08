## Context

The specification is `README.md`. It currently depends on its two sibling formats in two ways:

- **Data.** `occasion: {id, version}` names an intentions object. To write it correctly you need intentions' version semantics (issue #7). To check it you need an intentions workspace.
- **Spec text.** Three rules are defined by pointing at DKF's README:
  - `hash` "follows DKF's definition";
  - Redaction "follows DKF's redaction in shape and in every rule this section does not change";
  - the layout "follows DKF's sharding", which brings in sealing, segment counts, late merges, future-id validation, `legacy/` and the shape of the index.

  `author` and `standpoint` are also defined as references to "a particular", which is a DKF object type.

The other mentions of DKF and intentions are motivation (the Problem, Purpose and Approach sections), examples (the DKF citation), or definitions by exclusion ("each of those is a DKF claim"). None of them asks an implementor to do anything.

The rules being restated were read from DKF's README (`nodelogicau/particulars`, sections *Verifiable documents*, *Redaction*, *Sharding* and *`index.yaml`*) as of 2026-11-08.

## Goals / Non-Goals

**Goals:**
- A reader can implement a conformant episodes writer, reader and validator from `README.md` alone.
- No episode field holds an identifier whose meaning is defined by another format.
- Every MUST, SHOULD and MAY in the document stands on its own text.
- The family framing (the three kinds of memory, citation by DKF claims) stays, clearly labelled as informative.

**Non-Goals:**
- Resolving the other open issues (#2, #3, #4, #9, #10). Only the parts tied solely to `occasion` go away.
- Changing the DKF or intentions READMEs.
- Extracting a shared "provenance spine" specification. That remains an open question in Status.
- Changing any rule's meaning while restating it, apart from adapting it to episodes (for example, there are no retractions here).

## Decisions

**1. Remove `occasion` rather than generalise it.**
Alternatives:
- (a) Keep it, but as an opaque URI with no stated semantics. That still implies "this episode is related to that intention", and #1 shows that which episode belongs to which intention is a judgement.
- (b) Replace it with a generic `related: [ref]`. That's an interpretive field under another name.
- **Chosen:** the link becomes another format's business, typically a DKF claim citing the episode and the intention. Episodes become a leaf: cited, citing nothing. The loop-closing paragraph moves to the informative section and says the loop closes in claims.

**2. Restate rules inline, not by reference to a third document.**
Alternative: extract the shared rules (hash, redaction shape, sharding) into a common spec that all three formats cite. That would swap a dependency on DKF for a dependency on a third document, against the goal. It also needs the other formats' agreement. Inline restatement duplicates text across the family, and that risk is handled below. The README may still say informatively that a rule matches DKF's, so readers who know DKF recognise it.

**3. Identify people, agents and places by URI or identifier, not by "particular".**
`author`, `standpoint`, `participants` and `place` hold a URI where one is known, otherwise a string identifier. Resolving one is outside the format, and a value that can't be resolved is still valid. That's what the draft already means. It just no longer leans on DKF's object model to say so. An informative note can add that a DKF workspace may treat these values as particulars.

**4. Mark informative text with a Conformance section, not per paragraph.**
Add a short **Conformance** section. Its normative content is *Core Object Types* and *File Layout*, together with the key words (RFC 2119/8174). Everything else is informative, including Problem, Purpose, Approach, Object Model, Relation to other formats, Design Principles and Status. Rename "How the other formats cite an episode" to **Relation to other formats** and make it explicitly informative. Alternative: tag every paragraph. That's noisy, and the current structure already separates motivation from rules well.

**5. Adapt the sharding and index rules to episodes when restating them.**
Episodes have one object type, no retractions and no particulars. So:
- The root index holds `format`, `segments` (each with `path` and `count`) and `entries`. It has no `retracted` list and no type directories beyond `episodes/`.
- A sealed month allows exactly two changes: rewriting `source_status`, and gaining or extending a `redacted` block.
- Late merges are detected by segment `count`, and the fix is to re-mint before merging.
- A validator warns on an id from later than now, and fails on an id two or more months ahead.
- Month derivation, the one-month grace period and the `legacy/` rules carry over unchanged.

**6. Adapt the redaction rules the same way.**
A required field becomes valid when absent only because a `redacted` block lists it. For episodes those fields are `content.text` (inline) and `content.ref` (reference). DKF's `restates_redacted` finding is left out: no episode restates another's text, and the effect on citing claims is already covered as "becomes unverifiable".

## Risks / Trade-offs

- [Restated rules drift from DKF's over time] → An informative "matches DKF's rule at the time of writing" note on each restated rule. Drift is then visible but not binding. The provenance-spine open question already tracks unifying them.
- [Losing `occasion` makes "what did I do against what I meant" harder to answer] → The query moves to DKF claims, which is where the judgement already lives. Issue #9's warning (a missing episode is not evidence) stays open for the text that remains.
- [The restatement accidentally changes a rule's meaning] → Tasks include a side-by-side check of each restated rule against DKF's text.
- [The README grows] → Accepted. Self-containment costs length. The sharding restatement is the biggest addition.

## Migration Plan

None needed. The format is a draft (`episodes/0.1` isn't declared) and no implementation exists. A draft file that carries `occasion` is treated like any field an implementation added: readers ignore it and give it no meaning.

## Open Questions

- Should the intentions or DKF READMEs drop or change text that relies on `occasion`? In particular, can a DKF claim cite both an episode and an intention? This needs checking in those repos, outside this change.
- After merge, should issues #1, #5, #6, #7 and #8 be closed with a pointer to this change? That needs the maintainer's approval.
