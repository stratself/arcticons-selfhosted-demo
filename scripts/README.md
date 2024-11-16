# Scripts

All scripts are to run from root directory of repository.

To prepare a release, run the following scripts in order:

## 1. generate-icons.py

Takes icons from `/newicons` and export them to svg, png, and webp files.

This script is a modified version of [`preparerelease.py`](https://github.com/Arcticons-Team/Arcticons/blob/main/scripts/preparerelease.py) found in the main repo.

## 2. list-icons.py

List all icons inside `icons/black/svg` and add them to `iconList.txt`.

## publish-website.py

Read from `iconList.txt` and add each icon as appropriate divs inside website.
