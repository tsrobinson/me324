# ME324 — AI and Deep Learning

LSE Summer School · 2026 · Dr Thomas Robinson · Lab instructor: Kaifang Zhou

Three-week (54 hour) intensive introduction to deep learning and modern AI:
foundations → vision & generative → text generation → ethics & wrap.

---

## Repo layout

```
summer_school/
├── _quarto.yml                # Project-level Quarto config (theme, format)
├── refs.bib                   # Shared bibliography
├── README.md                  # This file
│
├── assets/
│   ├── theme/
│   │   └── me324.scss         # Custom RevealJS theme (extends `white`)
│   └── images/                # Shared image assets (carried across from MY475)
│
├── lectures/
│   ├── lecture-01-what-is-ai.qmd
│   ├── lecture-02-deep-models-primer.qmd
│   ├── lecture-03-computational-graphs.qmd
│   ├── lecture-04-backpropagation.qmd
│   ├── lecture-05-feedforward.qmd
│   ├── lecture-06-cnns.qmd
│   ├── lecture-07-generative-images.qmd
│   ├── lecture-08-text-embeddings.qmd
│   ├── lecture-09-rnns.qmd
│   ├── lecture-10-attention-transformers.qmd
│   ├── lecture-11-tokenization-refinements.qmd
│   └── lecture-12-ethics-recap.qmd
│
├── labs/                      # (To be built — daily computer workshops)
│
├── _site/                     # Quarto build output (gitignored)
│
├── ME324 Course Outline 2025.docx
└── deep_learning_ss_course_proposal_2627.docx
```

---

## The website

This repo is a **Quarto website** (the source of the GitHub Pages site). It has a home
page (`index.qmd`), a **Lectures** page (`lectures.qmd`, a card listing of the decks), a
**Labs** page (`labs.qmd`, links to every notebook), and the **Reading list**
(`readings.qmd`). The lecture decks still build as RevealJS slides (config in
`lectures/_metadata.yml`); the lab notebooks render as read-only HTML pages
(`labs/_metadata.yml` turns execution off).

```bash
# Build the whole site (pages + decks + lab pages) into docs/
quarto render

# Live preview while editing
quarto preview
```

The rendered site is written to **`docs/`** (committed, so GitHub Pages can serve it).

Requirements:

