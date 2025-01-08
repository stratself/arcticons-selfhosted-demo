from PIL import Image
import os
import io
import re
import glob
import cairosvg
import argparse
import json
import jsonschema
import tomllib

configSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "size": {"type": "integer"},
        "color": {"type": "string"},
        "src": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
            "additionalProperties": False,
        },
        "dst": {
            "type": "object",
            "properties": {
                "svg": {"type": "string"},
                "png": {"type": "string"},
                "webp": {"type": "string"},
            },
            "minProperties": 1,
            "additionalProperties": False,
        },
    },
    "required": ["size", "color", "src", "dst"],
}

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, help="Config file to use")
parser.add_argument("--checkonly", action="store_true", help="Run checks only. Requires -c or --checksrc to be set")
parser.add_argument(
    "--checksrc",
    type=str,
    help="Path to the icons directory for checking (only enabled alongside --checkonly flag)",
)
parser.add_argument(
    "--nopreserve",
    action="store_true",
    help="Remove icons after creation",
)

args = parser.parse_args()


def get_config(config_file: str, configSchema: dict):
    # Get config file and check their validity
    config = tomllib.load(open(config_file, "rb"))
    for i in config:
        jsonschema.validate(instance=config[i], schema=configSchema)
    return config


def check_arcticons_path(path):
    # Check if the given path includes "Arcticons" folder or if it is one level below
    arcticons_folder = os.path.join(path, "arcticons-selfhosted-demo")
    if os.path.exists(arcticons_folder) and os.path.isdir(arcticons_folder):
        return arcticons_folder
    else:
        app_folder = os.path.join(path, "app")
        newicons_folder = os.path.join(path, "newicons")
        if (
            os.path.exists(newicons_folder)
            and os.path.isdir(newicons_folder)
            and os.path.exists(app_folder)
            and os.path.isdir(app_folder)
        ):
            return path
        else:
            print(
                f"The path '{path}' does not include the 'arcticons-selfhosted' folder."
            )
            while True:
                user_input = input("Do you want to continue? (y/n): ").lower()
                if user_input == "y":
                    break
                elif user_input == "n":
                    exit()  # or raise an exception or take appropriate action
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
    return path


# Define original color
ORIGINAL_STROKE = r"stroke\s*:\s*(#FFFFFF|#ffffff|#fff|white|rgb\(255,255,255\)|rgba\(255,255,255,1\.?\d*\))"
ORIGINAL_STROKE_ALT = r"stroke\s*=\"\s*(#FFFFFF|#ffffff|#fff|white|rgb\(255,255,255\)|rgba\(255,255,255,1\.?\d*\))\""
ORIGINAL_FILL = r"fill\s*:\s*(#FFFFFF|#ffffff|#fff|white|rgb\(255,255,255\)|rgba\(255,255,255,1\.?\d*\))"
ORIGINAL_FILL_ALT = r"fill\s*=\"\s*(#FFFFFF|#ffffff|#fff|white|rgb\(255,255,255\)|rgba\(255,255,255,1\.?\d*\))\""

##### Iconpack stuff #####


def create_new_drawables(svgdir: str, newdrawables: str) -> None:
    # Create newdrawables.txt file
    data = json.load(open(newdrawables))

    # populate newDrawables list
    newDrawables = []
    if not args.new:
        newDrawables = json.load(open(newdrawables))["new"]

    for file_path in glob.glob(f"{svgdir}/*.svg"):
        file = os.path.basename(file_path)
        name = file[:-4]
        newDrawables.append(name)

    # return sorted unique list of newDrawables
    newDrawables = list(sorted(set(newDrawables)))
    data["new"] = newDrawables
    # Write to json
    if os.path.exists(newdrawables):
        os.remove(newdrawables)

    with open(newdrawables, "w") as fp:
        json.dump(data, fp, indent=4, sort_keys=True)

    print(f"There are {len(newDrawables)} new icons")


