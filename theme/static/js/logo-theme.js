// theme/static/js/logo-theme.js
function updateLogoColors() {
  console.log('[logo-theme.js] updateLogoColors triggered (class-based)');
  // Find the SVG logo and test square
  const svg = document.querySelector('svg[aria-label="Sample SVG Logo"]');
  const colorTest = document.getElementById('theme-color-test');
  if (!svg || !colorTest) return;

  // Remove all color classes from previous theme
  svg.classList.remove(
    'bg-accent', 'bg-primary', 'bg-secondary', 'bg-neutral',
    'border-accent', 'border-primary', 'border-secondary', 'border-neutral',
    'text-primary-content', 'text-accent-content', 'text-neutral-content'
  );
  colorTest.classList.remove(
    'bg-accent', 'bg-primary', 'bg-secondary', 'bg-neutral',
    'border-accent', 'border-primary', 'border-secondary', 'border-neutral'
  );

  // Add new color classes for the current theme
  svg.classList.add('bg-accent', 'border-primary');
  colorTest.classList.add('bg-accent', 'border-primary');
}

document.addEventListener('DOMContentLoaded', updateLogoColors);

// Patch setTheme to also update logo colors
if (typeof window.setTheme === 'function') {
  const origSetTheme = window.setTheme;
  window.setTheme = function(theme) {
    origSetTheme(theme);
    setTimeout(updateLogoColors, 50);
  };
} else {
  window.setTheme = function(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    setTimeout(updateLogoColors, 50);
  };
} 