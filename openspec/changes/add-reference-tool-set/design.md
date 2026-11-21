## Context

The format says what an episode is, how a workspace is laid out, and how a
free-text query is answered. It names no operations. episodes-cli v0.2.0 has
thirteen verbs and no MCP server.

The sibling formats each name a tool set, in different ways:

```
              particulars                intentions                 episodes (this change)
section       MCP Server Tools           Reference Tool Set         Reference Tool Set
names are     the interface              a reference; a listed      a reference; a listed
                                         name keeps its semantics   name keeps its semantics
written       ahead of a binary          from intentions-cli        ahead of a binary,
                                         v0.11.0, verified          from the v0.2.0 verbs
transport     MCP                        MCP                        none named normatively
```

The episodes Conformance section says that only *Core Object Types* and *File
Layout* are normative, and that "every other section is informative".
`standalone-conformance` requires the document to stand without any other
specification.

Four writer rules can't be checked by a validator, and a tool call is the
likeliest place for each to break:
- self-attestation only on an explicit request;
- `via` whenever the attestation was recorded;
- recording is parsing;
- nothing is recorded before it happens.

## Goals / Non-Goals

**Goals:**

- A skill or prompt written against one implementation's tools works against
  another's.
- A model calling the tools cannot do what the writer rules forbid:
  - record an act no turn attests;
  - record an act on someone else's behalf;
  - backdate or postdate when a record was made.
- The set follows the CLI verbs closely, so a tool is easy to implement as
  the verb, and a tool's result is the verb's `--json` output.
- The format still stands alone.

**Non-Goals:**

- Requiring any implementation to expose tools.
- Requiring MCP, or defining a wire format, tool annotations or a manifest.
- Bulk and maintenance operations: `import`, `index`, `init`,
  `workspace pointer`, `version`.
- Settling whether a harness may attest its own acts. That stays open in
  *Status*.
- A skill or prompt text. That is the implementation's to write, as
  particulars-cli and intentions-cli write theirs.

## Decisions

### The names are a reference, and a listed name is binding

The set takes intentions' standing. An implementation MAY use other names.
One that exposes a listed name SHALL keep its semantics and accept its
parameters as stated.

- **Alternatives:**
  - *Names are the interface*, as in particulars. This forces every
    implementation to use these names. That is more than a draft format
    should ask.
  - *A wholly informative section.* Nothing would hold a tool called
    `act_attest` to the rules that make it safe, and the section would fail
    at its one purpose.
- **Consequence for Conformance:** the section becomes normative, and it
  binds only an implementation that exposes a listed name. Conformance gets
  one sentence saying so. An implementation with no tools still conforms on
  the two existing normative sections alone.

### Transport-neutral, with MCP informative

The normative text says "tool", "parameter" and "result". MCP, resource
templates and annotations such as `destructiveHint` appear only in
informative notes. This keeps `standalone-conformance` true without
modifying it: no rule is defined by reference to MCP.

The rule for `episode_redact` is stated by its effect: irreversible, never
cascading, and its result naming what was removed and that history may hold
it. It is not stated as an annotation.

### Written ahead of the binary

Intentions verified its set against a release. Here there is no server to
verify against, and the rules that matter are format decisions, not
implementation details: dropping `control` over a tool call, binding the
author and the clock, and the capture rule. The set is therefore drawn from
the v0.2.0 verbs and flags, and episodes-cli is asked, in an issue, to
implement `serve --mcp` against it.

*Status* notes that no implementation exposes the set yet. A later change
can record the version that does.

### `act_attest` requires `via`, and has no `control` parameter

The format keeps both cases:
- an act linked `via` the episode that attests it;
- an act logged from a dedicated control, with no link.

The tool offers only the first.

- **Why:** a tool call comes from a model. "This came from a dedicated
  control" is then a statement about a UI the model doesn't own, and it is
  exactly the inference the self-attestation rule forbids. A real control,
  such as a "log my run" button, calls the implementation directly: the CLI's
  `act --control`, or a connector. It never goes through a model.
- **`via` must resolve at write time.** It names an episode that is in the
  workspace now and whose `standpoint` equals the act's. The format accepts
  an unresolved `via` when reading, because an attesting turn can later be
  redacted or dropped. When writing, though, the attestation must already
  have been recorded, because the writer MUST record it.
- **Alternatives:**
  - *Keep `control` as the caller's statement*, as the CLI does. Over a tool
    call no human is "the caller", so this was rejected.
  - *Leave acts out of the set.* Recording "log ninety minutes from nine" on
    the person's request is a common case, and the turn that asks is exactly
    what `via` exists for, so this was rejected too.

