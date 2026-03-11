const isTypingField = (el) => el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT');

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
}

// Atajos globales para operar sin mouse
window.addEventListener('keydown', (e) => {
  const active = document.activeElement;
  if (e.ctrlKey && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    globalScan?.focus();
    globalScan?.select();
  }

  if (e.ctrlKey && e.key.toLowerCase() === 'n') {
    const form = document.getElementById('nuevaOrdenForm');
    if (form) {
      e.preventDefault();
      const first = form.querySelector('select, input, textarea');
      first?.focus();
    }
  }

  if (e.ctrlKey && e.key.toLowerCase() === 'b') {
    const search = document.getElementById('searchOrdenes');
    if (search) {
      e.preventDefault();
      search.focus();
      search.select();
    }
  }

  // Si no está escribiendo en campos, todo tecleo manda foco al escáner
  if (!e.ctrlKey && !e.altKey && !e.metaKey && !isTypingField(active)) {
    globalScan?.focus();
  }
});

// Mejoras numpad: Enter salta al próximo campo numérico
const numpadFields = Array.from(document.querySelectorAll('input.numpad'));
numpadFields.forEach((field, idx) => {
  field.setAttribute('inputmode', 'decimal');
  field.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.code === 'NumpadEnter') {
      e.preventDefault();
      const next = numpadFields[idx + 1];
      if (next) {
        next.focus();
        next.select();
      }
    }
  });
});
