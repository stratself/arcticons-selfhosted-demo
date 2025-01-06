# Advanced usages

## Create your own Arcticons flavor

To create your own flavor, first clone the repo and prepare the environment.

Then, create a TOML file with a custom-defined section, something like this:

```toml
# Define each flavor in a section as below
# All paths are relative to this file's directory

[ arcticons-custom ]
name = "Custom mode"
size = 512 # Size of exported PNG/WEBP in pixels
color = "#639" # Color in hex

[ arcticons-custom.src ]
path = "newicons"

[ arcticons-custom.dst ]
# Define destination for each format
svg = "icons/custom/svg" # svgs will be copied
# png and webp will be generated according to size
png = "icons/custom/png"
webp = "icons/custom/webp"

# Add more sections for more flavors

# [ arcticons-white ]
# ...```

Place this config file at the root directory of the repo, as the referenced paths are **relative** to the file. Then run the `generate-icons.py` script referencing it:

```bash
uv run scripts/generate-icons.py -c generate-icons-custom.toml --nopreserve
```

The new files will be available.

## Selfhosting the icons

You may self-host this icon pack by exposing the contents of this repo via a web server e.g. Caddy or Nginx. By default they're the black and white flavors found in `/icons`.