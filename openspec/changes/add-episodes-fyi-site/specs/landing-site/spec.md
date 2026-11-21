## ADDED Requirements

### Requirement: The site is one static file with no build and no external request
The site SHALL consist of a single hand-written `docs/index.html`, served by GitHub Pages from `docs/` on `main`. The file SHALL contain no `<script>` element and SHALL reference no resource on any other origin: no external stylesheet, font, image, or `@import`. All diagrams SHALL be inline SVG.

#### Scenario: The page is loaded
- **WHEN** `index.html` is opened in a browser with the network inspector recording
- **THEN** exactly one request is made, for the document itself, and no script executes

#### Scenario: A reviewer checks the source
- **WHEN** the file is searched for `<script`, `<link rel="stylesheet"`, `src="http`, `href="http` inside `<link>`, and `@import`
- **THEN** none is found

### Requirement: The custom domain is declared in the repository
`docs/CNAME` SHALL contain exactly `episodes.fyi`, and `docs/README.md` SHALL record the Pages settings and the DNS records needed to serve it.

#### Scenario: Pages is configured from the repository
- **WHEN** Pages is set to deploy `main` from `/docs`
- **THEN** GitHub reads the custom domain from `docs/CNAME` without it being typed into settings

### Requirement: The page renders in both colour schemes
Colours SHALL be defined as CSS custom properties on `:root`, redefined under `prefers-color-scheme: dark`, and every SVG SHALL take its fills and strokes from those properties.

#### Scenario: The system theme changes
- **WHEN** the operating system switches between light and dark
- **THEN** the page, including every diagram, re-renders legibly with no hard-coded colour remaining from the other scheme

### Requirement: The page reads at phone width
At a viewport 360 CSS pixels wide the page SHALL NOT scroll horizontally. A diagram wider than the viewport SHALL scroll within its own container.

#### Scenario: The page is opened on a phone
- **WHEN** the page is loaded at 360 pixels wide
- **THEN** the body has no horizontal scroll and every diagram is reachable by scrolling its own container

### Requirement: The hero states the headline and the two calls to action
The hero SHALL carry the eyebrow "Episodes · an open format for episodic memory", the headline "You don't reconcile the past.", a lead paragraph that says the format is an early draft, a primary call to action linking to the start section, and a secondary call to action linking to the specification README on GitHub. A muted line beneath the hero diagram SHALL credit the sources the headline and diagram draw on; no heading on the page SHALL name a philosopher.

#### Scenario: A reader arrives
- **WHEN** the page loads at the top on a desktop viewport
- **THEN** the headline, lead, both calls to action and the hero diagram are visible without scrolling

#### Scenario: A reader follows the second call to action
- **WHEN** "Read the spec" is activated
- **THEN** the browser lands on the README of `github.com/nodelogicau/episodes`

### Requirement: The page carries its sections in order
After the hero, the page SHALL present, in this order: "One conversation, two fates"; "Whose memory is it?"; "It records. It never interprets.", including the family diagram; a proof section titled "Read by a second reader"; "Start in your terminal"; and a footer.

#### Scenario: The headings are listed
- **WHEN** the `<h2>` elements are read in document order
- **THEN** they match the five section titles above in that order

### Requirement: The family diagram shows references running into episodes only
The family diagram SHALL show particulars, intentions and episodes, each sibling linked to its site (particulars.fyi, intentions.fyi). It SHALL draw no reference leaving the episodes element, and no reference between the intentions and episodes elements. It SHALL show a DKF claim citing an episode as its evidence, and the link between an intention and what took place as a DKF claim citing both. Its caption SHALL link forgetting.fyi.

#### Scenario: The diagram's arrows are traced
- **WHEN** every arrow in the family diagram is followed
- **THEN** none starts at the episodes element, and none joins the intentions and episodes elements directly

#### Scenario: A sibling is followed
- **WHEN** the particulars or intentions element of the diagram is activated
- **THEN** the browser lands on particulars.fyi or intentions.fyi respectively

### Requirement: The page says nothing the specification does not
Every claim the page makes about the format SHALL be true of the README on `main` at the time of publication. Outside the "Start in your terminal" section the page SHALL NOT name a field, a vocabulary value, or a CLI verb, so that a rename in the specification cannot falsify it.

#### Scenario: The page is checked against the README
- **WHEN** each sentence of the page's prose is read against the README's Problem, Purpose, Approach, Relation to other formats and Status sections
- **THEN** no sentence asserts something those sections do not

#### Scenario: A field is renamed in the specification
- **WHEN** any field or vocabulary value changes name in a later change
- **THEN** no edit outside the terminal section is required for the page to remain true

### Requirement: The proof figure is drawn from real output and can be regenerated
The proof section SHALL contain a figure rendered from the actual `--json` output of a released episodes-cli binary run against an invented example workspace committed under `docs/example/`, written by that binary with the clock fixed and not hand-edited. A script under `docs/` SHALL regenerate the figure's SVG in place between marker comments, and `docs/README.md` SHALL record both the commands that built the workspace and the command that regenerates the figure. The figure's caption SHALL name the CLI version it was drawn from. The figure SHALL NOT show episode ids.

#### Scenario: The figure is regenerated
- **WHEN** the documented command is run against the committed example workspace with the named CLI version
- **THEN** the SVG between the markers is byte-identical to the committed one

#### Scenario: The example workspace changes
- **WHEN** an episode in `docs/example/` is added and the command is re-run
- **THEN** the figure changes to match and nothing outside the markers is touched

#### Scenario: The example workspace is validated
- **WHEN** `episodes validate` is run on `docs/example/` with the named CLI version
- **THEN** it reports no errors

### Requirement: The second-reader account agrees with the implementation's record
Where the proof section states how many points the implementation raised, how many are settled and how many remain open, those counts SHALL equal the status table in episodes-cli's `SPEC-FEEDBACK.md` at the time of publication, and the section SHALL link to that file.

#### Scenario: The counts are tallied
- **WHEN** the rows of the feedback file's status table are counted by status
- **THEN** the page's counts of raised, settled and open items match

#### Scenario: A new item is recorded upstream
- **WHEN** a row is added to the feedback file after publication
- **THEN** the page is out of date until its next edit, and the pre-publication read against the README and the feedback file catches it

### Requirement: The footer's licence statement agrees with the repository
The footer SHALL state that the specification is released under CC0 and the CLI under the MIT License, and this SHALL match this repository's `LICENSE`, its README License section, and episodes-cli's `LICENSE`.

#### Scenario: The licences are compared
- **WHEN** the footer, this repository's `LICENSE` and License section, and episodes-cli's `LICENSE` are read together
- **THEN** all agree

### Requirement: The README points at the site
`README.md` SHALL carry, near the title, a one-line pointer to episodes.fyi described as a visual introduction.

#### Scenario: A reader opens the README
- **WHEN** the first screen of the README is read
- **THEN** the pointer to episodes.fyi is visible
