siteTemplateFile = 'scripts/template/template.html'
iconTemplateFile = 'scripts/template/iconTemplate.html'
iconListFile = 'icons/iconList.txt'
websiteFile = 'docs/index.html'
svgLink = '../icons/white/svg/'
pngLink = '../icons/white/png/'
webpLink = '../icons/white/webp/'

def publishWebsite(siteTemplateFile, iconTemplateFile, iconListFile, websiteFile):
    iconTemplate = open(iconTemplateFile,'r').read()
    icons = open(iconListFile).read().split()
    iconDivs = ""

    for icon in icons:
        print(f"Exporting {icon} to website")
        iconTitle = icon.title().replace("_"," ")
        iconDiv = iconTemplate.replace("{icon}",icon)
        iconDiv = iconDiv.replace("{iconTitle}",iconTitle)
        iconDiv = iconDiv.replace("{svgLink}",svgLink)
        iconDiv = iconDiv.replace("{pngLink}",pngLink)
        iconDiv = iconDiv.replace("{webpLink}",webpLink)
        iconDivs = iconDivs + iconDiv

    iconWebsite = open(siteTemplateFile).read()

    index = iconWebsite.find('<div class="iconList">') + len('<div class="iconList">')

    iconWebsite = iconWebsite[:index] + iconDivs + iconWebsite[index:]

    f = open(websiteFile,'w')
    print("Writing index.html")
    f.write(iconWebsite)
    f.close()
    print("Completed!")

if __name__ == "__main__":
    publishWebsite(siteTemplateFile,iconTemplateFile,iconListFile,websiteFile)