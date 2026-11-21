## 1. Conformance

- [ ] 1.1 In *Conformance*, add one sentence naming *Reference Tool Set* as normative for an implementation that exposes a listed tool name, and only for it. Keep "every other section is informative" true for the rest.

## 2. The section

- [ ] 2.1 Add a section *Reference Tool Set* to README.md between *File Layout* and *Design Principles*, opening with:
  - why a set is named: skills and prompts carry over between implementations;
  - its standing: names are a reference, a listed name keeps its semantics, and an implementation with no tools conforms;
  - that it is drawn from the episodes-cli v0.2.0 verbs and that no implementation exposes it yet;
  - an informative note that, in the family, the set is what an MCP server exposes, as DKF's and intentions' sets are.
- [ ] 2.2 State the parameter conventions:
  - snake-case names after the flags;
  - lists for `participants`, `links` as `{rel, href}`, `mementos` and `fields`;
  - `text` passed as a value;
  - `hash_file` and `content_file` as paths the implementation reads, and why;
  - `?` for optional;
  - results are the operation's non-interactive output, and every refusal it makes, the tool makes.
- [ ] 2.3 Add the three tables, Record, Recall and Workspace, giving each tool's parameters and what it does, checked flag by flag against the v0.2.0 verbs:
  - `record inline`, `record ref`, `conversation start`, `conversation turn`, `act`, `observe`, `redact`;
  - `show`, `list`, `query`, `thread`;
  - `validate`, `workspace`.
- [ ] 2.4 State the rules that bind a listed name:
  - the author, the harness and the clock are bound, and `source.model` may be passed;
  - `act_attest` requires a `via` that resolves now to an episode of the bound author's standpoint, and takes no control parameter;
  - the capture rule for conversations, labelled a rule for writers;
  - `episode_record_ref` refuses a duplicate and names the existing episode;
  - `episode_redact`'s result lists what it removed and says history may hold it;
  - the recall tools write nothing, and `episode_query` follows *Recall by query*.
- [ ] 2.5 Add the informative note on resource templates: `episode://{id}` and `episode://{id}/thread`, a scheme local to the server, notification after `observe` and `redact`, and no copy kept of redacted text.

## 3. The rest of the document

- [ ] 3.1 In *Self-attested acts*, add an informative pointer from the dedicated-control case to `act_attest`, saying a control records directly and not through a model's tool call.
- [ ] 3.2 In *When an episode is recorded*, add an informative pointer from "inline content is recorded as it happens" to the capture rule.
- [ ] 3.3 In *Status*, add that no implementation exposes the reference tool set yet, and that the episodes-cli issue tracks one.
- [ ] 3.4 Add the new section to the table of contents, if the document has one.

## 4. Finish

- [ ] 4.1 Check that the normative sentences of the section name no transport and depend on no other specification, so that `standalone-conformance` still holds.
- [ ] 4.2 Proofread, and run `openspec validate add-reference-tool-set`.
- [ ] 4.3 Raise `serve --mcp`, exposing this set, as an issue on nodelogicau/episodes-cli. Ask that findings go in its SPEC-FEEDBACK file.
