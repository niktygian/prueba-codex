document.querySelectorAll('form').forEach((f) => {
  f.addEventListener('submit', () => {
    const btn = f.querySelector('button[type="submit"], button:not([type])');
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Procesando...';
      setTimeout(() => (btn.disabled = false), 900);
    }
  });
});
