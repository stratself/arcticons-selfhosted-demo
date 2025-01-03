# Scripts

This project uses [uv](https://docs.astral.sh/uv/) to run Python commands. Dependencies are also noted in [`requirements.txt`](requirements.txt)

To prepare a release, run the following scripts from the root directory of the repo:

```bash
uv sync --dev # sync dependencies
uv run ./scripts/generate-icons.py -c generate-config.toml --nopreserve
uv run ./scripts/check-icons.py icons/white/svg newicons/appfilter.json --sort
uv run ./scripts/publish-website.py
```

## 1. generate-icons.py

Takes icons from `/newicons` and export them to svg, png, and webp files.

This script is a heavily modified version of [`preparerelease.py`](https://github.com/Arcticons-Team/Arcticons/blob/main/scripts/preparerelease.py) found in the main repo. It takes the following arguments:
```
usage: gen.py [-h] [-c CONFIG] [--checkonly] [--checksrc CHECKSRC] [--nopreserve]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file to use
  --checkonly           Run checks only. Requires -c or --checksrc to be set
  --checksrc CHECKSRC   Path to the icons directory for checking (only enabled alongside --checkonly flag)
  --nopreserve          Remove icons after creation
```
## 2. check-icons.py

Validate the JSON category map (`appfilter.json`) and sort alphabetically with the `--sort` flag. Currently only checks for files with missing category or without a reference.

If an alert is raised, kindly fix the issue before proceeding.

## publish-website.py

Read from `appfilter.json` and add each icon as appropriate divs inside website.
