document.querySelectorAll('form').forEach((f) => {
  f.addEventListener('submit', () => {
    const btn = f.querySelector('button[type="submit"], button:not([type])');
    if (btn) {
      const oldText = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Procesando...';
      setTimeout(() => {
        btn.disabled = false;
        btn.textContent = oldText;
      }, 700);
    }
  });
});

const globalScan = document.getElementById('barcodeInputGlobal');
if (globalScan) {
  setTimeout(() => globalScan.focus(), 150);
  document.addEventListener('keydown', (e) => {
    if (!e.ctrlKey && !e.altKey && !e.metaKey && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      globalScan.focus();
    }
  });
}
