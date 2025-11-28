// Popup Triggers
document.querySelector('a[href="#about"]').addEventListener('click', (e) => {
  e.preventDefault();
  document.getElementById('aboutPopup').classList.add('active');
});

document.querySelector('a[href="#faq"]').addEventListener('click', (e) => {
  e.preventDefault();
  document.getElementById('faqPopup').classList.add('active');
});

document.querySelector('a[href="#contact"]').addEventListener('click', (e) => {
  e.preventDefault();
  document.getElementById('supportPopup').classList.add('active');
});

// Close Popups
document.querySelectorAll('.close-info').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.getAttribute('data-close');
    document.getElementById(target).classList.remove('active');
  });
});


