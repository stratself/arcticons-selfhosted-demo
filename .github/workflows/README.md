# Workflows

Arcticons-selfhosted uses a few automated CI/CD workflows.

## buildRelease.yml - build a new release

When a commit is tagged as a release (using `git tag <version>` and then `git push --tag`), run a github release with the following types of artifacts:

- `Arcticons-selfhosted-<version>.(zip|tar.gz)`: zip or tar.gz package of only icons for black and white flavor.
- `Arcticons-selfhosted-<flavor>-<version>.(zip|tar.gz)`: packages of each included flavor (currently there are 2: black and white)
- The changelog: currently just a total count of icons. In the future this may also point to a changelog file.

## newWebsite.yml - publish new website

When new icons are detected in the `/icons` directory, the website is regenerated again using `/scripts/build-website.py` with uv.

## preChecks.yml - pre-audit pull request

On new PRs, the workflow checks for whether the submitted icon is accounted for in the appfilter.json, and whether it meets standard SVG requirements (namely white strokes and 1px in width). Workflow failure 

This check is not automatically enabled due to email spam on runs. Newer solutions are considered.