# Scripts

To prepare a release, run the following scripts from the root directory of the repo:

```bash
python3 ./scripts/generate-icons.py .
python3 ./scripts/list-icons.py
python3 ./scripts/publish-website.py
```

## 1. generate-icons.py

Takes icons from `/newicons` and export them to svg, png, and webp files.

This script is a modified version of [`preparerelease.py`](https://github.com/Arcticons-Team/Arcticons/blob/main/scripts/preparerelease.py) found in the main repo.

## 2. list-icons.py

List all icons inside `icons/black/svg` and add them to `iconList.txt`.

## publish-website.py

Read from `iconList.txt` and add each icon as appropriate divs inside website.
