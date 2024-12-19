function copyUrl(event) {
    event.preventDefault();
    navigator.clipboard.writeText(event.target.getAttribute('href')).then(() => {

      // Popup for three seconds then gone
      var popup = document.getElementById('popup');
      popup.style["visibility"]="visible";
      setTimeout(function(){popup.style["visibility"]="hidden";},3000);
    }, () => {
    });
}