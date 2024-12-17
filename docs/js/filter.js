var displayedCategories = ["selfhosted", "other", "programming", "distros"];

function filter(className) {

    // edit displayedCategories list

    if (displayedCategories.includes(className)){
        displayedCategories = 
        displayedCategories.filter( 
            function(item){
                return item !== className
            }
        )
    }

    else if (displayedCategories.includes(className) == false){
        displayedCategories.push(className)
    };

    console.log(displayedCategories);

    // toggle button color
    var button = document.getElementById(`${className}-toggle`);
    button.classList.toggle("button-on");

    // display items with list categories
    var icons = document.querySelectorAll(`.iconPanel`);

    icons.forEach(function (icon) {

        var iconCategories = icon.dataset.categories.split(" ");

        if (iconCategories.some(iconCategory => displayedCategories.includes(iconCategory)) == false){
            console.log(displayedCategories);
            icon.classList.add("invisible");
        }

        else if (iconCategories.some(iconCategory => displayedCategories.includes(iconCategory))){
            console.log(displayedCategories);
            icon.classList.remove("invisible");
        };
    });


} 