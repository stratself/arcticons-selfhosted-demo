# Scripts

This project uses [uv](https://docs.astral.sh/uv/) to run Python commands. Dependencies are also noted in [`requirements.txt`](requirements.txt)

To prepare a release, run the following scripts from the root directory of the repo:

```bash
uv run ./scripts/generate-icons.py .
uv run ./scripts/check-icons.py icons/white/svg newicons/appfilter.json --sort
uv run ./scripts/publish-website.py
```

## 1. generate-icons.py

Takes icons from `/newicons` and export them to svg, png, and webp files.

This script is a modified version of [`preparerelease.py`](https://github.com/Arcticons-Team/Arcticons/blob/main/scripts/preparerelease.py) found in the main repo. It takes the following arguments:

- `-h, --help`: print help page
- `--checkonly`: do not create icon, check for their validity only
- `--new`: discard all entry in `newicons/generated/newdrawables.json` and rewrite them with all new SVGs. Suitable for new release.

## 2. check-icons.py

Validate the JSON category map (`appfilter.json`) and sort alphabetically with the `--sort` flag. Currently only checks for files with missing category or without a reference.

If an alert is raised, kindly fix the issue before proceeding.

## publish-website.py

Read from `appfilter.json` and add each icon as appropriate divs inside website.
