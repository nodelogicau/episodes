# episodes.fyi

The landing page for the Episodes Format: one hand-written HTML file, no build
step, no JavaScript, no external requests. Served by GitHub Pages from this
`docs/` directory on `main`, with the custom domain in `CNAME`.

The page is a visual introduction, not the specification. The README at the
root of this repository is the specification, and the page says nothing it
does not. Outside the terminal section and the generated proof figure, it
names no field, vocabulary value or CLI verb.

## Deployment

Repository settings → Pages: source **Deploy from a branch**, branch `main`,
folder `/docs`, custom domain `episodes.fyi`, **Enforce HTTPS** once the
certificate is issued.

## DNS (Cloudflare, for episodes.fyi)

Apex `A` records, all four GitHub Pages addresses, DNS-only (grey cloud) so
GitHub can issue the certificate:

```
episodes.fyi.  A  185.199.108.153
episodes.fyi.  A  185.199.109.153
episodes.fyi.  A  185.199.110.153
episodes.fyi.  A  185.199.111.153
```

Optional: `www` as a `CNAME` to `nodelogicau.github.io` (GitHub redirects it
to the apex once the custom domain is set).

`blog.episodes.fyi` and every other subdomain are deliberately left free.

## The example workspace

`example/` is a real workspace, written by episodes-cli 0.2.0 with the clock
fixed for every write. It is invented: Ada's week of 16 November 2026. Jane
emails on Monday that the status page certificate expires on Friday (a trace,
never the mail's text). On Tuesday Ada tells her assistant she renewed it from
two until half past; the conversation is a container of two turns, one in
each speaker's name, and the act is recorded as attested via Ada's turn. On
Friday the mail is observed gone from the mailbox, and the trace remains.
Nothing in it is hand-edited. It was built with:

```sh
export ADA=https://example.com/people/ada JANE=https://example.com/people/jane \
  ASST=https://example.com/assistant EPISODES_HARNESS=example-harness
episodes init docs/example --author "$ADA" --harness example-harness \
  --zone Australia/Melbourne
W="--workspace docs/example"
episodes $W record ref --kind email --standpoint "$JANE" --participant "$ADA" \
  --ref "mail:inbox/4471" --message-id "<status-cert-4471@mail.example.com>" \
  --media-type message/rfc822 --label "Status page certificate expires Friday" \
  --occurred "2026-11-16T09:12:00+11:00[Australia/Melbourne]" --basis stated \
  --now 2026-11-15T22:15:00Z
CONV=$(episodes $W conversation start --standpoint "$ADA" --participant "$ASST" \
  --text "I renewed the status page certificate this afternoon, from two until half past. Can you log it?" \
  --now 2026-11-17T05:40:00Z --json)
C=$(jq -r .container.id <<<"$CONV"); T1=$(jq -r .turn.id <<<"$CONV")
episodes $W conversation turn "$C" --standpoint "$ASST" --participant "$ADA" \
  --text "Logged: renewed the status page certificate, Tuesday 14:00 to 14:30." \
  --now 2026-11-17T05:40:20Z
episodes $W act --label "Renewed the status page certificate" \
  --occurred "2026-11-17T14:00:00+11:00[Australia/Melbourne]" \
  --end "2026-11-17T14:30:00+11:00[Australia/Melbourne]" --basis stated \
  --via "$T1" --now 2026-11-17T05:40:30Z
MAIL=$(episodes $W list --kind email --json | jq -r '.episodes[0].id')
episodes $W observe "$MAIL" --state gone --now 2026-11-19T23:00:00Z
episodes $W validate --now 2026-11-20T00:00:00Z
```

Re-running that produces a workspace with different ids. The committed one is
the one the figure was drawn from; do not rebuild it to regenerate the figure.

## Regenerating the proof figure

The figure in the proof section is a static SVG rendered from the binary's
own output on `example/`, by `timeline-figure.py`:

```sh
python3 docs/timeline-figure.py
```

The script runs `episodes list --json`, `episodes thread --json` and
`episodes show --json` against the example workspace and rewrites the SVG
between the `TIMELINE-FIGURE` markers in `index.html`. With the same binary
the result is byte-identical; with a newer binary the version written into the
figure changes, which is the signal to re-read the caption.

## Before publishing an edit

- Read every sentence of prose against the README's Problem, Purpose,
  Approach, Relation to other formats, Design Principles and Status sections.
- Tally the status table in episodes-cli's `SPEC-FEEDBACK.md` and check the
  proof section's counts (raised, settled, open).
- Check the footer's licence sentence against both `LICENSE` files and the
  README's License section.
