import os
import argparse
import json
import tomllib
import jsonschema

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
parser.add_argument(
    "--nosort", action="store_true", help="Sort JSON keys alphabetically"
)
parser.add_argument("-c", "--config", type=str, help="Config file to use")
parser.add_argument(
    "-p", "--paths", type=str, help="Comma-separated paths to the icons directory"
)
parser.add_argument("JSON_APPFILTER", type=str, help="Path to the JSON file")

args = parser.parse_args()


def get_config(config_file: str, configSchema: dict):
    # Get config file and check their validity
    config = tomllib.load(open(config_file, "rb"))
    for i in config:
        jsonschema.validate(instance=config[i], schema=configSchema)
    return config


def check_icons(icons_paths: list, categories_map_path: str) -> None:
    print("Checking validity of JSON categories map")
    categories_map = json.load(open(categories_map_path, "r"))

    icons = []
    for icon in categories_map:
        icons.append(icon)
        if "alts" in categories_map[icon]:
            [icons.append(alt) for alt in categories_map[icon]["alts"]]
    print("There are", len(icons), "icons in the category map")

    iconList = []
    for icons_path in icons_paths:
        print(icons_path)
        iconsInPath = [icon[:-4] for icon in os.listdir(icons_path) if icon.endswith('.svg')]
        print("There are", len(iconsInPath), f"icons in {icons_path}")
        iconList += iconsInPath

    lostIcons = list(set(iconList) - set(icons))
    lostKeys = list(set(icons) - set(iconList))
    lostCategories = [
        i for i in categories_map if len(categories_map[i]["categories"]) == 0
    ]

    if len(lostIcons) > 0:
        print("::warning WARN: The following icons are not found in the category map:\n")
        [print(f"\t{lostIcon}.svg") for lostIcon in lostIcons]
        print("\n")
    if len(lostKeys) > 0:
        print("::warning WARN: The following keys do not have an icon associated with it:\n")
        [print(f"\t{lostKey}.svg") for lostKey in lostKeys]
        print("\n")
    if len(lostCategories) > 0:
        print("::warning WARN: The following icons are not assigned a category:\n")
        [print(f"\t{lostCategory}.svg") for lostCategory in lostCategories]
        print("\n")

    if args.nosort:
        return
    print("Sorting JSON categories map")
    json.dump(categories_map, open(categories_map_path, "w"), indent=4, sort_keys=True)
    return


def main():
    if args.config is not None:
        config = get_config(args.config, configSchema)
        paths = []
        for flavor in config:
            paths.append(config[flavor]["src"]["path"])
            # takes any first key that is a path
            firstKey = next(iter(config[flavor]["dst"]))
            paths.append(config[flavor]["dst"][firstKey])
        print(paths)
    elif args.paths is not None:
        paths = args.paths.split(",")
    else:
        print("Please supply paths or a config file")
        return
    check_icons(paths, args.JSON_APPFILTER)


if __name__ == "__main__":
    main()
