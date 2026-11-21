## ADDED Requirements

### Requirement: The reference tool set and its standing
The specification SHALL name a reference set of tools, one for each operation, grouped by what each acts on and named after the verb:
- **Record:** `episode_record_inline`, `episode_record_ref`, `conversation_start`, `conversation_turn`, `act_attest`, `episode_observe`, `episode_redact`.
- **Recall:** `episode_show`, `episode_list`, `episode_query`, `episode_thread`.
- **Workspace:** `validate`, `workspace_status`.

These names are a reference, not a requirement: an implementation MAY expose its operations under other names, or expose no tools. An implementation that exposes a listed name SHALL keep that tool's semantics and accept its parameters as the specification states them. The Conformance section SHALL name *Reference Tool Set* as normative for an implementation that exposes a listed name, and only for that implementation.

#### Scenario: No tools are exposed
- **WHEN** an implementation reads, writes and validates episodes and exposes no tools
- **THEN** it conforms, and nothing in this capability applies to it

#### Scenario: Names differ, nothing is bound
- **WHEN** an implementation exposes a tool called `record_act` with its own parameters
- **THEN** nothing in this capability applies to that tool

#### Scenario: A listed name is exposed
- **WHEN** an implementation exposes a tool called `act_attest`
- **THEN** it SHALL behave as the `act_attest` requirement below states, whatever else it does

### Requirement: Parameters follow the verbs, and results are the verbs' output
Each tool SHALL take the parameters the specification lists for it, named in snake case after the reference implementation's flags. Repeatable values SHALL be lists: `participants`, `links` as `{rel, href}` pairs, `mementos` and `fields`. Text SHALL be passed as a value. `hash_file` and `content_file`, where offered, SHALL be paths the implementation reads, so that exact bytes never pass through a caller's output. Identifiers SHALL be the episode ids the format defines. A tool's result SHALL be the implementation's non-interactive output for the corresponding operation, and every refusal the operation makes, the tool SHALL make.

#### Scenario: Links passed to a tool
- **WHEN** `episode_record_inline` receives `links: [{rel: "via", href: "epi_…"}]`
- **THEN** the written episode carries that `via` link, and the result equals what the operation prints as JSON

#### Scenario: A refused value
- **WHEN** `episode_record_inline` is passed a `uid`
- **THEN** it is refused as the operation refuses it, and nothing is written

### Requirement: The author, the harness and the clock are bound
No listed tool SHALL accept `source.author`, `source.harness`, or a value standing for the current time. The author and the harness SHALL come from the implementation's configuration when it starts. `source.timestamp`, the instant an id is minted, and any time defaulted to now SHALL come from the implementation's clock. A tool MAY accept `source.model`. A tool SHALL accept `occurred` and `basis` where its operation does.

#### Scenario: A caller passes an author
- **WHEN** a listed tool is called with `source.author` naming someone other than the bound author
- **THEN** the call is refused, or the value is ignored and the bound author written, and the result says which

#### Scenario: A caller passes a time for now
- **WHEN** a listed tool is called with a `now` or `timestamp` parameter
- **THEN** the parameter is not accepted, and `source.timestamp` is the implementation's clock

### Requirement: act_attest requires via
`act_attest` SHALL take `via`, `occurred` and `basis`, all required, and SHALL take no parameter that records an act as logged from a dedicated control. `via` SHALL name an episode present in the workspace when the call is made, whose `standpoint` equals the bound author. The act's `standpoint` SHALL be the bound author and its content SHALL be `{mode: attested}`. The specification SHALL state, in an informative note, that a dedicated logging control records through the implementation directly and not through a model's tool call.

#### Scenario: No via
- **WHEN** `act_attest` is called without `via`
- **THEN** the call is refused and nothing is written

#### Scenario: via names an episode not recorded
- **WHEN** `act_attest` is called with a `via` that names no episode in the workspace
- **THEN** the call is refused and nothing is written

