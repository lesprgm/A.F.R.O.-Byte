// script.js

// Toggle the mobile menu when the menu icon is clicked
document.getElementById('menu-icon').addEventListener('click', () => {
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('active');
});

// Optional: Close the menu when clicking outside of it (if applicable)
document.addEventListener('click', (event) => {
    const menuIcon = document.getElementById('menu-icon');
    const navbar = document.querySelector('.navbar');
    
    if (!navbar.contains(event.target) && !menuIcon.contains(event.target)) {
        navbar.classList.remove('active');
    }
});
