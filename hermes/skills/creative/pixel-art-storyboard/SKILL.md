---
name: pixel-art-storyboard
description: "Convert a short scene description, book/album cover brief, or 2-paragraph synopsis into a seamless-loop animated pixel-art cover rendered as a self-contained HTML+canvas file."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/creative/pixel-art-storyboard/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Pixel Art Storyboard

Source: `AnastasiyaW/claude-code-config/skills/creative/pixel-art-storyboard/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Pixel Art Storyboard

This module ships two static HTML templates under `templates/` — `single-cover.html` and
`grid-cover.html` — both fully read and confirmed inert (no network calls, no `eval`, only
inline canvas-drawing JavaScript with placeholder tokens like `{{TITLE}}` for the operator to
fill in). They ship as reference/asset data, the same way `pixel-art-studio`'s
`elements/elements.js` does, since neither is invoked by an operator or agent directly. The
upstream `SKILL.md` referenced a third template, `templates/cover-template.js`, which does not
exist anywhere in the pinned upstream snapshot — every code example below points at the two
templates that actually exist instead.

This skill's own bake-to-video/GIF workflow depends on `pixel-art-studio`'s `bake_animation.py`,
which drives headless Chromium via Playwright and shells out to `ffmpeg` — a much larger external
toolchain than the Pillow/numpy `pixel-art-studio` scripts need. It was initially rejected during
review, then reconsidered and accepted after two modifications closed the gaps that caused the
rejection: the target URL must now be `localhost`/`127.0.0.1`/`::1` (rejected otherwise), and its
temp frame directory is always removed afterward. See `mappings/reviewed-scripts.yaml` for the
full record; `mappings/rejected-scripts.yaml` keeps the original rejection as history. The
"Baking finished animations" section below reflects it as available, subject to that localhost
restriction.

Take a short scene description (2–3 paragraphs, one to three elements, mood-driven) and turn it
into a self-contained HTML file with one or more canvas-rendered seamless-loop pixel-art scenes.

This is the bridge from narrative input to animated visual output. It pairs with
`pixel-art-studio` (which handles palettes, dithering, and quality scoring) by providing the
workflow for going from "I want a cover for X" to a working HTML file that opens in a browser.

## When to use

| Request | Use this skill? |
|---|---|
| "Make a cover for [book/album/game]" | Yes — single-cover workflow |
| "Animate this scene" plus a one- to three-paragraph description | Yes |
| "I want a looping pixel background showing X" | Yes |
| "Generate covers for these N books" | Yes — multi-cover grid layout |
| "Just draw a sprite of X" | Use `pixel-art-studio` directly (no scene narrative) |
| "Convert this image to pixel art" | Use `pixel-art-studio`'s `preprocess.py` |
| "Score the quality of my pixel art" | Use `pixel-art-studio`'s `quality_check.py`, or an independent review pass (see Quality review below) |

## The 5-element scene framework

Every scene description must specify these five elements, either explicitly given or inferred
from the request.

| Element | What | Example |
|---|---|---|
| Subject | One to three foreground icons that carry meaning | "Red apple in pale hands" |
| Setting | Background environment, depth layers (at most three) | "Deep night void, single distant star" |
| Lighting | Source, direction, mood | "Cool moonlight from upper-left, warm highlight on subject" |
| Palette | Three to six named colors, not hex | "Midnight black, ivory skin, deep crimson, warm highlight" |
| Motion | What loops, and the period in seconds | "Highlight on apple orbits in 4s; petal drifts down once per loop" |

If the request is vague ("a moody book cover"), fill in the missing elements with sensible
defaults before generating, then list them so the operator can confirm or adjust. Do not proceed
without all five elements settled.

See `references/scene-description-framework.md` for full guidance and three worked examples.

## Workflow

### Step 1 — parse the input into the 5-element framework

If given a paragraph synopsis: extract Subject and Setting plus any symbolic accents. The
iconography is often named explicitly (e.g. "the apple symbolizes forbidden fruit") — that is the
Subject.

If given only a title: research the work (a web search for its cover symbolism or iconic
imagery) to find canonical visual icons, and use those as Subject.

Output a draft scene-description block:

```
SUBJECT: <one to three icons>
SETTING: <one to three layers of depth>
LIGHTING: <source, direction, mood>
PALETTE: <three to six named colors plus accent>
MOTION: <what loops, and the period>
```

### Step 2 — pick the canvas and loop spec

| Canvas | When |
|---|---|
| 64×96 (book aspect, 2:3) | Book/album covers |
| 96×96 (square) | Album art, square covers |
| 128×72 (landscape, 16:9) | Game splash, banner |
| 64×64 (square) | Game tile / icon set |
| 256×144 (wide) | Stream/video banner |

Loop period (see `references/looped-animation-techniques.md` for the full table):

| Loop | Feels like | Use |
|---|---|---|
| 2–3s | Alive, ambient | Idle breathe, water, candle |
| 4–6s | Subtle motion | Breathing, slow drift, ribbon flutter |
| 8–15s | Atmospheric breathing room | Petal fall, smoke plumes |
| 30–60s+ | Slow ambient | Day cycle, wave breaks |

### Step 3 — design the canvas program

For each cover, write a `draw{Name}(ctx, W, H, t)` function where `t` is in `[0, 1)` and is the
loop phase. All animation must derive from `t` — no `Math.random()` (use a seeded hash instead),
no `pos += dt` accumulation (use `sin(t * TAU)` instead), no off-palette ad-hoc colors.

Layer order, bottom to top:

1. Background (sky gradient, void, atmospheric base)
2. Far depth (stars, distant mountains, fog)
3. Mid depth (mid-ground objects, settings)
4. Subject (the iconographic foreground)
5. Foreground motion (falling petals, drifting embers, dust)

Each layer can have its own sub-period, but the parent loop must be their least common multiple,
or use periods that do not visibly drift within a reasonable viewing time.

Use `templates/single-cover.html` as a starting skeleton for its `drawScene(ctx, W, H, t)`
function.

### Step 4 — compose into HTML

A single self-contained HTML file. Layout: one cover, or a responsive grid of covers (2×2 or 4×1
with breakpoints).

Style anchors (a dark-atmospheric aesthetic already used by this skill's own templates):

- Background `#0b0812` (near-black with a violet undertone)
- Foreground text `#a896b4` (lavender-grey)
- Accent (titles, year tags) `#ffb4c8` (pale pink)
- Border `rgba(255,255,255,.06)` (barely visible)
- Font: a monospace stack such as `"JetBrains Mono", ui-monospace, Menlo, monospace`
- Letter-spacing: 0.2–0.35em on titles for generous breathing room
- Cover `image-rendering: pixelated` (and `crisp-edges` for broader support) — forces
  nearest-neighbor scaling