# Change Color of SVG based on rules
def svg_colors(
    dir: str,
    stroke: str,
    fill: str,
    stroke_alt: str,
    fill_alt: str,
    replace_stroke: str,
    replace_fill: str,
    replace_stroke_alt: str,
    replace_fill_alt: str,
) -> None:
    generatedData: dict = {}
    for file_path in glob.glob(f"{dir}/*.svg"):
        file = os.path.basename(file_path)
        name = file[:-4]
        with open(file_path, "r") as fp:
            content = fp.read()
        file = os.path.basename(file_path)
        content = re.sub(stroke, replace_stroke, content, flags=re.IGNORECASE)
        content = re.sub(fill, replace_fill, content, flags=re.IGNORECASE)
        content = re.sub(stroke_alt, replace_stroke_alt, content, flags=re.IGNORECASE)
        content = re.sub(fill_alt, replace_fill_alt, content, flags=re.IGNORECASE)
        generatedData[name] = content
    return generatedData


# Create PNG of the SVG and Copy to destination
def create_icons(
    generatedData: dict,
    size: str,
    export_dir_svg: str,
    export_dir_png: str,
    export_dir_webp: str,
    mode: str,
):
    print(f"Working on {mode}")
    for icon in generatedData:
        content = generatedData[icon]
        if export_dir_svg is not None:
            if os.path.exists(export_dir_svg) is not True:
                os.makedirs(export_dir_svg)
            with open(f"{export_dir_svg}/{icon}.svg", "w") as fp:
                fp.write(content)
        try:
            # Convert SVG to PNG
            png_data = cairosvg.svg2png(
                bytestring=content,
                output_width=size,
                output_height=size,
            )

            # Open the PNG image from the in-memory data
            image = Image.open(io.BytesIO(png_data))

            # Convert and save it as PNG
            if export_dir_png is not None:
                if os.path.exists(export_dir_png) is not True:
                    os.makedirs(export_dir_png)

            # Convert and save it as WebP
            image.save(export_dir_png + f"/{icon}.png", format="PNG")
            if export_dir_webp is not None:
                if os.path.exists(export_dir_webp) is not True:
                    os.makedirs(export_dir_webp)
                image.save(export_dir_webp + f"/{icon}.webp", format="WEBP")

        except Exception as e:
            print(f"Error: {e}")


def remove_svg(dir: str):
    for file_path in glob.glob(f"{dir}/*.svg"):
        os.remove(file_path)


###### Checks ######


