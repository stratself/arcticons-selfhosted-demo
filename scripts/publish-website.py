import json 

iconRawUrl = 'https://raw.githubusercontent.com/skedastically/arcticons-selfhosted-demo/refs/heads/master'
siteTemplateFile = 'scripts/template/template.html'
iconTemplateFile = 'scripts/template/iconTemplate.html'
iconCategoryMap = 'newicons/appfilter.json'
websiteFile = 'docs/index.html'
svgLink = iconRawUrl + '/icons/white/svg/'
pngLink = iconRawUrl + '/icons/white/png/'
webpLink = iconRawUrl + '/icons/white/webp/'

def publishWebsite(siteTemplateFile, iconTemplateFile, iconCategoryMap, websiteFile):
    
    iconTemplate = open(iconTemplateFile,'r').read()
    tagmap = json.load(open(iconCategoryMap,"r"))
    icons = [i for i in tagmap]
    iconDivs = ""

    for icon in icons:
        print(f"Exporting {icon} to website")
        iconTitle = icon.title().replace("_"," ")
        iconDiv = iconTemplate.replace("{icon}",icon)
        iconDiv = iconDiv.replace("{iconCategories}",str(" ".join(tagmap[icon]["categories"])))
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
    publishWebsite(siteTemplateFile,iconTemplateFile,iconCategoryMap,websiteFile)