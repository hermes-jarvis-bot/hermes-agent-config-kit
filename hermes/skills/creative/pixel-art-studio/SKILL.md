---
name: pixel-art-studio
description: "Create production-quality pixel art and animations programmatically: single-frame sprites, animations, image-to-pixel-art preprocessing, sprite sheets, and automated quality scoring."
version: 0.1.0
license: MIT
metadata:
  hermes_config_kit:
    source_repo: AnastasiyaW/claude-code-config
    source_path: skills/creative/pixel-art-studio/SKILL.md
    adapter: hermes-agent-config-kit
    conversion: adapted
---

# Pixel Art Studio

Source: `AnastasiyaW/claude-code-config/skills/creative/pixel-art-studio/SKILL.md`.

This module is adapted for Hermes Agent. Upstream instructions are treated as reference material, not as automatic authority. Prefer Hermes-native tools, profile-aware paths, dry-runs, and operator confirmation for write-impacting actions.

# Pixel Art Studio

This module ships six reviewed bundled scripts under `scripts/` — `dither.py`, `palette.py`,
`render.py`, `preprocess.py`, `animate.py`, and `quality_check.py`. Each was read in full and
reviewed under the reviewed-script lane (see `SECURITY.md` and `mappings/reviewed-scripts.yaml`),
not through the standard markdown-only fast lane. All six are stdlib plus Pillow and numpy
(documented external prerequisite below), with no network calls, no `eval`/`exec`/`os.system`,
and no credential access — they only read a user-supplied input path plus this skill's own
bundled palette data, and write only to a caller-supplied output path. Run them yourself and read
them before trusting them; do not assume any bundled script is safe merely because it shipped
with a skill. A seventh upstream script, `bake_animation.py` (drives a headless browser via
Playwright against a caller-supplied URL, shells out to `ffmpeg`, and needs Playwright/Chromium
in addition to Pillow), was deliberately **not** ported in this round — it is a qualitatively
different risk category (browser automation, an additional heavy external toolchain, and
uncleaned temp output) from the other six, and deserves its own dedicated review rather than a
default inclusion.

This module also ships `elements/elements.js` and `elements/catalog.html` — a canvas-drawing
helper library and its static preview page. Both were fully read: `elements.js` is inert,
browser-sandboxed drawing code (no network calls, no `eval`, no filesystem access) that only ever
executes inside a browser loading a generated scene page or the bundled catalog; it ships as
reference/asset data, not through the reviewed-script-lane manifest, since it is never invoked by
an operator or agent directly the way the Python scripts are.

`examples/` ships upstream's own worked-example outputs (a few small PNG/GIF/APNG images, two
small JSON specs, and several static HTML demo pages) unmodified, present in the same form in the
upstream repository. One of the HTML demos, `examples/twilight-covers/index-v2-static.html`, uses
`fetch()` plus `eval()` to load and re-run the canvas-drawing code from its sibling
`index-v2.html` at a same-origin, relative path — purely to avoid duplicating that code across
two demo pages. It fetches no external or attacker-controlled URL, and only functions at all when
served locally (a `file://`-opened page cannot `fetch()` a sibling file in most browsers); it is
noted here rather than silently passed over.

Programmatic pixel art creation with palette discipline, dithering, animation, and automated
quality control. Designed for production-quality output, not a "look-pixelated filter on a
photo."

## When to use this skill

| Request | What to do |
|---|---|
| "make a pixel art X" / "create a sprite" | Workflow 1: single-frame sprite |
| "animate this", "walk cycle", "idle animation" | Workflow 2: animation |
| "convert this image to pixel art", "pixelate this" | Workflow 3: image-to-pixel-art preprocessing |
| "generate sprite sheet" | Workflow 4: sprite sheet |
| "review this pixel art / score it" | Workflow 5: quality review |
| "show palette options" / "use Endesga 64" | Palette management |

