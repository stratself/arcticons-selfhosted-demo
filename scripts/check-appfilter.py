import os
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--nosort", action="store_true", help="Sort JSON keys alphabetically")
parser.add_argument("ICONS_PATH", type=str, help="Path to the icons directory")
parser.add_argument("JSON_FILE", type=str, help="Path to the JSON file")

args = parser.parse_args()


def check_icons(icons_path, categories_map_path):
    print("Checking validity of JSON categories map")
    categories_map = json.load(open(categories_map_path, "r"))

    icons = []
    for icon in categories_map:
        icons.append(icon)
        if "alts" in categories_map[icon]:
            [icons.append(alt) for alt in categories_map[icon]["alts"]]
    print("There are", len(icons), "icons in the category map")

    iconList = [i[:-4] for i in os.listdir(icons_path)]
    print("There are", len(iconList), "icons in folder")

    lostIcons = list(set(iconList) - set(icons))
    lostKeys = list(set(icons) - set(iconList))
    lostCategories = [
        i for i in categories_map if len(categories_map[i]["categories"]) == 0
    ]

    if len(lostIcons) > 0:
        print("WARN: The following icons are not found in the category map:\n")
        [print(f"\t{lostIcon}.svg") for lostIcon in lostIcons]
        print("\n")
    if len(lostKeys) > 0:
        print("WARN: The following keys do not have an icon associated with it:\n")
        [print(f"\t{lostKey}.svg") for lostKey in lostKeys]
        print("\n")
    if len(lostCategories) > 0:
        print("WARN: The following icons are not assigned a category:\n")
        [print(f"\t{lostCategory}.svg") for lostCategory in lostCategories]
        print("\n")

    if args.nosort:
        return
    print("Sorting JSON categories map")
    json.dump(
        categories_map, open(categories_map_path, "w"), indent=4, sort_keys=True
    )


def main():
    check_icons(args.ICONS_PATH, args.JSON_FILE)


if __name__ == "__main__":
    main()
