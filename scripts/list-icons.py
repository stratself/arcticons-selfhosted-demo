import os

ICONS_PATH = './icons/white/svg'
(ICON_LIST_PATH) = './icons/iconList.txt'
iconList = [i[:-4] for i in os.listdir(ICONS_PATH)]
print(f"There are {len(iconList)} icons")


with open(ICON_LIST_PATH, 'w') as f:
    for icon in iconList:
        f.write(f"{icon}\n")
    f.close()