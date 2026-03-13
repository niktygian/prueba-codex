const isTypingField = (el) => el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT');

const getFocusable = (scope = document) => Array.from(
  scope.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])')
).filter((el) => el.offsetParent !== null);

// UX existente de envío
for (const f of document.querySelectorAll('form')) {
  f.addEventListener('submit', () => {
    const btn = f.querySelector('button[type="submit"], button:not([type])');
    if (!btn) return;
    const oldText = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Procesando...';
    setTimeout(() => {
      btn.disabled = false;
      btn.textContent = oldText;
    }, 700);
  });
}

const globalScan = document.getElementById('barcodeInputGlobal');
if (globalScan) setTimeout(() => globalScan.focus(), 150);

// ===== Atajos solicitados =====
// F1: ayuda de teclado
const kbHelp = document.getElementById('keyboardHelp');
const closeKbHelp = () => kbHelp?.classList.remove('open');
const openKbHelp = () => kbHelp?.classList.add('open');

kbHelp?.addEventListener('click', (e) => {
  if (e.target.dataset.close === '1') closeKbHelp();
});

document.addEventListener('keydown', (e) => {
  const active = document.activeElement;

  if (e.key === 'F1') {
    e.preventDefault();
    openKbHelp();
    return;
  }

  // F2: nuevo registro (foco en formulario principal)
  if (e.key === 'F2') {
    e.preventDefault();
    const form = document.getElementById('nuevaOrdenForm') || document.querySelector('form');
    const first = form ? getFocusable(form).find((el) => el.tagName !== 'BUTTON') : null;
    first?.focus();
    return;
  }

  // F3: búsqueda
  if (e.key === 'F3') {
    e.preventDefault();
    const search = document.getElementById('searchOrdenes') || document.querySelector('input[name="q"]') || globalScan;
    search?.focus();
    if (search?.select) search.select();
    return;
  }

  // ESC: cerrar ayuda o volver atrás
  if (e.key === 'Escape') {
    if (kbHelp?.classList.contains('open')) {
      e.preventDefault();
      closeKbHelp();
      return;
    }

    if (isTypingField(active)) {
      active.blur();
      return;
    }

    const backLink = document.querySelector('[data-esc-back="1"]');
    if (backLink?.href) {
      window.location.href = backLink.href;
      return;
    }

    if (window.history.length > 1) {
      window.history.back();
    }
    return;
  }

  // Mantener foco operativo en escáner si no estás escribiendo
  if (!e.ctrlKey && !e.altKey && !e.metaKey && !isTypingField(active) && e.key.length === 1) {
    globalScan?.focus();
  }
});

// ===== Enter: siguiente campo lógico / submit =====
for (const form of document.querySelectorAll('form')) {
  form.addEventListener('keydown', (e) => {
    const el = e.target;
    if (e.key !== 'Enter' && e.code !== 'NumpadEnter') return;
    if (!isTypingField(el) || el.tagName === 'TEXTAREA') return;

    e.preventDefault();
    const fields = getFocusable(form).filter((n) => ['INPUT', 'SELECT', 'TEXTAREA'].includes(n.tagName));
    const idx = fields.indexOf(el);
    const next = fields[idx + 1];

    if (next) {
      next.focus();
      if (next.select) next.select();
    } else {
      form.requestSubmit?.();
    }
  });
}

// ===== Numpad natural =====
for (const field of document.querySelectorAll('input.numpad')) {
  field.setAttribute('inputmode', 'decimal');
}

// ===== Flechas para navegar tablas/listas =====
for (const table of document.querySelectorAll('table')) {
  const rows = Array.from(table.querySelectorAll('tr')).slice(1).filter((r) => r.querySelector('td'));
  if (!rows.length) continue;

  rows.forEach((row, i) => {
    row.tabIndex = 0;
    row.dataset.rowIndex = String(i);
  });

  table.addEventListener('keydown', (e) => {
    const row = e.target.closest('tr');
    if (!row || !row.dataset.rowIndex) return;
    const idx = Number(row.dataset.rowIndex);

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      rows[Math.min(rows.length - 1, idx + 1)]?.focus();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      rows[Math.max(0, idx - 1)]?.focus();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      const firstLink = row.querySelector('a');
      firstLink?.focus();
    } else if (e.key === 'Enter') {
      const openLink = row.querySelector('a');
      if (openLink) {
        e.preventDefault();
        openLink.click();
      }
    }
  });
}