See `templates/single-cover.html` for a single-cover skeleton, `templates/grid-cover.html` for a
multi-cover grid layout.

### Step 5 — test in a browser

Serve the output locally and open it in a browser using whatever preview/screenshot tooling the
operator's environment provides; confirm there are no console errors and that the animation is
visibly running. Iterate.

If there are multiple covers, verify each animates independently (each on its own animation-frame
driver) by watching for two or three seconds and confirming each one changes on its own.

## Loop technique cheat-sheet

The single most important rule: never accumulate state. Always derive position or color from
`t = (now - start) % period`.

```javascript
// CORRECT — phase-derived, drift-free
const t = ((now - start) % period) / period;
const offset = Math.sin(t * Math.PI * 2) * amplitude;

// WRONG — accumulates float drift, may seam visibly after hours
let pos = 0;
function frame(dt) { pos += velocity * dt; /* ... */ }
```

Five techniques to combine for richer motion (see `references/looped-animation-techniques.md`):

1. Phase-based parametric — `sin(t * TAU)` for swaying, breathing, hover.
2. Sub-pixel breathing — animate anti-aliasing (intermediate) pixels without moving the
   silhouette itself.
3. Particle phase-locked — a particle's position is a function of phase and its own seed, not
   `pos += vel`.
4. Parallax with a common multiple — layer scroll rates that all complete a cycle within the same
   frame window.
5. Palette interpolation — mix two colors by `t` for day/night or mood shifts.

## Three registers for scene description

Match the output register to who or what consumes it (see `references/three-registers.md` for
the full taxonomy):

- **LLM agent** generating the canvas program: be explicit and parameter-heavy, constraints
  first — exact canvas size, exact palette hex values, exact motion description, exact phase
  derivation.
- **Human pixel artist** (a commission brief): atmospheric and emotional; trust the artist for
  technical details.