- [Quarto](https://quarto.org) ≥ 1.5
- A `dot` (Graphviz) install for the embedded `{dot}` graphs — `brew install graphviz` on Mac.
- Python + Jupyter (for rendering the lecture `{python}`/`{dot}` cells).

### Deploying to GitHub Pages

1. **Set your repo details** in `_variables.yml` (`owner`, `repo`, `branch`) — this drives
   the *Open in Colab* and *Download* links on the Labs page — and update `site-url` /
   `repo-url` in `_quarto.yml` to match. Then re-run `quarto render`.
2. Commit everything (including `docs/`) and push to GitHub.
3. In the repo: **Settings → Pages → Build and deployment → Source: _Deploy from a branch_**,
   then choose branch **`main`** and folder **`/docs`**. Save.
4. Your site appears at `https://<owner>.github.io/<repo>/` within a minute or two.

(`docs/.nojekyll` is included so GitHub Pages serves Quarto's `site_libs/` assets correctly.)

---

## The theme — `assets/theme/me324.scss`

A custom RevealJS theme designed to feel academic but contemporary, without
defaulting to Beamer's institutional grey or Quarto's vanilla white. It extends
the built-in `white` theme via Quarto's SCSS layering, so individual tweaks are
all in one file.

Design decisions worth noting:

- **Palette**: deep ink `#0E1A2B` for headings, warm off-white `#FBFAF6` paper,
  LSE-adjacent red `#C9322B` as the primary accent, calm blue `#1A6FB4` for
  links/secondary, teal-green `#2F8F6C` for positive callouts.
- **Fonts**: Inter (sans), Newsreader (serif/italic emphasis), JetBrains Mono
  (code). All pulled from Google Fonts.
- **Title slides**: dark gradient with subtle radial accents; eyebrow + footer
  framing positioned by absolute CSS rather than a partial template (so it
  works out of the box, no special config).
- **Section dividers**: any `# H1` becomes a left-rule headline; pair it with
  `{background-color="#0E1A2B"}` for a dark cover slide.
- **Slide titles**: `## H2` gets a hairline underline + accent rule for
  rhythm.
- **Utility classes** (use on text or in spans):
  - `.eyebrow` — small caps eyebrow label above a heading.
  - `.pill`, `.pill-blue`, `.pill-green`, `.pill-amber` — coloured chips.
  - `.card` — bordered surface block, good for "key takeaway" boxes.
  - `.small`, `.xsmall`, `.muted`, `.accent`, `.accent-2`, `.accent-3` —
    text styling.
  - `.bignum` — oversized stat / one-liner emphasis.
  - `.pause-cue` — inline cue for "stop and check" moments.
  - `.timing` — small monospace chip showing how long a section takes.
- **Structural slide types** (Quarto attribute: `{.classname}` on the
  section header):
  - `{.transition}` — the inter-lecture handoff slide. Dark gradient with the
    closing/opening question framed centrally. Use at the start (yesterday's
    question) and end (tomorrow's question) of every lecture.
  - `{.plenary}` / `{.exercise}` — the in-lecture activity sections. Blue
    gradient background to draw attention.
  - `{.break-slide}` — the 15-minute break. Calm warm-grey background, big
    `<span class="clock">15:00</span>` countdown.
- **In-slide boxes**:
  - `::: {.try-box}` / `::: {.reveal-box}` — paired "try this / then reveal
    the answer" cards.
  - `::: {.schedule}` with `::: {.slot}` children — the "today's plan"
    horizontal strip used at the top of each lecture.
- **Callouts**: Quarto's `::: {.callout-note/tip/warning/important/caution}`
  blocks are restyled to use the brand palette.

To preview the theme in isolation, render any lecture — they all use the same
configuration via `_quarto.yml`.

---

## Lecture sequence

| # | Date (2026) | Title | Reuses from MY475 |
|---|---|---|---|
| 1 | Mon 03 Aug | What do we mean by *AI*? | new |
| 2 | Tue 04 Aug | Deep models — a primer | L1 (perceptron, multi-input, weights) |
| 3 | Wed 05 Aug | Computational graphs & the maths of AI | L1 (linalg, calculus, graphs) |
| 4 | Thu 06 Aug | Backpropagation | L2 |
| 5 | Mon 10 Aug | Feed-forward networks in PyTorch | L3 |
| 6 | Tue 11 Aug | Classifying images (CNNs) | L5 |
| 7 | Wed 12 Aug | Generating images (autoencoders, VAEs, diffusion) | L4 |
| 8 | Thu 13 Aug | Text-gen 1/4 — embeddings & character models | new |
| 9 | Mon 17 Aug | Text-gen 2/4 — recurrent networks | new |
| 10 | Tue 18 Aug | Text-gen 3/4 — attention & transformers | new |
| 11 | Wed 19 Aug | Text-gen 4/4 — tokenisation & sampling | new |
| 12 | Thu 20 Aug | Ethics, limitations, course recap | new |
| — | Fri 21 Aug | Final exam | — |

Each lecture follows the **same 3-hour shape**:

1. **`{.transition}` slide** — picks up yesterday's closing question.
2. **Today's plan** — visual `{.schedule}` strip showing the three-block structure.
3. **Part 1** (≈ 45–55 min) — first content block, with worked examples.
4. **`{.plenary}` section** — in-class exercise with `{.try-box}` and
   `{.reveal-box}` slides.
5. **`{.break-slide}`** — 15-minute break (countdown clock).
6. **Part 2** (≈ 45–50 min) — second content block.
7. **`{.exercise}` section** — short in-lecture activity.
8. **Part 3** (≈ 25–35 min) — synthesis, applications, take-stock.
9. **`{.transition}` slide** — tomorrow's opening question (matches the next
   lecture's opening).
10. **Lab brief** — 90-minute computer workshop for the afternoon.

**Pedagogical design choices** worth knowing:

- **Maths clarifies, never proves.** Every formula is paired with a worked
  example using concrete numbers.
- **CS examples paired with social-science examples** throughout — voter
  turnout, Hegre civil-war forecasting, MIDAS missing-data imputation, Torres
  vote-tally CNNs, gender bias in embeddings, etc.
- **Each lecture's closing question is the next lecture's opening question**,
  word-for-word — to make the inter-lecture arc explicit.
- **Take stock slides** at the end of each Part — explicit summary of what
  the student can now do.

---

## To do — labs

Labs are still to be designed. The course brief is:

- 12 × 90-minute computer workshops.
- Python + PyTorch, Google Colab default, local install optional.
- Tracks the lecture content one-for-one (lab N follows lecture N).
- Hands-on: students implement, train, and probe models — not just read.

Some recurring threads worth carrying through the labs:

- Lectures 3–4 build a `Value`-based autodiff library by hand. Lab 5 should be
  the first lab in PyTorch.
- Labs 8–11 should share a single text corpus (probably *tiny-shakespeare* or
  similar) so students can directly compare bigram → RNN → transformer
  → BPE-transformer on the same data.
- The midterm take-home assessment sits between lab 8 and lab 9 (end of
  week 2). It should test the foundations + vision content.

---

## Acknowledgements

- Content scaffolding draws heavily on the LSE MY475 *Applied Deep Learning
  for the Social Sciences* slide set (also Robinson). The summer-school
  course extends MY475 with text generation, transformers, and a stronger
  ethics module.
- Theme inspiration: a mix of modern academic poster design, *Distill.pub*'s
  typographic restraint, and the Stripe/Linear school of dark gradient
  title cards.