#### Scenario: via names someone else's turn
- **WHEN** `act_attest` is called with a `via` naming a turn whose `standpoint` is Jane, and the bound author is Ben
- **THEN** the call is refused and nothing is written

#### Scenario: A requested act
- **WHEN** Ben's turn asks for ninety minutes of deep work from nine to be logged, the turn is recorded, and `act_attest` is called `via` that turn
- **THEN** an act is written with `standpoint` Ben, `content: {mode: attested}` and a `via` link to the turn

### Requirement: A conversation is captured from the harness's transcript
The specification SHALL recommend that a harness record a conversation's turns from its own transcript, through a hook or a connector, and not by having a model call `conversation_turn` with text the model writes. It SHALL say that an implementation MAY leave `conversation_start` and `conversation_turn` out of the tools it lists to a model, and SHALL label the recommendation a rule for writers that no validator can check.

#### Scenario: Reading the recommendation
- **WHEN** an implementor reads the *Reference Tool Set* section
- **THEN** it says that turns come from the harness's transcript, that the two conversation tools may be withheld from a model, and that no validator can check this

#### Scenario: The tools are withheld
- **WHEN** an implementation lists every tool except `conversation_start` and `conversation_turn` to a model
- **THEN** it conforms

### Requirement: episode_record_ref refuses a duplicate
`episode_record_ref` SHALL refuse a call whose `(standpoint, media_type, uid)` matches an existing reference episode, unless `allow_duplicate` is true, and the refusal SHALL name the existing episode.

#### Scenario: The same email cited twice
- **WHEN** `episode_record_ref` is called twice with the same standpoint, `media_type: message/rfc822` and `message_id`
- **THEN** the second call is refused, nothing is written, and the refusal names the first episode

### Requirement: episode_redact states what it did
`episode_redact` SHALL take `id`, `fields` and `reason`, and apply the format's redaction rules: the closed set of paths, the merged block, no cascade. Its result SHALL list every field it removed, including those removed with `content.ref`, and SHALL say that the redaction cannot be undone and that version history may still hold the text.

#### Scenario: Redacting a reference
- **WHEN** `episode_redact` removes `content.ref` from a reference episode that carries a `uid` and links
- **THEN** the result lists `content.ref`, `content.uid` and `links` as removed, and says history may still hold them

#### Scenario: A thread is not redacted with its container
- **WHEN** `episode_redact` removes `content.text` from a container
- **THEN** no child episode changes

### Requirement: Recall tools write nothing
`episode_show`, `episode_list`, `episode_query`, `episode_thread`, `validate` and `workspace_status` SHALL write nothing. `episode_query` SHALL follow *Recall by query*, and each result SHALL carry `resolution`. Withdrawn episodes SHALL be returned by `episode_list` only when `include_withdrawn` is true, and never by `episode_query`.

#### Scenario: A query
- **WHEN** `episode_query` is called with `text: "certificate"`
- **THEN** the results are those *Recall by query* defines, in its order, each with `resolution`, and no file in the workspace changes

### Requirement: The section is transport-neutral
The normative text of *Reference Tool Set* SHALL NOT name MCP or any other transport, and SHALL NOT define a rule by reference to another specification. Any mention of MCP, resource templates or tool annotations SHALL be informative. An informative note SHALL offer the templates `episode://{id}` and `episode://{id}/thread`, and SHALL say:
- the scheme is local to the server and is never written into an episode;
- a server that takes subscriptions notifies subscribers after `observe` and `redact`;
- a client keeps no copy of text a redaction removed.

#### Scenario: Reading the normative text
- **WHEN** the section's normative sentences are read without its informative notes
- **THEN** none names MCP or depends on another specification

#### Scenario: An episode is redacted while a client holds it
- **WHEN** a client has read `episode://epi_…` as a resource and the episode's `content.text` is then redacted
- **THEN** the informative note tells the server to notify the subscribed client, and tells the client to drop the text
