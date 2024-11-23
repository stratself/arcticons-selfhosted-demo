document.getElementById('searchBar').addEventListener('input', function (event) {
    const searchTerm = event.target.value.toLowerCase();
    const listIcons = document.querySelectorAll('.iconList .iconPanel');
    
    listIcons.forEach(function (icon) {
        const iconID = icon.id.toLowerCase();
        if (iconID.includes(searchTerm)) {
            icon.style.display = 'flex';
        } else {
            icon.style.display = 'none';
        }
    });
});