### The author, the harness and the clock are bound; the model may be passed

- **`source.author` and `source.harness`** come from the implementation's
  configuration when it starts: the CLI's `--author` and `--harness`, the
  environment, then the workspace's `defaults`. No tool accepts them.
  - **Why:** an act's `standpoint` is its `source.author`. A per-call author
    would let a model attest an act on anyone's behalf.
- **`source.model` MAY be passed.** The implementation can't otherwise know
  which model is calling, and a wrong value misattributes the recording, not
  the act.
- **No tool accepts a value standing for now.** `source.timestamp`, the
  instant an id is minted, and any `occurred` defaulted to now all come from
  the implementation's clock. The CLI's `--now` stays a test-facing flag of
  the binary.
  - `occurred` itself is still passed, with `basis`, because when something
    happened is the caller's to state.
- **Alternative:** a `source` parameter, as intentions has. Intentions has no
  act whose subject is its author, so the risk doesn't arise there.

### A conversation is captured from the harness's transcript

- The rule is a **SHOULD**: a harness records turns from its own transcript,
  through a hook or a connector, and not by having a model call
  `conversation_turn`. An implementation MAY leave `conversation_start` and
  `conversation_turn` out of what it lists to a model.
- **Why the tools stay in the set:**
  - A harness that has no hook still needs a way in.
  - A connector built on the tools should get the same semantics as one
    built on the CLI.
- **Why a SHOULD, not a MUST:** nothing can tell a turn written from a
  transcript from one re-typed by a model, so a MUST would be unverifiable.
  It sits beside the self-attestation rules as a rule for writers.
- **Alternatives:**
  - *Drop the two tools.* This leaves hookless harnesses with nothing, and
    connectors with no shared semantics.
  - *Say nothing.* This invites the common failure: a model summarising what
    the person said, and calling that a turn.

### `standpoint` isn't restricted beyond the format

The tools accept any `standpoint` the format accepts. Recording Jane's email
needs `standpoint: Jane`, written by a harness acting for Ben. Restricting
`standpoint` to the bound author, or to a container's participants, would
forbid what the format is for.

The guards against misattribution are:
- the bound author, which fixes the standpoint of every act;
- the capture rule;
- review through git.

### Parameters follow the flags

- Each tool takes its verb's flags, in snake case.
- Repeatable flags become lists: `participants`, `links` (each `{rel,
  href}`), `mementos` and `fields`.
- `text` is passed as a value. There is no `text_file`.
- **`hash_file` and `content_file` stay as paths the implementation reads.**
  - The bytes they cover, such as a complete `message/rfc822` message, must
    be exact. A value passed through a model's JSON output is not a reliable
    carrier of exact bytes.
  - A remote implementation that can't read the caller's files simply
    doesn't offer them, and takes `hash` and `state` instead.
- A tool's result is the verb's `--json` output, and every refusal the verb
  makes, the tool makes.

### Resource templates are informative, and episodes are not immutable

An episode is never revised, but its file still changes in two ways:
- `observe` rewrites `source_status`;
- `redact` removes fields and records the redaction.

So `episode://{id}` is not cacheable forever. The informative note says:
- the templates are local to the server, and the scheme is never written
  into an episode, whose links use ids;
- a server that takes subscriptions notifies subscribers on `observe` and
  `redact`;
- a client keeps no copy of text after a redaction removes it. This is the
  rule `redaction-completeness` already states for every derived value.

## Risks / Trade-offs

- **The set is written ahead of a binary, and an implementation may find a
  parameter that doesn't fit.** → The episodes-cli issue asks for findings to
  go in its SPEC-FEEDBACK file, as happened for the format itself, and a
  follow-up change records the verified version.
- **A harness with a shell can call `episodes act --control` and get around
  `act_attest`.** → The rule binds the tool, and the format's own rule still
  binds the writer. A skill an implementation ships should say the same
  thing. This change doesn't try to constrain shells.
- **The capture rule is unenforceable.** → It is a SHOULD, labelled as a rule
  for writers, the same standing as the self-attestation rules.
- **Copies can drift.** The tool names follow the siblings' pattern
  (`object_verb`), but the rules are restated here, not shared. → *Status*
  already carries the provenance-spine question. A shared tool vocabulary
  would be part of it.

## Open Questions

- Should `conversation_turn` refuse a turn whose `standpoint` is neither the
  container's standpoint nor one of its participants? The format doesn't say
  who may speak in a conversation, so this change leaves it open.
- Should a later version add a tool that records a reference episode together
  with the claim citing it, the "on demand" practice in *When an episode is
  recorded*? That spans two formats, and belongs to a harness, not to this
  set.
