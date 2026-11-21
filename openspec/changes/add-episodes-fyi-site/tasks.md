## 1. Settle what the page will assert

- [ ] 1.1 Confirm where the episodes.fyi zone is held (Cloudflare or the registrar)
- [ ] 1.2 README: add the one-line pointer to episodes.fyi under the title, worded as the siblings' READMEs word theirs
- [ ] 1.3 Choose the amber accent and record the full palette for both schemes, starting from intentions.fyi's neutrals
- [ ] 1.4 Confirm nodelogicau/episodes-cli#22 is open or landed, and note which in the launch checklist

## 2. The example workspace and the figure script

- [ ] 2.1 Write the build commands for `docs/example/` with episodes-cli v0.2.0 and `EPISODES_NOW` fixed: `init` for Ada, a conversation with turns in two standpoints, an act attested via a turn, a trace of an email from another person
- [ ] 2.2 Run them; confirm `episodes validate` on `docs/example/` reports no errors
- [ ] 2.3 Run `episodes list --json` and `episodes thread --json` and confirm the output carries what the timeline needs (standpoint, occurred, container and order, the act's attesting turn, whether content is inline or a trace)
- [ ] 2.4 Write `docs/timeline-figure.py`: run the binary with the fixed clock, emit the SVG between `TIMELINE-FIGURE` markers in `index.html`, omit ids, use the shared SVG class vocabulary, write the CLI version into the caption
- [ ] 2.5 Confirm a second run is byte-identical

## 3. The page

- [ ] 3.1 `docs/index.html` skeleton: head, `:root` palette and dark override, type scale, section rhythm and SVG class vocabulary carried over from intentions.fyi
- [ ] 3.2 Hero: eyebrow, "You don't reconcile the past.", lead saying it's an early draft, two calls to action, the one-happening-many-readings SVG, muted source credit
- [ ] 3.3 "One conversation, two fates": the two-fates SVG, the kicker, the three cards
- [ ] 3.4 "Whose memory is it?": prose and the standpoint / traces-and-inline SVG
- [ ] 3.5 "It records. It never interprets.": prose on readings and accumulation, then the family diagram with links to particulars.fyi and intentions.fyi, the loop routed through a DKF claim, no arrow leaving episodes, caption linking forgetting.fyi
- [ ] 3.6 "Read by a second reader": the lead paragraph with counts from `SPEC-FEEDBACK.md`, the generated figure between markers, caption with CLI version
- [ ] 3.7 "Start in your terminal": the cask install and first-run commands, links to the spec, the CLI and the release, the status line
- [ ] 3.8 Footer with the licence sentence
- [ ] 3.9 Top-of-file HTML comment recording how the figure is regenerated

## 4. Supporting files

- [ ] 4.1 `docs/CNAME` containing `episodes.fyi`
- [ ] 4.2 `docs/README.md`: purpose, Pages settings, DNS records for where the zone is held, `www` note, subdomains left free, the example's build commands, the figure regeneration command

## 5. Verify

- [ ] 5.1 No `<script`, no external stylesheet, font, image or `@import`; one request in the network inspector
- [ ] 5.2 Both colour schemes, every diagram legible in each
- [ ] 5.3 360 px wide: no horizontal page scroll, diagrams scroll within their containers
- [ ] 5.4 Every link resolves: spec README, CLI repo, v0.2.0 release, `SPEC-FEEDBACK.md`, particulars.fyi, intentions.fyi, forgetting.fyi, `#start`
- [ ] 5.5 Trace every arrow in the family diagram: none leaves episodes, none joins intentions and episodes
- [ ] 5.6 Read every sentence against the README's Problem, Purpose, Approach, Relation to other formats and Status sections; outside the terminal section the page names no field, value or CLI verb
- [ ] 5.7 Tally `SPEC-FEEDBACK.md`'s status table and check the page's counts
- [ ] 5.8 Footer licence sentence agrees with both `LICENSE` files and the README License section

## 6. Deploy and close out

- [ ] 6.1 Commit `docs/` and the README pointer on main; push
- [ ] 6.2 Pages settings: deploy from `main`, folder `/docs`; confirm the `github.io` address serves the page
- [ ] 6.3 DNS: four apex `A` records (DNS-only if on Cloudflare), optional `www` CNAME; wait for the certificate; enforce HTTPS
- [ ] 6.4 Before announcing, episodes-cli#22 has landed and 5.6–5.8 have been re-run
- [ ] 6.5 Archive the change with sync so `landing-site` lands in the main specs