- **A diffusion-model pixel-art prompt** (if generating a reference image rather than a canvas
  program): noun-heavy, comma-separated, with explicit style anchors and a negative prompt
  excluding blur, photorealism, and smooth gradients.

## Working examples

This adapter's `pixel-art-studio` port ships one fully worked case study — a four-cover "Twilight"
example — at `pixel-art-studio/examples/twilight-covers/` (HTML plus a `scenarios.md`
describing each cover's scene description). It demonstrates: mining a well-known work for
canonical iconography, a 5-element scene description per cover, a grid layout with four
independent canvases, distinct loop periods per cover so their beats do not sync mechanically,
and a consistent style match to this skill's own dark-atmospheric aesthetic. Use it as a template
when generating a new multi-cover set.

## Quality review

A ship-ready cover from this skill should pass:

1. Console clean — no JavaScript errors, no "color is undefined", no NaN coordinates.
2. Every canvas renders — a grid layout has no missing covers.
3. Animation runs — visible motion within two or three seconds of page load.
4. The loop is seamless — no visible "snap" at the period boundary.
5. Palette discipline — each cover uses only its declared colors (checkable with
   `pixel-art-studio`'s `scripts/palette.py --analyze`).
6. The symbolic accent is visible at the logical (not just the upscaled display) resolution.
7. The layout matches the reference aesthetic — dark background, lavender-grey text, pink accent,
   monospace, generous letter-spacing.

If any of these fail, fix them before declaring the work done. For an independent check beyond a
self-review, apply this same checklist from a fresh context — someone who has not seen how the
cover was produced, reading only the rendered page and its console output — the same
Generator-Evaluator discipline used elsewhere in this adapter's guidance; it does not require a
dedicated named agent, only genuine independence from the generating session.

## Mandatory rules

1. A single self-contained HTML file — no external CSS/JS files, no CDN links; it must work
   offline.
2. Canvas dimension parity — the `<canvas width height>` attributes match the logical pixel grid;
   CSS sizes are scaling only.
3. `image-rendering: pixelated` is required on every canvas, or the browser will smooth the
   upscale and the pixel art will look blurry.
4. One independent animation-frame driver per canvas — never share a single driver across
   multiple canvases, since one slow draw would block the others.
5. No `Math.random()` in the render path — it must be deterministic; use a seeded hash instead.
6. No accumulating state — everything derives from `t`. No counters that build up frame to frame.
7. Test in a browser before declaring the work done.

## Gotchas

- `Math.random()` in the render path breaks loop seamlessness — particles will drift between
  cycles. Use a seeded hash instead.
- A canvas resolution/CSS size mismatch without `image-rendering: pixelated` upscales with
  smoothing (bilinear-style), and the pixel art looks blurry.
- A responsive grid's breakpoints collapse column count at certain viewport widths — verify at
  more than one width, or adjust the breakpoints to taste.
- An animation-frame driver keeps running on a hidden or backgrounded tab, but browsers often
  throttle it heavily there — for automated screenshot tooling that never actually displays the
  page, render once on the first frame outside the driver loop so the screenshot isn't empty.
- Truncating a coordinate with a bitwise trick introduces a one-pixel jitter on ranges that cross
  zero — use an explicit floor function for negative coordinates; for the usual positive-only
  canvas range either approach is fine.
- A loop period not evenly divisible by the frame interval can cause a perceptible step at typical
  refresh rates — prefer round periods (1s/2s/4s/8s) over odd ones.
- Interpolating a palette in RGB space can clip a saturated channel; use HSL space when
  hue-shifting, RGB only for a pure value shift.
- Redrawing a full-canvas background gradient every frame is wasteful at any real scale; for the
  small canvases this skill targets it is fine, but pre-render to an offscreen canvas once and
  reuse it if a much larger canvas is ever needed.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Canvas appears blurry | Missing `image-rendering: pixelated` | Add it to the canvas's CSS |
| Animation snaps at the loop boundary | First and last frame differ | Derive everything from `t = (now % period) / period` |
| Particles look random on every page load | `Math.random()` instead of a seeded hash | Replace with a seeded hash of a stable index |
| Two animations drift apart over time | Each accumulates its own state | Both should derive `t` from the same clock source directly |
| Color is suddenly NaN or undefined | A hex parser failed on a shorthand form | Always use full six-digit hex |
| Empty canvas in a screenshot | The tab was throttled and the animation-frame driver paused | Draw once on init, outside the driver loop |
| A grid layout shows fewer columns than expected | Viewport width triggered a breakpoint | Adjust the breakpoint, or test at a wider viewport |
| The loop "stutters" at the boundary | Period not divisible by the frame interval | Use a round period (1s/2s/4s/8s) |
| Sub-pixel breathing is not visible | The logical pixel grid is too small | At 16×16 the breathing is only a one- or two-pixel jump; use 32 or larger |

## Reference index

| Topic | File |
|---|---|
| Looped animation techniques (frame match, sub-pixel, parallax, particles, palette interpolation) | `references/looped-animation-techniques.md` |
| Scene description 5-element framework, worked examples | `references/scene-description-framework.md` |
| Three prompt registers (LLM / human / diffusion-model) | `references/three-registers.md` |
| Cover-style canvas templates (single and grid) | `templates/single-cover.html`, `templates/grid-cover.html` |
| Common animation easing functions for pixel art | `references/easing-curves.md` |
| Retouch-style production standard (layered composition) | `references/retouch-style-guide.md` |
| Baking a runtime animation to a video/GIF file | `references/smoother-animation-baking.md` (uses `pixel-art-studio`'s `bake_animation.py`, reviewed and accepted with a localhost-only URL restriction — see `mappings/reviewed-scripts.yaml`) |
| Curating a scene-element dataset toward a reusable library | `references/dataset-to-library-actionable.md` |
| Scaling a canvas element library as it grows | `references/element-library-scaling-architecture.md` |
| A higher-detail rendering pipeline for larger canvases | `references/high-detail-pipeline.md` |
| Sourcing reference imagery from a curated board into a library | `references/pinterest-to-library-pipeline.md` |

## Palette selection: use the Design Seeds curated palettes

Before hand-picking colors, search `pixel-art-studio`'s bundled Design Seeds catalog (ten
palettes covering moods such as nature, twilight, dawn, mystic, vintage, autumn, dreamy, and
dramatic):

```bash
# By tag
python ../pixel-art-studio/scripts/palette.py --search-tag twilight
python ../pixel-art-studio/scripts/palette.py --search-tag dramatic
python ../pixel-art-studio/scripts/palette.py --search-tag mystical

# By free-form mood
python ../pixel-art-studio/scripts/palette.py --mood "night warm"
python ../pixel-art-studio/scripts/palette.py --mood "romantic"
python ../pixel-art-studio/scripts/palette.py --mood "peaceful retreat"
```

The Design Seeds palettes are pre-validated for visual harmony (artist-curated, hue-shifted,
mood-coherent) — using one as the base palette skips the color-discipline step entirely. For
cultural or hardware-authentic palettes (NES, GameBoy DMG, and others), use the bundled palettes
in `pixel-art-studio/scripts/palettes/`.

## Baking finished animations

Upstream's own workflow bakes a verified runtime animation to GIF, WebM-with-alpha, MP4, or a PNG
sequence for archival distribution, using `pixel-art-studio`'s `bake_animation.py`. It drives a
headless Chromium browser via Playwright, shells out to `ffmpeg`, and needs a substantially larger
external toolchain (Playwright, a Chromium install, and `ffmpeg` in `PATH`) than the Pillow/numpy
the other bundled scripts need — reviewed and accepted with one restriction: the target URL must
be `localhost`/`127.0.0.1`/`::1` (the script rejects anything else), and its temp frame directory
is always cleaned up afterward. See `mappings/reviewed-scripts.yaml` for the full record and
`references/smoother-animation-baking.md` for the workflow itself, including the exact command
form.

```bash
python ../pixel-art-studio/scripts/bake_animation.py http://localhost:8000/scene.html \
  --canvas-id scene --period-ms 4000 --fps 30 --format webm-alpha -o scene.webm
```

## Companion skill

`pixel-art-studio` (sister skill): static sprite design, palette tools, dithering, quality
scoring, and bundled palettes. Use it directly for non-narrative pixel-art tasks. Together the
two skills cover: scene description and animated-cover composition (this skill) plus static
design and quality tooling (`pixel-art-studio`). An independent quality review of generated
covers is guidance (see "Quality review" above), not a dedicated named agent this adapter can
invoke.
