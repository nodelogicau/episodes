## 1. Field table

- [x] 1.1 Add `activity` to the `kind` examples, still described as descriptive only
- [x] 1.2 Update the `content` row: `mode: none` is for a container, or for a self-attested act

## 2. Content and the self-attested act

- [x] 2.1 Widen the `mode: none` paragraph in `#### content`: valid on a container, and on a self-attested act; writers SHOULD write a container together with its first child
- [x] 2.2 Add a `#### Self-attested acts` subsection after Containment, covering:
  - what one is;
  - the two content forms (ref to the attesting episode, or `none`);
  - a YAML example of a deep-work block attested in conversation
- [x] 2.3 In it, state the self-only rules: standpoint equals `source.author`; a ref'd attestation's standpoint equals the act's; an unresolved ref is reported as unresolved, not invalid
- [x] 2.4 State the writer rule: record only on explicit attestation, never from inference; a passing remark stays a turn, and what is taken from it is a DKF claim (informative pointer)
- [x] 2.5 State how a validator recognises one by shape: `mode: none` with no children, or a `ref` that is an episode id; `kind` changes nothing
- [x] 2.6 State timing: `occurred` is when the act took place (`stated` or `inferred`), subject to the rule that nothing is recorded before it happens; give the "logged before it ends" case
- [x] 2.7 Say why other people's acts are excluded, pointing to the `standpoint` section's rule for notes

## 3. Surrounding text

- [x] 3.1 Add a bullet to When an episode is recorded: self-attested acts are recorded on the person's explicit attestation
- [x] 3.2 Add a Status open question on a harness's own acts that left no record

## 4. Verify

- [x] 4.1 Check that new normative text doesn't depend on DKF or intentions (`standalone-conformance`)
- [x] 4.2 Check that the example satisfies the `episode-evidence` timing rules
- [x] 4.3 Run `openspec validate self-attested-acts`