# Check Icons
def checkSVG(dir: str):
    print(f"Checking drawability of icons in {dir}")
    def replace_stroke(match):
        strokestr = match.group("strokestr")
        stroke_width = float(match.group("number"))
        if stroke_width > 0.9 and stroke_width < 1.2:
            return f"{strokestr}1"
        elif stroke_width >= 0 and stroke_width < 0.3:
            return f"{strokestr}0"
        else:
            return f"{strokestr}{stroke_width}"

    strokeattr = {}
    for file_path in glob.glob(f"{dir}/*.svg"):
        file = os.path.basename(file_path)
        name = file[:-4]
        with open(file_path, "r", encoding="utf-8") as fp:
            content = fp.read()
            content = re.sub(
                r'(?P<strokestr>stroke-width(?:="|: ?))(?P<number>\d*(?:.\d+)?)(?=[p"; }\/])',
                replace_stroke,
                content,
            )

            # check colors regex
            stroke_colors = re.findall(
                r"stroke(?:=\"|:)(?:rgb[^a]|#).*?(?=[\"; ])", content
            )
            fill_colors = re.findall(
                r"fill(?:=\"|:)(?:rgb[^a]|#).*?(?=[\"; ])", content
            )
            stroke_opacities = re.findall(
                r"stroke-opacity(?:=\"|:).*?(?=[\"; ])", content
            )
            fill_opacities = re.findall(r"fill-opacity(?:=\"|:).*?(?=[\"; ])", content)
            stroke_rgbas = re.findall(r"stroke(?:=\"|:)rgba.*?(?=[\"; ])", content)
            fill_rgbas = re.findall(r"fill(?:=\"|:)rgba.*?(?=[\"; ])", content)

            # Other Attributes regex
            strokes = re.findall(r"stroke-width(?:=\"|:).*?(?=[\"; ])", content)
            linecaps = re.findall(r"stroke-linecap(?:=\"|:).*?(?=[\";}])", content)
            linejoins = re.findall(r"stroke-linejoin(?:=\"|:).*?(?=[\";}])", content)
            # Write the updated content back to the file
            with open(file_path, "w", encoding="utf-8") as output_file:
                output_file.write(content)
            # colors
            for stroke_color in stroke_colors:
                if stroke_color not in [
                    "stroke:#ffffff",
                    "stroke:#fff",
                    "stroke:#FFFFFF",
                    'stroke="#fff',
                    'stroke="#ffffff',
                    'stroke="#FFFFFF',
                    'stroke="white',
                    "stroke:rgb(255,255,255)",
                    'stroke="rgb(255,255,255)',
                ]:
                    if file in strokeattr:
                        strokeattr[file] += [stroke_color]
                    else:
                        strokeattr[file] = [stroke_color]
            for fill_color in fill_colors:
                if fill_color not in [
                    "fill:#ffffff",
                    "fill:#fff",
                    "fill:#FFFFFF",
                    'fill="#ffffff',
                    'fill="#fff',
                    'fill="#FFFFFF',
                    'fill="white',
                    "fill:rgb(255,255,255)",
                    'fill="rgb(255,255,255)',
                ]:
                    if file in strokeattr:
                        strokeattr[file] += [fill_color]
                    else:
                        strokeattr[file] = [fill_color]
            for stroke_opacity in stroke_opacities:
                if stroke_opacity not in [
                    'stroke-opacity="0',
                    'stroke-opacity="0%',
                    'stroke-opacity="1',
                    'stroke-opacity="100%',
                    "stroke-opacity:1",
                    "stroke-opacity:0",
                ] and not re.findall(r"stroke-opacity[=:]\"?[01]\.0+$", stroke_opacity):
                    if file in strokeattr:
                        strokeattr[file] += [stroke_opacity]
                    else:
                        strokeattr[file] = [stroke_opacity]
            for fill_opacity in fill_opacities:
                if fill_opacity not in [
                    'fill-opacity="0',
                    'fill-opacity="0%',
                    'fill-opacity="1',
                    'fill-opacity="100%',
                    "fill-opacity:0",
                    "fill-opacity:1",
                ] and not re.findall(r"fill-opacity[=:]\"?[01]\.0+$", fill_opacity):
                    if file in strokeattr:
                        strokeattr[file] += [fill_opacity]
                    else:
                        strokeattr[file] = [fill_opacity]
            for stroke_rgba in stroke_rgbas:
                stroke_rgba_color, stroke_rgba_opacity = stroke_rgba.rsplit(",", 1)
                if stroke_rgba_color not in [
                    "stroke:rgba(255,255,255",
                    'stroke="rgba(255,255,255',
                ] or float(stroke_rgba_opacity[:-1]) not in [0.0, 1.0]:
                    if file in strokeattr:
                        strokeattr[file] += [stroke_rgba]
                    else:
                        strokeattr[file] = [stroke_rgba]
            for fill_rgba in fill_rgbas:
                fill_rgba_color, fill_rgba_opacity = fill_rgba.rsplit(",", 1)
                if fill_rgba_color not in [
                    "fill:rgba(255,255,255",
                    'fill="rgba(255,255,255',
                ] or float(fill_rgba_opacity[:-1]) not in [0.0, 1.0]:
                    if file in strokeattr:
                        strokeattr[file] += [fill_rgba]
                    else:
                        strokeattr[file] = [fill_rgba]
            # Other Attributes
            for stroke in strokes:
                if stroke not in [
                    "stroke-width:1",
                    "stroke-width:1px",
                    "stroke-width:0px",
                    "stroke-width:0",
                    'stroke-width="1',
                    'stroke-width="1px',
                    'stroke-width="0',
                ]:
                    if file in strokeattr:
                        strokeattr[file] += [stroke]
                    else:
                        strokeattr[file] = [stroke]
            for linecap in linecaps:
                if linecap not in [
                    "stroke-linecap:round",
                    'stroke-linecap="round',
                    "stroke-linecap: round",
                ]:
                    if file in strokeattr:
                        strokeattr[file] += [linecap]
                    else:
                        strokeattr[file] = [linecap]
            for linejoin in linejoins:
                if linejoin not in [
                    "stroke-linejoin:round",
                    'stroke-linejoin="round',
                    "stroke-linejoin: round",
                ]:
                    if file in strokeattr:
                        strokeattr[file] += [linejoin]
                    else:
                        strokeattr[file] = [linejoin]

    if len(strokeattr) > 0:
        print("\n\n::warn ______ Found SVG with wrong line attributtes ______\n")
        for svg in strokeattr:
            print(f"\n{svg}:")
            for attr in strokeattr[svg]:
                print(f"\t {attr}")

        print("\n\n::warn ____ Please check these first before proceeding ____\n\n")
        return True
    return False


