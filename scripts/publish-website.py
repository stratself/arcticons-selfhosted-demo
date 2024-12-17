import json 

iconRawUrl = 'https://raw.githubusercontent.com/skedastically/arcticons-selfhosted-demo/refs/heads/master'
siteTemplateFile = 'scripts/template/template.html'
iconTemplateFile = 'scripts/template/iconTemplate.html'
buttonToggleFile = "scripts/template/buttonToggleTemplate.html"
iconCategoryMap = 'newicons/appfilter.json'
websiteFile = 'docs/index.html'
svgLink = iconRawUrl + '/icons/white/svg/'
pngLink = iconRawUrl + '/icons/white/png/'
webpLink = iconRawUrl + '/icons/white/webp/'

def publishWebsite(siteTemplateFile, iconTemplateFile, iconCategoryMap, websiteFile, buttonToggleFile):
    
    tagmap = json.load(open(iconCategoryMap,"r"))
    icons = [i for i in tagmap]
    iconTemplate = open(iconTemplateFile,'r').read()
    iconDivs = ""
    categories = []

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
        for item in tagmap[icon]["categories"]:
            categories.append(item)

    buttonToggleTemplate = open(buttonToggleFile).read()
    buttonToggleDiv = ""
    categoriesSet = ("selfhosted","programming","distros","other")
    for category in categoriesSet:
        buttonToggle = buttonToggleTemplate.replace("{category}",category)
        buttonToggle = buttonToggle.replace("{categoryTitle}",category.title())
        buttonToggle = buttonToggle.replace("{categoryCount}",str(categories.count(category)))
        buttonToggleDiv = buttonToggleDiv + buttonToggle + '\n'

    iconWebsite = open(siteTemplateFile).read()
    iconWebsite = iconWebsite.replace("{iconCount}",str(len(icons)))
    
    index = iconWebsite.find('<div class="iconList">') + len('<div class="iconList">')
    iconWebsite = iconWebsite[:index] + iconDivs + iconWebsite[index:]

    index = iconWebsite.find('<div class="category-filters">') + len('<div class="category-filters">')
    iconWebsite = iconWebsite[:index] + "\n\t<text>Categories:</text>" + buttonToggleDiv + iconWebsite[index:]

    f = open(websiteFile,'w')
    print("Writing index.html")
    f.write(iconWebsite)
    f.close()
    print(f"Completed publishing website! {len(icons)} icons are generated")

if __name__ == "__main__":
    publishWebsite(siteTemplateFile,iconTemplateFile,iconCategoryMap,websiteFile,buttonToggleFile)