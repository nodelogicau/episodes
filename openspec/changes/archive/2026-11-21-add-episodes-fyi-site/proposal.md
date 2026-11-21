## Why

The format has a normative README and a released reference implementation (episodes-cli v0.2.0, with a Homebrew cask). What it lacks is a front door: nothing a practitioner can read in five minutes that says what episodic memory is for before they open seventeen hundred lines of specification. Its two siblings have one each, at particulars.fyi and intentions.fyi, and forgetting.fyi names this format as the family's gap. The domain episodes.fyi is held, and the README's Status section now names the CLI (#44), so the page can say what exists without contradicting the spec.

## What Changes

- A landing site at **episodes.fyi**, served by GitHub Pages from `docs/` on `main`, in the shape of `intentions/docs`: one hand-written `docs/index.html`, no build step, no JavaScript, no request to any other origin, inline SVG diagrams themed through CSS variables for light and dark.
- The page is a visual introduction, not the specification. The README on GitHub remains the spec and the page's second call to action links to it.
- Hero headline: **"You don't reconcile the past."** The README's Problem section said plainly. The sources the Approach rests on (Kierkegaard's "understood backwards", *Being and Time* §65) are credited in muted text under the hero diagram; no philosopher is named in a heading.
- The beats: the hero; "One conversation, two fates"; "Whose memory is it?"; "It records. It never interprets." with the family diagram linking particulars.fyi, intentions.fyi and forgetting.fyi and showing that references run into episodes and never out, and that intentions and episodes meet only through a DKF claim citing both; a proof section drawn from real CLI output; "Start in your terminal"; a footer stating the licences.
- `docs/example/`: a small invented workspace written by episodes-cli v0.2.0 with the clock fixed, and `docs/timeline-figure.py`, which redraws the proof figure from the binary's `--json` output.
- `docs/CNAME` carrying `episodes.fyi` and `docs/README.md` carrying the deploy and DNS notes and the regeneration command.
- One README edit: a one-line pointer to episodes.fyi under the title. The License section already states CC0 and MIT, so it needs no change.
- Outside the repo: Pages settings and DNS for episodes.fyi.

## Capabilities

### New Capabilities

- `landing-site`: what episodes.fyi is built from and what it asserts. Single static file, no build, no script, no external request, both colour schemes, the required sections and calls to action, the family diagram's one-way references, a proof figure regenerable from real CLI output on a committed example workspace, second-reader counts that agree with episodes-cli's `SPEC-FEEDBACK.md`, a footer whose licence statement agrees with the repository, and a README that points at the site.

### Modified Capabilities

None. No requirement of the format changes. The page states only what the README's Problem, Purpose, Approach and Status sections already say.

## Impact

- New `docs/` directory with `index.html`, `CNAME`, `README.md`, an example workspace and a figure script. One edit to `README.md`. No change to any format capability spec and none to the CLI.
- The proof figure depends on the `--json` output of episodes-cli v0.2.0. The caption names the version, and the regeneration command is documented so the figure can be redrawn when the output or the example changes.
- The second-reader paragraph quotes counts from `SPEC-FEEDBACK.md`. nodelogicau/episodes-cli#22 (its stale preamble) does not block the page, but should land before launch so the file the page links to doesn't contradict the README.