# Check Icons


###### Main #####
# runs everything in necessary order
def main():
    if args.config is not None:
        CONFIG = get_config(args.config, configSchema)
    elif args.checksrc is not None and args.checkonly is True:
        checkSVG(args.checksrc)
        return
    else:
        raise ValueError("Please provide paths or a config file")
        return

    ARCTICONS_DIR = os.path.dirname(
        os.path.abspath(args.config)
    )
    #check_arcticons_path(ARCTICONS_DIR)

    for flavor in CONFIG:
        print(flavor)
        NEWICONS_PATH = CONFIG[flavor]["src"]["path"]
        MODE = flavor + ' - ' + CONFIG[flavor]["name"]
        SIZE = CONFIG[flavor]["size"]
        COLOR = CONFIG[flavor]["color"]
        REPLACE_STROKE = f"stroke:{COLOR}"
        REPLACE_STROKE_ALT = f'''stroke="{COLOR}"'''
        REPLACE_FILL = f"fill:{COLOR}"
        REPLACE_FILL_ALT = f'''fill="{COLOR}"'''
        
        checkSVG(NEWICONS_PATH)

        if args.checkonly:
            continue
                   
        try:
            EXPORT_DIR_SVG = CONFIG[flavor]["dst"]["svg"]
        except KeyError:
            EXPORT_DIR_SVG = None
        try:
            EXPORT_DIR_PNG = CONFIG[flavor]["dst"]["png"]
        except KeyError:
            EXPORT_DIR_PNG = None
        try:
            EXPORT_DIR_WEBP = CONFIG[flavor]["dst"]["webp"]
        except KeyError:
            EXPORT_DIR_WEBP = None

        data = svg_colors(
            NEWICONS_PATH,
            ORIGINAL_STROKE,
            ORIGINAL_FILL,
            ORIGINAL_STROKE_ALT,
            ORIGINAL_FILL_ALT,
            REPLACE_STROKE,
            REPLACE_FILL,
            REPLACE_STROKE_ALT,
            REPLACE_FILL_ALT,
        )

        create_icons(data, SIZE, EXPORT_DIR_SVG, EXPORT_DIR_PNG, EXPORT_DIR_WEBP, MODE)
        print(f"There are {len(data)} new icons")
    for flavor in CONFIG:
        if args.nopreserve:
            remove_svg(NEWICONS_PATH)


if __name__ == "__main__":
    main()
