from jinja2 import Environment, FileSystemLoader
import json

# Load environment
config = json.loads(open('site-config.json').read())
appfilter = json.loads(open('newicons/appfilter.json').read())
environment = Environment(loader=FileSystemLoader(config['templatesDir']))

categories = []
icons = []

for icon in appfilter:
    icons.append(icon)
    for category in appfilter[icon]['categories']:
        categories.append(category)
    if "alts" in appfilter[icon]:
        for alt in appfilter[icon]["alts"]:
            icons.append(icon)
            categories.append(category)



for category in config['categories']:
    config['categories'][category]['count'] = categories.count(category)

config['iconCount'] = len(icons)

results_template = environment.get_template("index.html")
context = {
    "config": config,
    "appfilter": appfilter
}

with open(f"{config['dst']}/{config['pageName']}", mode="w", encoding="utf-8") as results:
    print("Generating webpage with the following config:")
    print(json.dumps(config, indent=4))
    results.write(results_template.render(context))
    print(f"... wrote {config['pageName']}")