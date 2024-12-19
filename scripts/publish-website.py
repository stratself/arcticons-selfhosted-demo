import json
from bs4 import BeautifulSoup


iconRawUrl = "https://raw.githubusercontent.com/skedastically/arcticons-selfhosted-demo/refs/heads/master"
siteTemplateFile = "scripts/template/template.html"
iconTemplateFile = "scripts/template/iconTemplate.html"
buttonToggleFile = "scripts/template/buttonToggleTemplate.html"
iconSwitcherFile = "scripts/template/iconSwitcherTemplate.html"
iconCategoryMap = "newicons/appfilter.json"
websiteFile = "docs/index.html"
svgLink = iconRawUrl + "/icons/white/svg/"
pngLink = iconRawUrl + "/icons/white/png/"
webpLink = iconRawUrl + "/icons/white/webp/"


def publishWebsite(
    siteTemplateFile,
    iconTemplateFile,
    iconCategoryMap,
    websiteFile,
    buttonToggleFile,
    iconSwitcherFile,
):
    categories_map = json.load(open(iconCategoryMap, "r"))
    icons = [i for i in categories_map]
    iconTemplate = open(iconTemplateFile, "r").read()
    iconDivs = ""
    categories = []

    for icon in icons:
        print(f"Exporting {icon} to website")

        # Replace title, icon, categories, and links
        iconTitle = icon.title().replace("_", " ")
        iconDiv = iconTemplate.replace("{icon}", icon)
        iconDiv = iconDiv.replace(
            "{iconCategories}", str(" ".join(categories_map[icon]["categories"]))
        )
        iconDiv = iconDiv.replace("{iconTitle}", iconTitle)
        iconDiv = iconDiv.replace("{svgLink}", svgLink)
        iconDiv = iconDiv.replace("{pngLink}", pngLink)
        iconDiv = iconDiv.replace("{webpLink}", webpLink)

        # Check for existence of alts and add them to icon listing
        iconAlts = ""
        iconSwitcher = ""
        if "alts" in categories_map[icon]:
            iconAlts = (
                "data-alt='" + icon + " " + " ".join(categories_map[icon]["alts"]) + "'"
            )
            iconSwitcher = open(iconSwitcherFile, "r").read().replace("{icon}", icon)
            for alt in categories_map[icon]["alts"]:
                for item in categories_map[icon]["categories"]:
                    categories.append(item)

        iconDiv = iconDiv.replace("{iconAlts}", iconAlts)
        iconDiv = iconDiv.replace("{iconSwitcher}", iconSwitcher)

        # Compile final icon divs set
        iconDivs = iconDivs + iconDiv

        # Append category to count them later
        for item in categories_map[icon]["categories"]:
            categories.append(item)

    buttonToggleTemplate = open(buttonToggleFile).read()
    buttonToggleDiv = ""
    categoriesSet = ("selfhosted", "programming", "distros", "other")
    for category in categoriesSet:
        buttonToggle = buttonToggleTemplate.replace("{category}", category)
        buttonToggle = buttonToggle.replace("{categoryTitle}", category.title())
        buttonToggle = buttonToggle.replace(
            "{categoryCount}", str(categories.count(category))
        )
        buttonToggleDiv = buttonToggleDiv + buttonToggle + "\n"

    iconWebsite = open(siteTemplateFile).read()
    totalIcons = []
    for icon in icons:
        totalIcons.append(icon)
        if "alts" in categories_map[icon]:
            [totalIcons.append(alt) for alt in categories_map[icon]["alts"]]
    iconWebsite = iconWebsite.replace("{iconCount}", str(len(set(totalIcons))))
    iconWebsite = iconWebsite.replace("{iconDivs}", iconDivs)
    iconWebsite = iconWebsite.replace("{iconCategories}", buttonToggleDiv)
    iconWebsite = BeautifulSoup(iconWebsite, "html.parser").prettify()
    f = open(websiteFile, "w")
    print("Writing index.html")
    f.write(iconWebsite)
    f.close()
    print(f"Completed publishing website! {len(set(totalIcons))} icons are generated")


if __name__ == "__main__":
    publishWebsite(
        siteTemplateFile,
        iconTemplateFile,
        iconCategoryMap,
        websiteFile,
        buttonToggleFile,
        iconSwitcherFile,
    )
