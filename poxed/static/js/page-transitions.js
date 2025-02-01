document.addEventListener('DOMContentLoaded', () => {
    const logoElement = document.getElementById('page-logo-tranny');
    const mainContent = document.querySelector('main');
    const transitionElement = document.querySelector('.main-transition');


    // Initial page load
    requestAnimationFrame(() => {
        mainContent.classList.add('loaded');
    });

    // Initial state
    transitionElement.classList.add('hidden');

    // Handle all internal link clicks
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link && link.href && link.href.startsWith(window.location.origin)) {
            e.preventDefault();
 
            
            transitionElement.classList.remove('hidden');
            requestAnimationFrame(() => {
                transitionElement.classList.add('active');
                logoElement.classList.add('show');
            });

            // After logo appears and grows
            setTimeout(() => {
                // Hide logo
                logoElement.classList.remove('show');
                logoElement.classList.add('hide');

                // After logo shrinks and fades
                setTimeout(() => {
                    // Start page transition
                    mainContent.classList.remove('loaded');
                    window.location.href = link.href;
                }, 200); // Logo exit duration
            }, 600); // Logo show duration
        }
    });

    // Handle page load completion
    window.addEventListener('pageshow', () => {
        logoElement.classList.remove('show', 'hide');
        transitionElement.classList.remove('active');
        transitionElement.classList.add('hidden');
        
        requestAnimationFrame(() => {
            mainContent.classList.add('loaded');
        });
    });
});