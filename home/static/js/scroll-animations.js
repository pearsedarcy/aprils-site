const observerCallback = (entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
    }
  });
};

const observer = new IntersectionObserver(observerCallback, {
  threshold: 0.2
});

document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.fade-in-section');
  sections.forEach((section) => observer.observe(section));
});
