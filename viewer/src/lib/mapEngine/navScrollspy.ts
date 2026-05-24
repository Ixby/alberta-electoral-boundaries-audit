// @ts-nocheck
// Alberta Electoral Boundary Audit — nav scroll-spy
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

export function initNavScrollspy(): void {
  const navLinks = Array.from(document.querySelectorAll('nav a[href^="#"]'));
  const sections = navLinks
    .map(a => { const h = a.getAttribute('href'); return (h && h.length > 1) ? document.querySelector(h) : null; })
    .filter(Boolean);

  function setActive(id) {
    navLinks.forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === '#' + id);
    });
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) setActive(entry.target.id);
    });
  }, { rootMargin: '-50px 0px -60% 0px', threshold: 0 });

  sections.forEach(s => observer.observe(s));
}
