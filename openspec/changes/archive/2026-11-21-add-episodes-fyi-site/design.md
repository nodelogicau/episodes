## Context

`intentions/docs` is the model, and it was itself modelled on `particulars/docs`: one hand-written `index.html`, a `CNAME`, a `README.md` with deploy and DNS notes, a committed example workspace written by a released binary with the clock fixed, and one Python script that rewrites a proof SVG between marker comments. No build, no JavaScript, no external request, light and dark through CSS variables. Its `landing-site` spec is the closest precedent for what this change specifies. forgetting.fyi uses the same constraints for a paper rather than an introduction.

This repository's README is the normative specification, about 1,750 lines. Its Problem, Purpose and Approach sections already carry the argument the page needs: what happened has nowhere to go, an episode records and never interprets, most episodes are traces and not copies, and the family divides Kierkegaard's sentence between its formats. Status names episodes-cli v0.2.0 as a reference implementation. The License section already states CC0 1.0 Universal for the spec and MIT for implementations.

episodes-cli v0.2.0 has a Homebrew cask (`brew install nodelogicau/tap/episodes`), a global `--json` flag, and `EPISODES_NOW` for a fixed clock. Its `SPEC-FEEDBACK.md` records 18 items, 10 settled upstream and 8 open.

## Goals / Non-Goals

**Goals:**
- A page a practitioner reads in five minutes and comes away knowing why what happened needs its own format, that an episode never interprets, whose standpoint a record keeps, and how the other two formats cite it.
- Everything on the page true of the README as it stands, so the page can't drift into a second specification.
- The three sibling sites recognisably from one hand, deployable by the same steps.

**Non-Goals:**
- Rendering the specification as web pages. The README stays canonical and linked.
- Any client-side behaviour, analytics, fonts, or asset served from elsewhere.
- A blog, `www` content, or any subdomain.
- A GitHub Actions workflow. Deploy-from-branch needs none.

## Decisions

**One file, no build, no JavaScript.** The siblings' constraints carry over unchanged, for the same reasons: the page is content, a single file is the cheapest thing to review through git, and the three sites stay maintainable the same way. An Astro site (the `particulars-website` pattern) buys a blog this page doesn't need.

**The headline is the Problem section said plainly: "You don't reconcile the past."** The README's own sentence is "you don't reconcile a past event, only beliefs about it", and that's the distinction the format exists for. It also sets the page against its sibling: particulars is the format that reconciles. Rejected: "Life can only be understood backwards", which is Kierkegaard's line rather than the format's and belongs in the credit; "What happened, from where you stood", which is accurate but reads as a tagline rather than a claim. As with the siblings, the philosophy is credited once in muted text under the hero diagram (Kierkegaard's *Journals*, 1843; *Being and Time* §65) and named in no heading.

**The hero diagram is one happening, many readings.** A single fixed episode on the left; on the right, claims that cite it, one later revised, the episode unchanged. This is the Approach's central point, that kept apart, the event stays fixed and every reading cites the same record, and it needs no field names.

**The beats, in order.**
1. Hero: eyebrow "Episodes · an open format for episodic memory", headline, lead, a primary call to action to `#start`, a secondary one to the README, the diagram, the muted credit.
2. "One conversation, two fates": a person tells their assistant the certificate was renewed on Tuesday. Fate one: it stays in one harness's private chat history, and the claim drawn from it can cite nothing. Fate two: the conversation is a record of turns in the person's own workspace, and the claim cites the turn. Then three cards for what's done today instead: chat history, a note in the knowledge base, a journal entry.
3. "Whose memory is it?": every episode says whose experience or record it is and where the content lives. Most episodes are traces of something that already has a home, a pointer with enough to stand as a record after the thing is gone. Conversations, which have no other home, are held inline.
4. "It records. It never interprets.": no topics, no sentiment, no summary, no verdict; each of those is a reading that cites the episode. A record is never revised: it accumulates, and a person can withdraw content without the record losing its place. Beneath it, the family diagram (below).
5. Proof, "Read by a second reader" (below).
6. "Start in your terminal": the cask install, `init`, a conversation turn, a trace, `list`, `validate`; then links to the specification, the CLI and the release, and a status line: an early draft with a reference implementation.
7. Footer: the siblings' sentence with the names swapped.

**The family diagram shows the arrows only one way.** Three boxes in the README's Purpose order: particulars (what is believed), intentions (what a person means to do), episodes (what happened). The only arrow touching episodes runs into it, from particulars, labelled as a claim citing an episode as evidence. No arrow leaves episodes, and none runs between intentions and episodes: per the README's Relation to other formats, an episode doesn't name the intention it realised and intentions doesn't cite episodes; the link is a DKF claim citing both. The diagram shows that by routing the loop through particulars: a claim cites the episode and the intention, and that is what closes the loop. Each sibling box links to its site, and the caption links forgetting.fyi as the paper that names the gap. This is the one beat the siblings don't have, and the one fact about episodes most likely to be drawn wrongly.

