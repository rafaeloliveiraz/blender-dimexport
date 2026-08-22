# Contributing

Thanks for your interest in improving **Blender DimExport**! 🎉

## Reporting bugs / ideas
- Open an [issue](../../issues) describing the problem or feature.
- For bugs, include your **Blender version**, OS, and steps to reproduce.

## Pull requests
1. Fork the repo and create a branch: `git switch -c my-feature`.
2. Keep the add-on a **single self-contained file** (`export_object_dimensions.py`) so it stays easy to install.
3. Test inside Blender (2.80+): install the add-on, run an export in each format (TXT/CSV/JSON).
4. Update `CHANGELOG.md` and bump the `version` in `bl_info` when relevant.
5. Open the PR describing what changed and why.

## Code style
- Follow standard Python (PEP 8) where reasonable.
- Prefer clear names and small helper functions.

All contributions of good faith are welcome. 💙
