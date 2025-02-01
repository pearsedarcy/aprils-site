document.addEventListener('DOMContentLoaded', () => {
    
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
