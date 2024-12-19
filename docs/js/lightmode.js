function lightMode() {

  // change to light mode
  document.body.classList.toggle("light-mode");
  document.getElementsByClassName("searchBar")[0].classList.toggle("light-mode");
  // loop through all links and toggle replacement
  var links = document.getElementsByClassName("iconLink");
  for(let i = 0; i < links.length; i++) {
    if (links[i].href.includes("icons/white/")) {
      links[i].href = links[i].href.replace("icons/white/","icons/black/");
    }
    else if (links[i].href.includes("icons/black/")) {
      links[i].href = links[i].href.replace("icons/black/","icons/white/");
    }
  }

  // loop through all svgs and toggle replacement
  var images = document.getElementsByClassName("iconImage");
  for(let i = 0; i < images.length; i++) {
    if (images[i].src.includes("icons/white/")) {
      images[i].src = images[i].src.replace("icons/white/","icons/black/");
    }
    else if (images[i].src.includes("icons/black/")) {
      images[i].src = images[i].src.replace("icons/black/","icons/white/");
    }
  }

}