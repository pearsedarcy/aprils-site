// theme/static/js/logo-theme.js
function updateLogoColors() {
  console.log('[logo-theme.js] updateLogoColors triggered');
  // Find the SVG logo (adjust selector as needed)
  const svg = document.querySelector('svg[aria-label="Sample SVG Logo"]');
  if (!svg) return;

  // Get computed CSS variables for the current theme
  const styles = getComputedStyle(document.documentElement);

  // Log the CSS variable values
  const b1 = styles.getPropertyValue('--b1').trim();
  const p = styles.getPropertyValue('--p').trim();
  const pc = styles.getPropertyValue('--pc').trim();
  console.log('[logo-theme.js] CSS vars:', { b1, p, pc });

  // Update SVG elements with CSS variables, fallback to classes if needed
  const circle = svg.querySelector('circle');
  const rect = svg.querySelector('rect');
  const text = svg.querySelector('text');
  if (circle) {
    if (b1 && p) {
      circle.setAttribute('fill', b1);
      circle.setAttribute('stroke', p);
    } else {
      circle.setAttribute('fill', '#38bdf8'); // fallback color
      circle.setAttribute('stroke', '#6366f1');
    }
  }
  if (rect) {
    if (p) {
      rect.setAttribute('fill', p);
    } else {
      rect.setAttribute('fill', '#6366f1');
    }
  }
  if (text) {
    if (pc) {
      text.setAttribute('fill', pc);
    } else {
      text.setAttribute('fill', '#fff');
    }
  }
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