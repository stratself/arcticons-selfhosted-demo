import os, argparse, json

parser = argparse.ArgumentParser()
parser.add_argument("--sort", action="store_true", help="Sort JSON keys alphabetically")
parser.add_argument('ICONS_PATH', type=str, help='Path to the icons directory')
parser.add_argument('JSON_FILE', type=str, help='Path to the JSON file')

args = parser.parse_args()

def check_icons(icons_path, categories_map_path):
    
    print("Checking validity of JSON categories map")
    categories_map = json.load(open(categories_map_path,"r"))
    icons = [i for i in categories_map]
    iconList = [i[:-4] for i in os.listdir(icons_path)]

    lostIcons = list(set(iconList) - set(icons))
    lostCategories = [ i for i in categories_map if len(categories_map[i]["categories"]) == 0 ]

    if len(lostIcons) > 0:
        print("WARN: The following icons are not found in categories_map:\n")
        [print(f'\t{lostIcon}.svg') for lostIcon in lostIcons]
        print('\n')
    if len(lostCategories) > 0:
        print("WARN: The following icons are not assigned a category:\n")
        [print(f'\t{lostCategory}.svg') for lostCategory in lostCategories]
        print('\n')
        
    if args.sort:
        print("Sorting JSON categories map")
        json.dump(categories_map,open(categories_map_path,"w"),indent=4,sort_keys=True)

def main():
    check_icons(args.ICONS_PATH, args.JSON_FILE)
    
if __name__ == "__main__":
	main()
