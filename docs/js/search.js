document.getElementById('searchBar').addEventListener('input', function (event) {
    const searchTerm = event.target.value.toLowerCase();
    const listIcons = document.querySelectorAll('.iconList .iconPanel');
    
    listIcons.forEach(function (icon) {
        const iconName = icon.id.toLowerCase().replaceAll("_"," ");
        if (iconName.includes(searchTerm)) {
            icon.style.display = 'flex';
        } else {
            icon.style.display = 'none';
        }
    });
});

// Focus on searchbar when pressing '/'
const SearchBar = document.getElementById('searchBar')
document.addEventListener("keydown", focusSearch);
function focusSearch(event) {
    if ((event.key === 'k' || event.key === 'K') && event.ctrlKey) {
        SearchBar.focus();
        event.preventDefault();
        return false;
    }
}