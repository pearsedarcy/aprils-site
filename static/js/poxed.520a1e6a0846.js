document.addEventListener('DOMContentLoaded', () => {
    
    // Mobile menu functionality
    document.getElementById('mobile-menu-button').addEventListener('click', function() {
        const mobileMenuContent = document.getElementById('mobile-menu-content');
        const menuButton = document.getElementById('mobile-menu-button');
        const spans = menuButton.getElementsByTagName('span');
        
        if (mobileMenuContent.style.transform === 'translateY(0%)') {
          // Close menu
            mobileMenuContent.style.transform = 'translateY(-100%)';
            mobileMenuContent.style.display = 'none';
          // Reset hamburger
          spans[0].style.transform = 'rotate(0) translateY(0)';
          spans[1].style.opacity = '1';
          spans[2].style.transform = 'rotate(0) translateY(0)';
        } else {
          // Open menu
            mobileMenuContent.style.transform = 'translateY(0%)';
            mobileMenuContent.style.display = 'block';
          // Create X
          spans[0].style.transform = 'rotate(45deg) translateY(6px)';
          spans[1].style.opacity = '0';
          spans[2].style.transform = 'rotate(-45deg) translateY(-6px)';
        }
    });
    
    // Dropdown menu functionality
    const dropdownButtons = document.querySelectorAll('#page-header button:has(svg)');
    
    dropdownButtons.forEach(button => {
        const nav = button.nextElementSibling;
        let isOpen = false;

        button.addEventListener('click', () => {
            isOpen = !isOpen;
            
            if (isOpen) {
                nav.style.display = 'block';
                setTimeout(() => {
                    nav.style.opacity = '1';
                    nav.style.height = 'auto';
                }, 10);
            } else {
                nav.style.opacity = '0';
                nav.style.height = '0';
                setTimeout(() => {
                    nav.style.display = 'none';
                }, 300); // Match transition duration
            }

            // Rotate arrow icon
            const svg = button.querySelector('svg');
            svg.style.transform = isOpen ? 'rotate(180deg)' : 'rotate(0)';
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        dropdownButtons.forEach(button => {
            const nav = button.nextElementSibling;
            if (!button.contains(e.target) && !nav.contains(e.target)) {
                nav.style.opacity = '0';
                nav.style.height = '0';
                setTimeout(() => {
                    nav.style.display = 'none';
                }, 300);
                button.querySelector('svg').style.transform = 'rotate(0)';
            }
        });
    });
});
