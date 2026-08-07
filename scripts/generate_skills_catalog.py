#!/usr/bin/env python3
"""Generate hermes/skills/README.md, a browsable catalog of every ported skill.

Mirrors upstream's skills/README.md + scripts/generate_skills_catalog.py convention:
one row per skill (name, link, description), grouped by category. Category is the
skill's parent directory name when it lives at hermes/skills/<category>/<name>/SKILL.md
(matching upstream's own category-subfolder layout), or "Core" when it lives directly
at hermes/skills/<name>/SKILL.md (most of this adapter's principle/rule-derived ports).

Run with --check to verify the file on disk is current without writing (CI-friendly);
without --check it regenerates the file.

A Russian translation, README_RU.md, is maintained by hand alongside this file — this
script only generates the English catalog, since translation needs judgment a mechanical
transform cannot provide.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "hermes" / "skills"
OUTPUT = SKILLS_ROOT / "README.md"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    fm = text[4:end]
    result: dict[str, str] = {}
    for line in fm.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip().strip('"')
    return result


def collect_skills() -> dict[str, list[tuple[str, str, str]]]:
    """Return {category: [(name, relative_skill_dir, description), ...]}."""
    by_category: dict[str, list[tuple[str, str, str]]] = {}
    for skill_md in sorted(SKILLS_ROOT.rglob("SKILL.md")):
        rel = skill_md.relative_to(SKILLS_ROOT)
        parts = rel.parts
        if len(parts) == 2:
            category = "Core"
            skill_dir = parts[0]
        elif len(parts) == 3:
            category = parts[0].replace("-", " ").title()
            skill_dir = f"{parts[0]}/{parts[1]}"
        else:
            continue
        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = fm.get("name", skill_dir.rsplit("/", 1)[-1])
        description = fm.get("description", "").strip()
        by_category.setdefault(category, []).append((name, skill_dir, description))
    for entries in by_category.values():
        entries.sort(key=lambda e: e[0])
    return by_category


def render(by_category: dict[str, list[tuple[str, str, str]]]) -> str:
    total = sum(len(v) for v in by_category.values())
    lines = [
        "# Skills Catalog",
        "",
        f"Generated from every `SKILL.md` under this directory ({total} skills as of the",
        "last regeneration). Regenerate with `python3 scripts/generate_skills_catalog.py`;",
        "verify it is current with `--check`.",
        "",
        "A Russian translation of this catalog is maintained by hand at `README_RU.md` —",
        "update it when adding or materially changing a skill listed here.",
        "",
        "## Install",
        "",
        "This adapter never installs directly into a live Hermes profile. Preview, then",
        "apply, into a disposable or real Hermes home with the adapter's own installer:",
        "",
        "```bash",
        "python3 scripts/install_hermes.py --dry-run --hermes-home /tmp/hermes-home",
        "python3 scripts/install_hermes.py --apply --hermes-home /tmp/hermes-home",
        "```",
        "",
        "This copies every skill below into `<hermes-home>/skills/config-kit/`, preserving",
        "the category layout shown here. Remove the same way with",
        "`scripts/remove_hermes.py --dry-run|--apply`.",
        "",
        "## Catalog",
        "",
    ]
    for category in sorted(by_category, key=lambda c: (c != "Core", c)):
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| Skill | Description |")
        lines.append("|---|---|")
        for name, skill_dir, description in by_category[category]:
            lines.append(f"| [{name}]({skill_dir}/) | {description} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify README.md is current; do not write")
    args = ap.parse_args()
    by_category = collect_skills()
    content = render(by_category)
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.is_file() else None
        if current != content:
            print("ERROR: hermes/skills/README.md is stale; run scripts/generate_skills_catalog.py", file=sys.stderr)
            return 1
        print("hermes/skills/README.md is current")
        return 0
    OUTPUT.write_text(content, encoding="utf-8")
    total = sum(len(v) for v in by_category.values())
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({total} skills, {len(by_category)} categories)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