**The proof is real output on an invented workspace.** The format is the most personal of the three (conversations, mail, voice), so no real workspace is used, private or scoped. `docs/example/` is written by episodes-cli v0.2.0 with `EPISODES_NOW` fixed, in a scripted run recorded in `docs/README.md`: Ada's week, with one conversation container and its turns in two standpoints, an act attested via a turn, and a trace of an email from another person. Nothing in it is hand-edited. Re-running the script gives different ids, so the committed workspace is the one the figure is drawn from.

**The figure is a timeline, generated.** `docs/timeline-figure.py` runs `episodes list --json`, `episodes thread --json` and `episodes show --json` (for links and source status, which `list` doesn't carry) against the example with the fixed clock and rewrites the SVG between `TIMELINE-FIGURE` markers in `index.html`: one lane per standpoint, episodes placed by when they occurred, the conversation's turns in order under their container, the act linked to the turn that attested it, and the trace marked as pointing elsewhere, with a badge on the day its source was observed gone. The example's story is the page's own: Jane's email says a certificate expires Friday, Ada renews it on Tuesday and tells her assistant, the act is attested via her turn, and by Friday the email has gone from the mailbox while its trace remains. Ids are left out. The caption names the CLI version. Rejected: `query` output as the figure, since a result list shows recall rather than what an episode is; it can be a later change.

**The second-reader paragraph leads the proof section.** episodes-cli was written from the text; implementing it raised 18 points the draft didn't decide, 10 now settled in the spec and 8 open. The counts come from the status table in `SPEC-FEEDBACK.md`, which the paragraph links, and they're checked against it at publication, as intentions does.

**Siblings, not triplets.** The same neutrals, type scale, section rhythm and SVG class vocabulary as intentions.fyi, copied from its file, with a third accent hue: particulars is teal, intentions is indigo, episodes takes a warm amber, for what has been: `#9a5a0f` on light, `#e9b56c` on dark. intentions uses amber for its "challenge" colour; this page has no such role, so the challenge tokens are dropped rather than recoloured, and two classes are added for the figure (`trace`, a dashed card, and `container`, a dotted wrapper).

**Deploy from branch.** Repository settings, Pages, "Deploy from a branch", `main`, `/docs`, custom domain `episodes.fyi`, enforce HTTPS once the certificate is issued. DNS is the four GitHub Pages apex `A` records, DNS-only if the zone is on Cloudflare, and optionally `www` as a `CNAME` to `nodelogicau.github.io`.

## Risks / Trade-offs

- [The page and the README disagree] → The page's prose names no field, vocabulary value or verb outside the terminal section (the generated figure is the binary's output and is exempt), and a verification task reads every sentence against the README's Problem, Purpose, Approach, Relation to other formats, Design Principles and Status sections before launch.
- [The terminal section names CLI verbs that later change] → They're the CLI's, not the format's, and the section names the release it was written against. A CLI rename is an edit to that section only.
- [The `--json` shape changes and the figure goes stale] → The script and example are committed, regeneration is one command, and the caption names the version it was drawn from.
- [The second-reader counts go stale as items settle] → The page is out of date until its next edit, as with intentions. The pre-publication check reads the counts against the file.
- [The linked `SPEC-FEEDBACK.md` still says the README claims no implementation] → nodelogicau/episodes-cli#22 fixes it; a task checks it has landed before launch.
- [The format is a draft and may change under the page] → The page says it's an early draft, in the hero lead and the status line. Its claims are the Approach's, which are the least likely part of the README to change.
- [Hand-drawn SVG is slow to change] → Accepted, as both siblings accepted it.

## Migration Plan

1. Merge `docs/` and the README pointer to `main`.
2. Pages settings as above; confirm the `github.io` address serves the page.
3. DNS for episodes.fyi; wait for the certificate; enforce HTTPS.
4. Before announcing: episodes-cli#22 has landed, and the footer, the second-reader counts and the status line are checked against their sources.

Rollback is removing the custom domain in Pages settings; the repository is unaffected.

## Open Questions

- Where is the episodes.fyi zone: Cloudflare (as intentions.fyi, A records DNS-only) or the registrar (as particulars.fyi)? Only `docs/README.md` changes.
- Should the sibling sites gain a link to episodes.fyi, for example in the composition diagrams that currently point only at each other? That's a change in each sibling repo, not here.
- Whether the decisions behind the headline and register are recorded as claims in a knowledge workspace, as intentions did, and which one.
