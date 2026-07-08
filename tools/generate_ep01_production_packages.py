#!/usr/bin/env python3
"""
Generate WUCHENG EP01 production packages.

This script expands production/EP01/shot_blueprint.csv into a full
per-shot package tree with:
README.md, camera.yaml, flux_prompt.md, motion_prompt.md, veo.md, kling.md,
hailuo.md, sound.md, timeline.md, review.md

Run from repository root:
    python tools/generate_ep01_production_packages.py
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "production" / "EP01" / "shot_blueprint.csv"
OUT = ROOT / "production" / "EP01" / "shots"

MASTER_STYLE = (
    "Photorealistic Kodak Vision3 35mm film look, anamorphic 2.39:1, "
    "muted blue-gray dawn palette with warm tungsten practical lighting, "
    "old repaired industrial harbor city, wet cobblestones, rust, coal dust, "
    "patched metal, worn wood, drifting steam, restrained HBO prestige drama tone."
)

NEGATIVE = (
    "cartoon, anime, CGI look, cyberpunk neon overload, futuristic holograms, "
    "modern buildings, modern vehicles, clean new materials, oversaturated colors, "
    "fast movement, handheld camera, shaky camera, text, subtitles, logo, watermark, "
    "hero pose, exaggerated acting, fantasy magic"
)


def safe_float(value: str) -> float:
    try:
        return float(value)
    except Exception:
        return 4.0


def read_rows():
    with BLUEPRINT.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def common_readme(row):
    return f"""# {row['shot_id']} — {row['title_cn']} / {row['title_en']}

Episode: S01E01
Package: {row['package']}
Status: READY_FOR_VIDEO
Duration: {row['duration']}s
Aspect Ratio: 2.39:1
FPS: 24

---

## Purpose

{row['core_action']}

## Visual Target

Use the WUCHENG Video Bible visual language: repaired industrial materials, damp air, restrained movement, realistic lighting, and no unnecessary spectacle.

## Next Action

Generate AI video v1 using the motion prompt and camera settings in this package, then submit for Director Review.
"""


def camera_yaml(row):
    return f"""shot_id: {row['shot_id']}
episode: S01E01
package: {row['package']}
aspect_ratio: "2.39:1"
fps: 24
duration_seconds: {safe_float(row['duration']):.1f}
lens: "{row['lens']}"
camera_type: "{row['camera']}"
movement:
  type: "static or minimal motivated movement"
  speed: "low"
  shake: "off"
  stabilization: "cinematic stable"
depth_of_field: "as required by lens and story focus"
lighting:
  key: "warm tungsten practicals where present"
  fill: "cold blue-gray ambient dawn or night"
  notes: "Keep lighting restrained and physically motivated."
weather:
  surface: "wet industrial materials"
  atmosphere: "steam, mist, dust, cold air"
"""


def flux_prompt(row):
    return f"""# {row['shot_id']} Flux First Frame Prompt

## Prompt

{row['core_action']} {MASTER_STYLE}

## Negative Prompt

{NEGATIVE}

## Consistency Notes

- Preserve WUCHENG material rule: everything looks used, repaired, and maintained.
- Do not introduce new worldbuilding not required by this shot.
- Keep the shot quiet, restrained, and production-realistic.
"""


def motion_prompt(row):
    return f"""# {row['shot_id']} Motion Prompt

{row['core_action']}

Motion should be restrained, physically believable, and motivated by character behavior or the city itself. Camera movement should remain static or nearly static unless the shot specifically requires movement. Steam, rain residue, fabric, small tools, and light should move naturally. Avoid spectacle.

## Motion Rules

- No fast movement unless specifically required.
- No handheld shake.
- No exaggerated acting.
- No AI-style floating objects.
- Maintain continuity with the previous and next shot in the same package.
"""


def veo_prompt(row):
    return f"""# {row['shot_id']} Veo Prompt

Create a {row['duration']}-second cinematic shot in 2.39:1. {row['core_action']} {MASTER_STYLE}

The motion must be subtle and physically realistic. Keep the atmosphere quiet and emotionally restrained. No text, no logo, no modern objects, no cyberpunk neon spectacle.

## Duration

{row['duration']} seconds

## Output Intent

Use as final-candidate AI video source for {row['shot_id']} in S01E01.
"""


def kling_prompt(row):
    return f"""# {row['shot_id']} Kling Prompt

{row['duration']}s cinematic shot. {row['core_action']} {MASTER_STYLE}

Camera: {row['camera']}. Lens: {row['lens']}. Motion strength low. Keep everything realistic, damp, repaired, and grounded.

## Avoid

{NEGATIVE}
"""


def hailuo_prompt(row):
    return f"""# {row['shot_id']} Hailuo Prompt

{row['duration']}s, 2.39:1, cinematic realism. {row['core_action']} {MASTER_STYLE}

## Avoid

{NEGATIVE}
"""


def sound_md(row):
    return f"""# {row['shot_id']} Sound Design

## Ambience

- Industrial harbor room tone
- Wind through repaired metal structures
- Distant steam release
- Wet street or interior resonance depending on location

## Foley

- Physically motivated small sounds matching the shot action
- Fabric, tools, wood, metal, water, footsteps, breath as appropriate

## Music Cue

No melody unless specifically required. Use silence and low texture first.

## Silence Notes

Let quiet carry tension. Do not over-score.
"""


def timeline_md(row):
    dur = safe_float(row["duration"])
    mid = dur / 2
    return f"""# {row['shot_id']} Timeline

## 0.0s

Establish the shot state and visual focus.

## {mid:.1f}s

Primary action or emotional beat occurs: {row['core_action']}

## {dur:.1f}s

Clean cut point into next shot.
"""


def review_md(row):
    return f"""# {row['shot_id']} Review

Status: READY_FOR_VIDEO

## Review Grid

| Category | Score |
|---|---:|
| Story | /20 |
| Camera | /20 |
| Art | /20 |
| Sound | /20 |
| Emotion | /20 |
| Total | /100 |

## Lock Criteria

- Shot fulfills its stated story purpose.
- Camera language matches WUCHENG Video Bible.
- No obvious AI artifacts.
- Materials look repaired and lived-in.
- Motion is restrained and physically believable.
- Cut point works within package: {row['package']}.

## Decision

WIP / REVIEW / LOCK
"""


FILES = {
    "README.md": common_readme,
    "camera.yaml": camera_yaml,
    "flux_prompt.md": flux_prompt,
    "motion_prompt.md": motion_prompt,
    "veo.md": veo_prompt,
    "kling.md": kling_prompt,
    "hailuo.md": hailuo_prompt,
    "sound.md": sound_md,
    "timeline.md": timeline_md,
    "review.md": review_md,
}


def main():
    rows = read_rows()
    OUT.mkdir(parents=True, exist_ok=True)

    for row in rows:
        shot_dir = OUT / row["shot_id"]
        shot_dir.mkdir(parents=True, exist_ok=True)
        for name, func in FILES.items():
            (shot_dir / name).write_text(func(row), encoding="utf-8")

    index_path = ROOT / "production" / "EP01" / "shot_index.csv"
    with index_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["shot_id", "title_cn", "title_en", "duration", "status", "package", "notes"])
        for row in rows:
            writer.writerow([row["shot_id"], row["title_cn"], row["title_en"], row["duration"], "READY_FOR_VIDEO", row["package"], row["core_action"]])

    print(f"Generated {len(rows)} shot packages under {OUT}")


if __name__ == "__main__":
    main()
