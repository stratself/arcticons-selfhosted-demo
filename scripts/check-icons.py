import os, argparse, json

parser = argparse.ArgumentParser()
parser.add_argument('ICONS_PATH', type=str, help='Path to the icons directory')
parser.add_argument('JSON_FILE', type=str, help='Path to the JSON file')

args = parser.parse_args()

def check_icons(icons_path, tagmap_path):
    print("Checking validity of JSON tagmap")
    tagmap = json.load(open(tagmap_path,"r"))
    icons = [i for i in tagmap]
    iconList = [i[:-4] for i in os.listdir(icons_path)]

    lostIcons = list(set(iconList) - set(icons))
    lostCategories = [ i for i in tagmap if len(tagmap[i]["categories"]) == 0 ]

    if len(lostIcons) > 0:
        print("WARN: The following icons are not found in tagmap:\n")
        [print(f'\t{lostIcon}.svg') for lostIcon in lostIcons]
        print('\n')
    if len(lostCategories) > 0:
        print("WARN: The following icons are not assigned a category:\n")
        [print(f'\t{lostCategory}.svg') for lostCategory in lostCategories]
        print('\n')

def main():
    check_icons(args.ICONS_PATH, args.JSON_FILE)
    
if __name__ == "__main__":
	main()
