## Why

A harness reaches an episodes implementation through tools, and nothing in
the draft names them. A skill written against one implementation therefore
has nothing to carry over to another. DKF and intentions each name a
reference tool set, and the family's MCP servers follow them. Episodes has
none, and episodes-cli has no MCP server yet.

Three of the format's rules for writers can't be checked by a validator, and
a tool call is where each of them is most likely to break:

- **A self-attested act is recorded only on its standpoint's explicit
  request, and is linked `via` the episode that holds the attestation.**
  - The CLI's `act --control` means "a dedicated logging control". Over a
    tool call the caller is a model, and a model saying "this came from a
    control" is the very inference the rule forbids.
  - An act's `standpoint` is its `source.author`. If a tool call could set
    `source.author`, a model could attest an act on anyone's behalf.
- **Recording is parsing, and needs no model.** A model that calls a
  conversation-turn tool is re-typing the person's words. A transcript taken
  from the model's output can be paraphrased, trimmed or incomplete, and
  nothing in the file shows it.
- **Nothing is recorded before it happens.** A tool that accepts a time to
  stand for "now" lets a caller set `source.timestamp` to a moment it hasn't
  reached.

Naming the tools is also the moment to say how redaction, duplicate
references and recall behave when a model makes the call, before an
implementation decides for itself.

## What Changes

- **A new normative section, *Reference Tool Set*,** after *File Layout*.
  - It names one tool per verb, grouped by what each tool acts on:
    - **Record:** `episode_record_inline`, `episode_record_ref`,
      `conversation_start`, `conversation_turn`, `act_attest`,
      `episode_observe`, `episode_redact`.
    - **Recall:** `episode_show`, `episode_list`, `episode_query`,
      `episode_thread`.
    - **Workspace:** `validate`, `workspace_status`.
  - It gives each tool's parameters, typed after the format's own
    structures.
  - The names are a reference. An implementation MAY use others. One that
    exposes a listed name SHALL keep that tool's semantics, so skills carry
    over between implementations. An implementation that exposes no tools
    conforms.
  - The set is transport-neutral. MCP is named only in informative notes, so
    the format still defines no rule by reference to another specification.
- **The rules the set carries into a tool call,** binding on any
  implementation that exposes the listed name:
  - **`act_attest` requires `via`, and takes no `control` parameter.**
    - `via` must name an episode that is in the workspace now and has the
      act's standpoint.
    - A dedicated logging control records through the implementation
      directly, not through a model's tool call.
  - **No tool sets `source.author` or the clock.**
    - The author is the one the server is bound to, so an act's standpoint
      can't be chosen per call.
    - `source.timestamp`, and any time defaulted to now, come from the
      implementation's clock. No tool accepts a value to stand for now.
  - **A conversation is recorded from the harness's transcript.**
    - A harness SHOULD write turns from its own transcript, through a hook or
      a connector, and not by having a model call `conversation_turn`.
    - An implementation MAY leave `conversation_start` and
      `conversation_turn` out of the tools it lists to a model.
  - **`episode_record_ref` refuses a repeated `(standpoint, media_type,
    uid)`** unless `allow_duplicate` is passed.
  - **`episode_redact` is irreversible and never cascades.** Its result says
    what it removed and that version history may still hold the text.
  - **The recall tools write nothing.** `episode_query` follows *Recall by
    query*, and every result carries `resolution`.
- **Resource templates, informative:** `episode://{id}` and
  `episode://{id}/thread`, for a server that serves episodes as resources.
  - The scheme is local to the server and is never written into an episode.
  - An episode file changes only by `observe` and `redact`, so a server that
    takes subscriptions notifies subscribers on those writes. A client keeps
    no copy of redacted text.
- **Conformance:** *Reference Tool Set* joins *Core Object Types* and *File
  Layout* as normative, scoped to implementations that expose a listed name.

## Capabilities

### New Capabilities

- `harness-tools`: the reference tool set and its standing, and the
  parameter conventions:
  - `act_attest`'s `via`;
  - that the author and the clock are bound, not passed;
  - that conversations are captured from the harness's transcript;
  - duplicate refusal, redaction's result and read-only recall;
  - the informative resource templates.

  The name matches intentions' capability for its tool set.

### Modified Capabilities

None. `self-attested-acts` keeps the dedicated-control case. The tool set
only declines to offer it to a model. `standalone-conformance` holds as it
stands, because the new section defines no rule by reference to MCP or a
sibling format.

## Impact

- **`README.md`:**
  - *Conformance*: name the new section as normative for an implementation
    that exposes a listed tool.
  - A new section, *Reference Tool Set*, between *File Layout* and *Design
    Principles*.
  - *Self-attested acts*: an informative pointer from the dedicated-control
    case to `act_attest`.
  - *When an episode is recorded*: an informative pointer from "inline
    content is recorded as it happens" to the capture rule.
  - *Status*: a line saying no implementation exposes the set yet.
- **No change** to an episode, `episodes.yaml` or the index. No valid
  workspace becomes invalid.
- **episodes-cli:** it has no MCP server. `serve --mcp`, exposing this set,
  would be a new change there, raised as an issue on
  nodelogicau/episodes-cli. The set is drawn from the v0.2.0 verbs. It's
  written ahead of a binary, unlike intentions', whose set was verified
  against intentions-cli.
- **episodes.fyi:** no change. The page names no tool.
