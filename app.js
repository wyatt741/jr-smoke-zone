// JR Smoke Zone - age gate, mobile menu, theme toggle, scroll reveals.

// 21+ age gate: BOOT (in <head>) sets html[data-age="ok"] if already verified.
// "Yes" persists + reveals; "No" leaves the site.
(function () {
  const yes = document.getElementById('ag-yes');
  const no = document.getElementById('ag-no');
  if (yes) yes.addEventListener('click', () => {
    try { localStorage.setItem('age21', '1'); } catch (e) {}
    document.documentElement.setAttribute('data-age', 'ok');
  });
  if (no) no.addEventListener('click', () => { window.location.href = 'https://www.google.com'; });
})();

// Mobile menu
const burger = document.querySelector('.burger');
if (burger) {
  const toggle = (open) => { document.body.classList.toggle('menu-open', open); burger.setAttribute('aria-expanded', open); };
  burger.addEventListener('click', () => toggle(!document.body.classList.contains('menu-open')));
  document.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', () => toggle(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') toggle(false); });
}

// Theme toggle (dark default via BOOT script in <head>; choice persists)
document.querySelectorAll('.theme-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const dark = document.documentElement.getAttribute('data-theme') === 'dark';
    const next = dark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
});

// Scroll reveals
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
