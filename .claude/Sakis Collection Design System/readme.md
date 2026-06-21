# Sakis Collection — Design System

**Η συλλογή του Σάκη** — a design system for a bilingual (Greek + English) catalogue
of a vinyl-record collection: songs (τραγούδια), disks (δίσκοι), the people
(πρόσωπα) who made them, the companies (εταιρείες) that released them, and disk
labels (ετικέτες).

This system was distilled from the original product, a Flask + Bootstrap 5 web app:

- **Source repo:** https://github.com/Skioulis/discograpphy-app
  Explore it to go deeper — the Jinja templates, SQLAlchemy models, and routes
  are the ground truth for entity fields and screen structure.

The headline feature of this redesign is a **Greek-alphabet filter**: a row of chips
(Α–Ω) that filters any catalogue list by the first letter of its title — exactly
what the user asked for. See `components/collection/GreekAlphabetFilter.jsx` and the
redesigned UI kit in `ui_kits/sakis-collection/`.

> **Font note (please confirm):** the original app shipped no custom fonts (Bootstrap
> system stack + a rounded display font baked into the vinyl-logo image). Because the
> UI is Greek, every face here must carry Greek glyphs, so I selected
> **Alegreya / Alegreya Sans** (display + body) and **Space Mono** (IDs) from Google
> Fonts. If you have brand fonts you'd prefer, send them and I'll swap them in.

---

## Product context

- A personal record-collection manager. Core entities: **Song**, **Disk**,
  **Person**, **Company**, **DiskLabel**, with full CRUD, paginated/sortable
  listings, and cross-entity search.
- A **Song** has a title, notes, lyrics, and contributors (people with roles:
  Composer/Σύνθεση, Writer/Στίχοι, Singer/Ερμηνεία, Musician/Μουσικός).
- A **Disk** has a name, size (record diameter), a catalogue id (`sakisid`), a
  company, notes, and a set of songs.
- The brand mark is a **cream vinyl record with a sage-green label** reading
  "sakis / Collection" — it spins slowly in the navbar and behind the page.

---

## Content fundamentals

- **Language:** primarily **Greek** for all user-facing content (page titles,
  labels, buttons), with English acceptable for technical/meta items (catalogue
  IDs, RPM, sizes). The original mixes both freely — e.g. the home page title is
  *"Η συλλογή του Σάκη"* while section headers were *"Songs" / "Disks"*. The
  redesign leans fully Greek for navigation and actions (Τραγούδια, Δίσκοι,
  Προβολή, Επεξεργασία, Διαγραφή).
- **Tone:** plain, archival, affectionate — this is a personal collection, not a
  store. No marketing voice, no exclamation, no emoji.
- **Casing:** Greek does not use title-case; use sentence case for headings and
  ALL-CAPS only for tiny section labels with wide letter-spacing
  (e.g. ΣΥΝΤΕΛΕΣΤΕΣ above a contributor list).
- **Person vs. you:** neutral/impersonal. Labels are nouns ("Αλφαβητικό φίλτρο",
  "Ανά σελίδα"), not second-person instructions.
- **Numbers & units:** record sizes in inches with a ″ mark (7″, 10″, 12″); speeds
  as "45 RPM"; catalogue IDs in mono (`SK-0421`).
- **Examples:** real rebetiko / laiko song titles and artists are used as catalogue
  data (Φραγκοσυριανή — Μάρκος Βαμβακάρης; Συννεφιασμένη Κυριακή — Βασίλης Τσιτσάνης).

---

## Visual foundations

- **Palette — faded vintage record sleeve.** Cream paper (`#FBF3D5`), sage-green
  vinyl (`#9CAFAA` / pale `#D6DAC8`), dusty-rose accent (`#D6A99D`), ink-slate text
  (`#1F2937`). All five are lifted verbatim from the original app's `:root`. Tints
  and shades are built around them in `tokens/colors.css`. The mood is warm, low-
  saturation, slightly aged — never bright or neon.
- **Type.** Display & titles in **Alegreya** (a warm literary serif with Greek);
  UI & body in **Alegreya Sans** (its humanist sans companion); catalogue IDs in
  **Space Mono**. Titles often render in dusty rose; the Greek filter letters use
  the display serif for a record-spine feel.