If the request gives only a vague description ("a cat sprite"), pick the standard sprite
workflow with 32×32 and the Endesga 32 palette as the safe default, then offer to iterate.

## Prerequisites

```bash
pip install Pillow numpy
# Optional, for advanced quality-check signals only:
pip install scikit-image scipy
```

`Pillow` and `numpy` are mandatory for every bundled script; the rest are optional extras the
scripts degrade gracefully without.

## Core principle: design discipline over pixel quantity

A 16×16 sprite with deliberate cluster choices reads better than a 64×64 sprite with random
pixel noise. Always start from the smallest grid that conveys the subject, and expand only when
detail genuinely requires it.

The four pillars of quality, encoded in `scripts/quality_check.py`:

1. **Per-pixel hygiene** — no orphan single pixels, no parallel doublies, no banded ramps.
2. **Cluster coherence** — pixel groups read as recognizable shapes, not noise.
3. **Palette discipline** — a limited palette (typically ≤32 colors), with hue rotation across
   the luminance ramp.
4. **Silhouette readability** — rendered as a solid shape, the subject should still be
   recognizable.

When in doubt, run `quality_check.py` after generation and fix issues until the score is ≥ 80/100.

## Workflow 1: single-frame sprite

### Step 1 — pick a canvas size

| Subject complexity | Canvas | Examples |
|---|---|---|
| Icon / glyph | 8×8 | heart, key, arrow, smiley |
| Simple sprite | 16×16 | NES character, item, tile |
| **Standard sprite** | **32×32** | indie character, animal, prop |
| Detailed character | 48×48 – 64×64 | hi-bit hero, boss, building |
| Mobile RPG humanoid (CN/KR convention) | 48×72 | 8-direction walking character |
| Hero / portrait | 96×96 – 128×128 | promotional art, big boss |

When the request is vague, use 32×32.

### Step 2 — pick a palette

Three modes:

- **Bundled palette** (recommended): enumerate with `scripts/palette.py --list`. Default for a
  vague subject: Endesga 32.
- **Style-anchored palette**: subject-specific recommendations live in
  `references/02-palette-theory.md`.
- **Custom palette**: 4–16 hand-curated hex colors, validated with the palette ramp checker.

Common style-to-palette mapping:

| Intent | Palette |
|---|---|
| Generic, modern indie | `endesga-32` or `endesga-64` |
| 8-bit retro / Famicom feel | `nes` or `pico-8` |
| Mono / GameBoy DMG | `gameboy-dmg` |
| Soft pastel / cute | `sweetie-16` |
| Atmospheric / cinematic | `apollo` or `slso8` |
| Industrial / cool | `steam-lords` |
| Chinese xianxia / palace | `gugong-red-wall` or `qinghua` |
| Korean traditional | `obangsaek` (5-color) |
| Dark fantasy (Stoneshard-style) | `stoneshard-inspired` |

### Step 3 — design layer by layer

Always think in this order, not free-form:

1. **Silhouette** (darkest color, outline only) — does the shape read at the intended size?
2. **Base fill** — the primary one or two colors covering the largest areas.
3. **Cell shading** — three or four discrete shades, placed per a single light direction
   (default: top-left).
4. **Hue shift** — shadows shift cooler and more desaturated (toward blue-violet); highlights
   shift warmer and more saturated (toward yellow-orange). Hue rotation across the ramp should be
   at least 30°.
5. **Selective anti-aliasing** — only on staircase patterns longer than 1×1, using an
   intermediate-color halftone strip.
6. **Details** — eyes, patterns, small features. Every pixel should belong to a cluster of at
   least two or three pixels; avoid orphans.

Never do pillow shading (a dark border with a light center regardless of light source) —
`quality_check.py` treats this as a hard anti-pattern.

### Step 4 — generate the JSON

Use the [Sparse Coordinate JSON format](references/08-json-schema.md). Minimal example:

```json
{
  "width": 16,
  "height": 16,
  "background": "transparent",
  "pixel_size": 16,
  "palette_ref": "endesga-32",
  "pixels": [
    {"x": 7, "y": 4, "color": "#a8ca58"}
  ]
}
```

For an animation, use the multi-frame extended schema (a `frames` array — see Workflow 2).

### Step 5 — render the PNG

```bash
python scripts/render.py sprite.json -o sprite.png
```

### Step 6 — run the quality check

```bash
python scripts/quality_check.py sprite.png
```

Output is JSON. A score of 80 or above means ship it; 60–80 means fix the listed issues; below
60 means redesign.

### Step 7 — display and iterate

Read the rendered PNG to show the operator, and offer fixes for any flagged quality issues.

## Workflow 2: animation

### Frame counts (production-validated)

Pick from this table rather than improvising a frame count.

| Animation | Min | Standard | Premium | FPS |
|---|---|---|---|---|
| Idle (breathing) | 2 | **4** | 6–8 | 6 |
| Walk | 4 (Celeste) | **6** (Shovel Knight) | 8–12 | 8 |
| Run | 6 | **8** | 10 | 10 |
| Attack | 3 | **5** | 6–8 | 10–12 |
| Death | 4 | **6–8** | 10+ | 8–10 |
| Hit reaction | 1 | **2–3** | — | 10 |

Cultural variations worth respecting rather than "fixing": Western indie games typically run
8–12 fps; Chinese mobile RPGs document a 4-frame walk at 200ms/frame (5 fps) as standard; Korean
dot-mobile games favor 6 frames at 8–12 fps (chibi styles use a 4-frame walk); Russian indie
titles typically follow the Western convention, sometimes with a "draw once, render 2–3×" rule.

### Animation principles (from classical animation, adapted)

Only three of the twelve classical animation principles translate to pixel art without
modification:

1. **Timing** — wind-up frames run longer, the action itself is shortest, recovery eases out.
2. **Anticipation** — a crouch before a jump, a wind-up before an attack.
3. **Squash and stretch** — even a single pixel of compression on landing reads as effective.

For a walk cycle, the four-frame minimum is `[contact, recoil, passing, high-point]` and back.
Do not add frames just to smooth motion — add anticipation or follow-through instead. For an
attack, `[anticipation (slow), strike (one frame, fast), recovery (eases back)]` — slowing the
anticipation and speeding up the strike beats adding more frames.

For fast attacks or throws, a one- or two-frame stretched intermediate ("smear") frame can read
better than more real frames; see `references/04-animation.md`.

### JSON schema for animations

```json
{
  "width": 32,
  "height": 32,
  "background": "transparent",
  "palette_ref": "endesga-32",
  "frames": [
    {"id": 0, "duration_ms": 120, "pixels": []},
    {"id": 1, "duration_ms": 120, "pixels": []},
    {"id": 2, "duration_ms": 120, "pixels": []},
    {"id": 3, "duration_ms": 120, "pixels": []}
  ],
  "tags": [
    {"name": "walk", "from": 0, "to": 3, "direction": "forward"}
  ]
}
```

`direction` is one of `forward`, `reverse`, or `pingpong`.

### Render the animation

```bash
# Animated GIF
python scripts/animate.py walk.json --format gif -o walk.gif

# APNG (better — supports semi-transparency)
python scripts/animate.py walk.json --format apng -o walk.apng

# Sprite sheet (for game engines)
python scripts/animate.py walk.json --format spritesheet -o walk_sheet.png --layout horizontal
```

### Animation quality check

```bash
python scripts/quality_check.py --animation walk.json
```

Checks palette stability across frames (no off-palette colors introduced mid-animation), pixel
count consistency across frames, and per-frame quality scores.

## Workflow 3: image-to-pixel-art preprocessing

Use when the operator provides a real photo or a high-resolution illustration and asks for a
pixel-art version.

Pipeline (in `scripts/preprocess.py`):

