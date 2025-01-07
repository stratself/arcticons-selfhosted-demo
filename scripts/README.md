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

This script is a heavily modified version of [`preparerelease.py`](https://github.com/Arcticons-Team/Arcticons/blob/main/scripts/preparerelease.py) found in the main repo. 

<details>

<summary>It takes the following arguments:</summary>

```
usage: generate-icons.py [-h] [-c CONFIG] [--checkonly] [--checksrc CHECKSRC] [--nopreserve]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file to use
  --checkonly           Run checks only. Requires -c or --checksrc to be set
  --checksrc CHECKSRC   Path to the icons directory for checking (only enabled alongside --checkonly flag)
  --nopreserve          Remove icons after creation
```

</details>

## 2. check-appfilter.py

Validate the JSON category map (`appfilter.json`) against either 

- both src (default: ./newicons) and dst (default: ./icons/<flavor-name>/<format>) paths for each flavor inside config file, or
- a comma-separated list of formats

and auto-sort entries alphabetically. Currently only checks for files with missing category or without a reference.

If an alert is raised, kindly fix the issue before proceeding.


<details>
<summary>It takes the following arguments</summary>

```
usage: check-appfilter.py [-h] [--nosort] [-c CONFIG] [-p PATHS] JSON_APPFILTER

positional arguments:
  JSON_APPFILTER        Path to the JSON file

options:
  -h, --help            show this help message and exit
  --nosort              Sort JSON keys alphabetically
  -c CONFIG, --config CONFIG
                        Config file to use
  -p PATHS, --paths PATHS
                        Comma-separated paths to the icons directory
```

</details>

## publish-website.py

Read from `appfilter.json` and add each icon as appropriate divs inside website.