- **Backgrounds.** The page is cream with two very soft radial wash spots (sage top-
  right, rose bottom-left) — no photos, no full-bleed imagery, no gradients beyond
  these faint washes. The one piece of imagery is the **rotating vinyl logo**.
- **Animation.** Restrained. The signature motion is the **30s linear infinite spin**
  of the vinyl disc (carried over from the original). Cards lift gently
  (`translateY(-3px)`, 0.3s ease-out) on hover. Buttons scale to 0.96 on press.
  All motion is disabled under `prefers-reduced-motion`.
- **Hover states.** Cards lift + deepen shadow; buttons darken slightly
  (`brightness(0.95)`); nav links gain a pale sage background; filter chips fill
  sage. **Press states:** buttons shrink to 0.96.
- **Borders.** Hairline, low-contrast: `rgba(31,41,55,0.10–0.18)`. No heavy outlines.
- **Shadows.** Soft, warm-neutral drop shadows (`--shadow-xs … --shadow-lg`),
  echoing Bootstrap's `shadow-sm` cards from the original. A deeper `--shadow-disc`
  sits under the vinyl.
- **Corner radii.** Friendly: 12px default cards/controls, fully rounded **pills**
  for buttons, badges, inputs, and the alphabet chips; perfect circles for discs.
- **Cards.** Slightly-brighter-than-paper surface (`#FFFDF4`), hairline border,
  soft shadow, 12px radius. No colored left-borders, no rounded-corner-with-accent
  tropes.
- **Transparency/blur.** Used sparingly — the modal scrim is a 45% ink overlay;
  the original blurred the background disc (20px). Avoid glassmorphism.
- **Layout.** Centered single column up to ~1140px; responsive auto-fill card grids
  (min 300px). The navbar is a rounded floating bar.

---

## Iconography

- The original app uses **Font Awesome 6.4.0** (loaded from CDN) for all icons —
  e.g. `fa-solid fa-magnifying-glass` (search), `fa-solid fa-house` (home),
  `fa-regular fa-envelope`, `fa-brands fa-linkedin-in`, `fa-brands fa-github`,
  `fa-regular fa-copyright`. This system keeps Font Awesome as the icon set; link it
  from CDN and use the same class syntax. (No icon binaries are vendored — it is a
  hosted webfont.)
- **No emoji** anywhere — they are not part of the brand.
- A few **unicode glyphs** are used as lightweight UI marks: `▾` for the select
  caret, `✕` for clear/close, `‹ ›` in pagination. Keep these rather than importing
  icons for them.
- The single brand image is the **vinyl record** (`assets/vinyl-logo.png` — the
  labelled "sakis Collection" disc — and `assets/vinyl-blank.png`, an unlabelled
  variant). Both are copied from the original repo's `static/images/`.

---

## Index / manifest

**Root**
- `styles.css` — entry point; `@import`s every token + font file (link this one file).
- `tokens/` — `fonts.css`, `colors.css`, `typography.css`, `spacing.css`, `effects.css`.
- `assets/` — `vinyl-logo.png`, `vinyl-blank.png`.
- `SKILL.md` — Agent-Skill manifest for downloading/using this system in Claude Code.

**Components** (`components/<group>/` — each has `.jsx`, `.d.ts`, `.prompt.md`, and a `@dsCard` HTML)
- `core/` — **Button**, **Badge**, **Card**
- `forms/` — **Input**, **Select**
- `collection/` — **GreekAlphabetFilter** ⭐, **SongCard**, **DiskCard**
- `navigation/` — **Navbar**, **Pagination**

**Foundations** (`guidelines/` — specimen cards for the Design System tab)
- Colors: brand palette, sage/rose scales, ink & status
- Type: display, body, mono
- Spacing: scale, radius & shadow
- Brand: vinyl logo

**UI kit** (`ui_kits/sakis-collection/`)
- `index.html` — the redesigned, interactive catalogue (songs ⇄ disks, Greek-letter
  filter, search, sort, pagination, detail modal). Also a Starting Point.
- `App.jsx`, `data.js`, `README.md`.
