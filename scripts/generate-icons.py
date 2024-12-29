from shutil import copy2
from typing import List
from PIL import Image
import os
import io
import re
import glob
import cairosvg
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--checkonly", action="store_true", help="Run checks only")
parser.add_argument("--new", action="store_true", help="Run a new Release")
parser.add_argument("ARCTICONS_DIR", type=str, help="Path to the Arcticons directory")

args = parser.parse_args()

ARCTICONS_DIR = os.path.abspath(args.ARCTICONS_DIR)


def check_arcticons_path(path):
    # Check if the given path includes "Arcticons" folder or if it is one level below
    arcticons_folder = os.path.join(path, "Arcticons-selfhosted")
    if os.path.exists(arcticons_folder) and os.path.isdir(arcticons_folder):
        return arcticons_folder
    else:
        app_folder = os.path.join(path, "app")
        other_folder = os.path.join(path, "other")
        if (
            os.path.exists(other_folder)
            and os.path.isdir(other_folder)
            and os.path.exists(app_folder)
            and os.path.isdir(app_folder)
        ):
            return path
        else:
            print(
                f"The path '{path}' does not include the 'Arcticons-selfhosted' folder."
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


ARCTICONS_PATH = check_arcticons_path(ARCTICONS_DIR)

# Define Path
NEWICONS_PATH = ARCTICONS_PATH + "/newicons"
ICONS_PATH = ARCTICONS_PATH + "/icons"
NEWDRAWABLE_PATH = ARCTICONS_PATH + "/newicons/generated/newdrawables.json"
WHITE_DIR = ICONS_PATH + "/white/svg"
BLACK_DIR = ICONS_PATH + "/black/svg"
EXPORT_DARK_DIR = ICONS_PATH + "/white/webp"
EXPORT_LIGHT_DIR = ICONS_PATH + "/black/webp"
EXPORT_DARK_DIR_PNG = ICONS_PATH + "/white/png"
EXPORT_LIGHT_DIR_PNG = ICONS_PATH + "/black/png"

# Export Sizes of the icons
SIZES = [256]
# Define original color
ORIGINAL_STROKE = r"stroke\s*:\s*(#FFFFFF|#ffffff|#fff|white|rgb\(255,255,255\)|rgba\(255,255,255,1\.?\d*\))"
ORIGINAL_STROKE_ALT = r"stroke\s*=\"\s*(#FFFFFF|#ffffff|#fff|white|rgb\(255,255,255\)|rgba\(255,255,255,1\.?\d*\))\""
ORIGINAL_FILL = r"fill\s*:\s*(#FFFFFF|#ffffff|#fff|white|rgb\(255,255,255\)|rgba\(255,255,255,1\.?\d*\))"
ORIGINAL_FILL_ALT = r"fill\s*=\"\s*(#FFFFFF|#ffffff|#fff|white|rgb\(255,255,255\)|rgba\(255,255,255,1\.?\d*\))\""
# Define Replace Colors
REPLACE_STROKE_WHITE = "stroke:#fff"
REPLACE_STROKE_WHITE_ALT = '''stroke="#fff"'''
REPLACE_FILL_WHITE = "fill:#fff"
REPLACE_FILL_WHITE_ALT = '''fill="#fff"'''
REPLACE_STROKE_BLACK = "stroke:#000"
REPLACE_STROKE_BLACK_ALT = '''stroke="#000"'''
REPLACE_FILL_BLACK = "fill:#000"
REPLACE_FILL_BLACK_ALT = '''fill="#000"'''

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
    for x in glob.glob(f"{dir}/*.svg"):
        with open(x, "r") as fp:
            content = fp.read()

        content = re.sub(stroke, replace_stroke, content, flags=re.IGNORECASE)
        content = re.sub(fill, replace_fill, content, flags=re.IGNORECASE)
        content = re.sub(stroke_alt, replace_stroke_alt, content, flags=re.IGNORECASE)
        content = re.sub(fill_alt, replace_fill_alt, content, flags=re.IGNORECASE)

        with open(x, "w") as fp:
            fp.write(content)


# Create PNG of the SVG and Copy to destination
def create_icons(
    sizes: List[int],
    dir: str,
    export_dir: str,
    export_dir_png: str,
    icon_dir: str,
    mode: str,
):
    print(f"Working on {mode}")
    for file_path in glob.glob(f"{dir}/*.svg"):
        file = os.path.basename(file_path)
        name = file[:-4]
        copy2(file_path, f"{icon_dir}/{file}")
        for size in sizes:
            try:
                # Convert SVG to PNG
                png_data = cairosvg.svg2png(
                    url=file_path,
                    output_width=size,
                    output_height=size,
                )

                # Open the PNG image from the in-memory data
                image = Image.open(io.BytesIO(png_data))

                # Convert and save it as WebP
                image.save(export_dir + f"/{name}.webp", format="WEBP")

                # Convert and save it as PNG
                image.save(export_dir_png + f"/{name}.png", format="PNG")

            except Exception as e:
                print(f"Error: {e}")


def remove_svg(dir: str):
    for file_path in glob.glob(f"{dir}/*.svg"):
        os.remove(file_path)


###### Checks ######


# Check Icons
def checkSVG(dir: str):
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
        print("\n\n______ Found SVG with wrong line attributtes ______\n")
        for svg in strokeattr:
            print(f"\n{svg}:")
            for attr in strokeattr[svg]:
                print(f"\t {attr}")

        print("\n\n____ Please check these first before proceeding ____\n\n")
        return True
    return False


###### Main #####
# runs everything in necessary order
def main():
    if checkSVG(NEWICONS_PATH):
        return
    if args.checkonly:
        return
    create_new_drawables(NEWICONS_PATH, NEWDRAWABLE_PATH)
    svg_colors(
        NEWICONS_PATH,
        ORIGINAL_STROKE,
        ORIGINAL_FILL,
        ORIGINAL_STROKE_ALT,
        ORIGINAL_FILL_ALT,
        REPLACE_STROKE_WHITE,
        REPLACE_FILL_WHITE,
        REPLACE_STROKE_WHITE_ALT,
        REPLACE_FILL_WHITE_ALT,
    )
    create_icons(
        SIZES,
        NEWICONS_PATH,
        EXPORT_DARK_DIR,
        EXPORT_DARK_DIR_PNG,
        WHITE_DIR,
        "Dark Mode",
    )
    svg_colors(
        NEWICONS_PATH,
        ORIGINAL_STROKE,
        ORIGINAL_FILL,
        ORIGINAL_STROKE_ALT,
        ORIGINAL_FILL_ALT,
        REPLACE_STROKE_BLACK,
        REPLACE_FILL_BLACK,
        REPLACE_STROKE_BLACK_ALT,
        REPLACE_FILL_BLACK_ALT,
    )
    create_icons(
        SIZES,
        NEWICONS_PATH,
        EXPORT_LIGHT_DIR,
        EXPORT_LIGHT_DIR_PNG,
        BLACK_DIR,
        "Light Mode",
    )
    remove_svg(NEWICONS_PATH)


if __name__ == "__main__":
    main()
