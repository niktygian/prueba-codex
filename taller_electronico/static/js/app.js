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

const barcodeBtn = document.getElementById('barcodeBtn');
if (barcodeBtn) {
  barcodeBtn.addEventListener('click', () => {
    const input = document.getElementById('barcodeInput');
    const image = document.getElementById('barcodeImage');
    const value = (input.value || 'ORD-000001').trim();
    image.src = `/barcode/${encodeURIComponent(value)}.svg`;
  });
}
