# CODEX Project Engineering Guide

## Role

Codex acts as Project Engineer for WUCHENG. The job is to keep the production workspace organized, traceable, and ready for creative iteration without flattening the project's tone.

## Operating Principles

1. Preserve canon before expanding it.
2. Keep project files easy for a film team to scan.
3. Make every generated asset traceable to prompt, tool, source, owner, and status.
4. Separate draft exploration from approved production material.
5. Commit only scoped changes that match the current production task.

## Canon Order

1. Approved script drafts.
2. Current pilot outline.
3. Production handbook decisions.
4. Roadmaps and task notes.
5. Exploratory concept or prompt drafts.

## Naming Pattern

Use readable names that sort naturally:

`wucheng_<area>_<subject>_<version>.<ext>`

Examples:

- `wucheng_script_pilot_v01.md`
- `wucheng_storyboard_seq001_v01.png`
- `wucheng_concept_gray-harbor_street-vendor_v01.png`

## Asset Handling

Before an asset is used in production, update `assets/ASSET_INDEX.md` with:

- asset ID
- type
- title
- path or source
- status
- owner
- generation or capture notes
- rights and review state

## Commit Style

Use concise production-oriented commit messages. Example:

`feat: bootstrap WUCHENG production workspace`

## Sprint 1 Engineering Goal

Build enough structure that the team can move from pilot outline to script draft, storyboard pass, concept exploration, and asset tracking without losing provenance.
