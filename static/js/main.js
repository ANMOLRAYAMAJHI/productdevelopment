/**
 * main.js — AI-Powered Customer Helpdesk System
 * Updated to match the dark navy/teal/amber design system
 */

document.addEventListener('DOMContentLoaded', function () {
    initPopovers();
    initTooltips();
    setupFormValidation();
    setupTableInteractions();
    setupAutoSubmitFilters();
    setupFlashAutoDismiss();
});

/* ── BOOTSTRAP INIT ─────────────────────────────────────────── */

function initPopovers() {
    document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => {
        new bootstrap.Popover(el);
    });
}

function initTooltips() {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);
    });
}

/* ── FORM VALIDATION ────────────────────────────────────────── */

function setupFormValidation() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

/* ── TABLE ROW HOVER ────────────────────────────────────────── */
// CSS handles hover; this is kept for any dynamic tables added via JS.

function setupTableInteractions() {
    document.querySelectorAll('table tbody tr').forEach(row => {
        row.addEventListener('mouseenter', function () {
            this.style.background = 'rgba(14, 165, 160, 0.05)';
        });
        row.addEventListener('mouseleave', function () {
            this.style.background = '';
        });
    });
}

/* ── AUTO-SUBMIT FILTERS ────────────────────────────────────── */

function setupAutoSubmitFilters() {
    document.querySelectorAll('[data-auto-submit]').forEach(select => {
        select.addEventListener('change', function () {
            this.form && this.form.submit();
        });
    });
}

/* ── FLASH MESSAGE AUTO-DISMISS ─────────────────────────────── */

function setupFlashAutoDismiss() {
    document.querySelectorAll('.alert-custom').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });
}

/* ── NOTIFICATION TOAST ─────────────────────────────────────── */

/**
 * Show a toast notification.
 * @param {string} message
 * @param {'success'|'danger'|'info'|'warning'} type
 * @param {number} duration  ms before auto-dismiss (default 3500)
 */
function showNotification(message, type = 'info', duration = 3500) {
    const icons = {
        success: '✓',
        danger:  '✕',
        info:    'ℹ',
        warning: '⚠',
    };

    // Remove any existing toasts first
    document.querySelectorAll('.toast-hd').forEach(t => t.remove());

    const toast = document.createElement('div');
    toast.className = `toast-hd toast-${type}`;
    toast.innerHTML = `
        <span style="font-size:1rem; flex-shrink:0;">${icons[type] || icons.info}</span>
        <span style="flex:1;">${message}</span>
        <button onclick="this.parentElement.remove()"
            style="background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:1rem;padding:0;line-height:1;margin-left:0.4rem;">✕</button>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 400);
    }, duration);
}

/* ── CLIPBOARD ──────────────────────────────────────────────── */

function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => showNotification('Copied to clipboard!', 'success'))
        .catch(() => showNotification('Failed to copy.', 'danger'));
}

/* ── DATE FORMATTING ─────────────────────────────────────────── */

function formatDate(dateString) {
    const opts = {
        year: 'numeric', month: 'long', day: 'numeric',
        hour: '2-digit', minute: '2-digit',
    };
    return new Date(dateString).toLocaleDateString('en-US', opts);
}

/* ── CONFIRM DIALOG ─────────────────────────────────────────── */

function confirmAction(message) {
    return confirm(message);
}

/* ── DEBOUNCE ───────────────────────────────────────────────── */

function debounce(fn, wait) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), wait);
    };
}

/* ── SEARCH ─────────────────────────────────────────────────── */

const searchInput = document.getElementById('search-input');
if (searchInput) {
    searchInput.addEventListener('input', debounce(function (e) {
        console.log('Search:', e.target.value);
    }, 300));
}

/* ── API HELPER ─────────────────────────────────────────────── */

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
    };
    if (data) options.body = JSON.stringify(data);

    try {
        const res = await fetch(endpoint, options);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error('API error:', err);
        showNotification('An error occurred. Please try again.', 'danger');
        throw err;
    }
}

/* ── CSRF ───────────────────────────────────────────────────── */

function getCsrfToken() {
    const el = document.querySelector('meta[name="csrf-token"]');
    return el ? el.getAttribute('content') : '';
}

/* ── LOADING STATE ──────────────────────────────────────────── */

/**
 * Show a loading state on a button while an async action runs.
 * @param {HTMLElement} btn
 * @param {Promise} promise
 */
async function withButtonLoading(btn, promise) {
    const original = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="loading-dots"><span></span><span></span><span></span></span>`;
    try {
        return await promise;
    } finally {
        btn.disabled = false;
        btn.innerHTML = original;
    }
}

/* ── STAT COUNTER ANIMATION ─────────────────────────────────── */

/**
 * Animate a number counting up from 0 to target.
 * @param {HTMLElement} el
 * @param {number} target
 * @param {number} duration ms
 */
function animateCounter(el, target, duration = 800) {
    const start = performance.now();
    function tick(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        el.textContent = Math.round(eased * target);
        if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}

// Auto-animate stat values when they're updated
const statObserver = new MutationObserver(mutations => {
    mutations.forEach(({ target, oldValue }) => {
        const newVal = parseInt(target.textContent, 10);
        if (!isNaN(newVal) && target.textContent !== '—') {
            animateCounter(target, newVal, 700);
        }
    });
});

document.querySelectorAll('.stat-value').forEach(el => {
    statObserver.observe(el, { characterData: false, childList: true, subtree: true });
});

/* ── GLOBAL EXPORT ──────────────────────────────────────────── */

window.helpdesk = {
    showNotification,
    copyToClipboard,
    confirmAction,
    apiRequest,
    formatDate,
    debounce,
    withButtonLoading,
    animateCounter,
    getCsrfToken,
};