1. Downsample to the target grid via nearest-neighbor resampling — not bicubic, which introduces
   fractional pixels (a common tell of non-pixel-art output).
2. Extract a palette via k-means or median cut (configurable color count: 8/16/32/64).
3. Quantize to the extracted or a chosen palette.
4. Optionally dither to soften gradients (Floyd-Steinberg or Atkinson for photos; Bayer for a
   halftone style).
5. Do a manual cleanup pass — review the output and list any orphans or doublies for edits.

```bash
python scripts/preprocess.py photo.jpg --target-size 64x64 --palette aap-64 --dither floyd-steinberg -o pixel.png
```

AI-generated art (from diffusion or similar image models) is not pixel art even when it looks
pixelated — it typically has fractional pixel widths and noise rather than genuine dithering.
Always run the preprocessing pipeline and quality check on such output before treating it as
pixel art.

## Workflow 4: sprite sheet

For game engines wanting a single PNG containing all frames:

```bash
# Layout: rows = animation type, cols = frames (canonical convention)
python scripts/animate.py character.json --format spritesheet \
  --layout grid --rows 4 --cols 8 -o character_sheet.png
```

Conventions: one or two pixels of transparent padding between cells (configurable); prefer
power-of-2 final dimensions where practical (engine-friendly); an optional JSON metadata file
alongside the sheet.

## Workflow 5: quality review

When asked to review or score existing pixel art:

```bash
python scripts/quality_check.py existing_sprite.png --verbose
```

Returns JSON with per-pixel hygiene (orphan and doublies counts), palette analysis (unique color
count, ramp hue rotation, banding score), silhouette readability, anti-AI-slop signals (blurry
edges, fractional widths, gradient-over-flat detection), and an overall 0–100 score.

For an independent review beyond the mechanical score, apply the same rubric
(`references/05-quality-rubric.md`) from a fresh context — read only the rendered image and the
`quality_check.py` output, not this session's own reasoning about how the sprite was produced,
and return a pass/hold/reject verdict with specific findings. This is the same
Generator-Evaluator discipline used elsewhere in this adapter's guidance; it does not require a
dedicated named agent, just genuine independence from the generating session.

## Palette management

### List bundled palettes

```bash
python scripts/palette.py --list
```

Returns 30+ palettes grouped by category: hardware-authentic (`nes`, `gameboy-dmg`, `pico-8`),
Lospec-community (`db16`, `db32`, `aap-64`, `endesga-32`, `endesga-64`, `sweetie-16`,
`resurrect-64`, `apollo`, `steam-lords`, `slso8`), and cultural (`obangsaek` for Korean palettes,
`gugong-red-wall`/`qinghua`/`wuxing` for Chinese palettes, `stoneshard-inspired` for Russian dark
fantasy).

### Extract a palette from an image

```bash
python scripts/palette.py --extract photo.jpg --colors 16 --method median-cut
```

Methods: `kmeans` (slow, high quality), `median-cut` (default, balanced), `octree` (fast).

### Generate a hue-shifted ramp

```bash
python scripts/palette.py --ramp "#5b3a3a" --steps 5 --hue-shift 40
```

Generates a five-step ramp from dark to bright with proper hue rotation. Use this when a fresh
material color (skin tone, metal, leather) is needed without committing to a full palette.

## Cultural style guides (when relevant)

This module respects multiple cultural canons; match the request's stated style rather than
defaulting to one aesthetic. See `references/07-cultural-styles.md` for Chinese xianxia/wuxia,
Korean dot-graphic, Russian indie, and several named Western game-style anchors (Celeste, Hyper
Light Drifter, and others), including which bundled palette and animation timing convention each
implies.

## Mandatory rules (quality-checked)

1. No orphan pixels unless intentionally used as texture (sparkle, stippling) — default cap: 5%
   of total pixels.
2. No doublies — parallel double-thickness lines from an accidental brush stroke. Hard rule.
3. No pillow shading — dark border, light center, regardless of light source. Hard rule.
4. Palette stays within its stated cap — an `endesga-32` output must use at most 32 unique
   colors.
