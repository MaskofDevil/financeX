// Navbar Dropdown

const dropdownButton = document.getElementById('navbarDropdownMenu')
const dropdown = document.getElementsByClassName('navbar-dropdown-menu')[0]

dropdownButton.addEventListener('click', () => {
    dropdown.classList.toggle('active')
})