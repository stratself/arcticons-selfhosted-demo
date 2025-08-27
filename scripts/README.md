# Scripts

This project uses [uv](https://docs.astral.sh/uv/) to run Python commands. Dependencies are also noted in [`requirements.txt`](requirements.txt)

## Process for adding icons

To add icons to website, first check the icons' drawability and metadata to be correct. Please **run all commands from the root dir of this repo**.

```bash
uv sync --dev # sync dependencies

# check (not generate) all icons in ./newicons
uv run scripts/generate-icons.py --checksrc ./newicons --checkonly -e
# check appfilter JSON
uv run scripts/check-appfilter.py -c ./generate-icons.toml -e --nosort newicons/appfilter.json 
```

Then when all errors are resolved, run the following scripts, also from the repo's root directory:

```bash
# sort appfilter
uv run ./scripts/check-appfilter.py -c .\generate-icons.toml newicons/appfilter.json

# generate icons
uv run ./scripts/generate-icons.py -c generate-icons.toml --delete-after
```

After generating icons into the `./icons/**` paths, CI will automatically generate and publish new website. However you can also do it manually with `uv run ./scripts/publish-website.py`.

## Process for preparing a release

Every once in a while, let's do versioned releases. Use an annotated git tag and push it, the CI will take care of packaging.

```bash
git tag -a "0.3.3.2-beta"
git push --tag
```

## Script details

### 1. generate-icons.py

Takes icons from `/newicons` and export them to svg, png, and webp files.

This script is a heavily modified version of [`preparerelease.py`](https://github.com/Arcticons-Team/Arcticons/blob/main/scripts/preparerelease.py) found in the main repo. 

<details>

<summary>It takes the following arguments:</summary>

```
usage: generate-icons.py [-h] [-c CONFIG] [--checkonly] [--checksrc CHECKSRC] [--delete-after] [-e]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file to use
  --checkonly           Run checks only. Requires -c or --checksrc to be set
  --checksrc CHECKSRC   Path to the icons directory for checking (only enabled alongside --checkonly flag)
  --delete-after        Delete icons from the source folder after creation
  -e, --error           Errors on invalid checks
```

</details>

### 2. check-appfilter.py

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

### publish-website.py

Read from `appfilter.json` and add each icon as appropriate divs inside the website. This script requires a `site-config.json` file as found in the repo root.