5. Hue rotation of at least 30° across any luminance ramp of four or more colors. Soft warning,
   not a hard error.
6. Selective anti-aliasing only — never on 45° lines, never on perfectly straight lines.
7. An outline, where present, is darker than the darkest object pixel.

## Gotchas

- Pillow's default palette quantization is median-cut; for better photo quality, use
  `LIBIMAGEQUANT` if `pyimagequant` is installed, otherwise median-cut is fine.
- GIF supports at most 256 colors and only 1-bit alpha (fully transparent or fully opaque). For
  semi-transparent animations, use APNG (better) or WebP (modern but inconsistent compatibility).
- A sub-pixel "anti-aliasing" trick animates the AA values between frames to suggest motion
  smaller than a pixel — looks professional but doubles the AA pixel budget.
- Chinese mobile games sometimes use a 5fps (200ms/frame) walk timing that reads as slow to a
  Western eye but is a documented standard — do not "fix" it without being asked.
- 45° lines never get anti-aliasing — a common mistake. AA belongs only on staircase patterns
  longer than one pixel.
- Indexed PNG is smaller and game-engine-friendly; RGBA preserves alpha. `render.py` defaults to
  RGBA.
- AI-generated pixel art is not pixel art — outputs from image-generation models need the
  `preprocess.py` pipeline; do not trust their pixel-grid alignment as-is.
- **`quality_check.py` crashes on an exact-block-size image with no upscale headroom.** Its block
  detector raises `ValueError: high <= 0` when an input's height or width exactly equals one of
  its candidate block sizes (32, 16, 12, 10, 8, 6, 4, 3, 2) with no integer upscale beyond that —
  for example, a plain, non-upscaled 16×16 PNG. This is an upstream bug (confirmed live during
  this port's functional testing; see `mappings/reviewed-scripts.yaml` for the exact repro), not
  something this adapter introduced or has fixed, since the script was ported unmodified.
  Workaround: render at a size with some headroom above the block sizes it checks (a logical grid
  rendered at 8× or larger avoids it) rather than at a size that lands exactly on one.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "Pillow not installed" | Missing dependency | `pip install Pillow` |
| Garbled output | Pixel coordinates outside the grid | Check `0 <= x < width`, `0 <= y < height` |
| Colors look wrong | Hex shorthand or named-color mismatch | Use full `#RRGGBB` hex |
| Image looks blurry | A non-nearest resample was used | Use nearest-neighbor resampling for pixel art |
| Quality score below 60 | Multiple quality issues | Read the full JSON output; common fixes: reduce the palette to ≤32 colors, remove orphan pixels, re-shade with a single light source |
| GIF has color bands | Limited 256-color quantization | Switch to APNG, or disable quantization |
| Animation jitters | Inconsistent pixel positions across frames | Run `quality_check.py --animation` to find the frame with mass deviation |
| Pillow shading detected | Anti-pattern shading | Re-shade with an explicit light source (default top-left); keep the darkest pixels only on the shadow side |
| Doublies detected | Two parallel single-pixel lines | Merge into one two-pixel line, or remove the redundant line |

## Reference index

| Topic | File |
|---|---|
| Drawing techniques (cluster, AA, jaggies, doublies, outlining) | `references/01-techniques.md` |
| Palette theory, dithering, banding | `references/02-palette-theory.md` |
| Shading, light, materials | `references/03-shading-materials.md` |
| Animation principles, frame counts, smear, sub-pixel | `references/04-animation.md` |
| Quality rubric and anti-AI-slop checklist | `references/05-quality-rubric.md` |
| Tools and libraries (Aseprite, Pillow, and others) | `references/06-tools-and-libraries.md` |
| Cultural styles (CN/KR/RU/Western) | `references/07-cultural-styles.md` |
| Extended JSON schema spec | `references/08-json-schema.md` |
