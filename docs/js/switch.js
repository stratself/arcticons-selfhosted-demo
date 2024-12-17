function switchIcon(iconID) {

    var iconTarget = document.getElementById(iconID);
    var iconAltList = iconTarget.dataset.alt.split(" ");
    var iconCurrentAlt = iconTarget.dataset.current;
    var iconCurrentAltIndex = iconAltList.indexOf(iconCurrentAlt);

    // calculate new alt icon
    var iconNewAltIndex = iconCurrentAltIndex + 1
    
    if (iconNewAltIndex > (iconAltList.length - 1)) {
        var iconNewAltIndex = 0;
    };
    iconNewAlt = iconAltList[iconNewAltIndex]
    var iconLinks = iconTarget.getElementsByClassName("iconLink");

    // change icon image
    var iconImg = iconTarget.getElementsByClassName('iconImage')[0];
    iconImg.src = iconImg.src.replace(`${iconCurrentAlt}.`,`${iconNewAlt}.`);

    // change icon URL
    for(let i = 0; i < iconLinks.length; i++) {
        iconLinks[i].href = iconLinks[i].href.replace(`${iconCurrentAlt}.`,`${iconNewAlt}.`);
    }

    // change current icon variable
    iconTarget.dataset.current = iconNewAlt

}