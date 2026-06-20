/**
 * main.js — AI-Powered Customer Helpdesk System
 * Updated to match the dark navy/teal/amber design system
 */

document.addEventListener('DOMContentLoaded', function () {
    initPopovers();
    initTooltips();
    setupFormValidation();
    // table interactions handled via CSS for better performance
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
    // Intentionally left blank — CSS :hover handles visual feedback to avoid
    // adding many JS listeners which can cause jank on pages with many rows.
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

    const csrfToken = getCsrfToken();
    if (csrfToken && method !== 'GET' && method !== 'HEAD') {
        options.headers['X-CSRFToken'] = csrfToken;
        options.headers['X-CSRF-Token'] = csrfToken;
    }

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

/* ── AJAX FORM SUBMIT (Ticket) ───────────────────────────────────── */
const ticketForm = document.getElementById('ticket-form');
if (ticketForm) {
    ticketForm.addEventListener('submit', function (e) {
        // If form is marked for AJAX, handle via fetch and show loading state
        if (ticketForm.getAttribute('data-ajax') === 'true') {
            e.preventDefault();
            const btn = document.getElementById('submit-ticket-btn');
            // collect values
            const payload = {
                customer_name: ticketForm.querySelector('[name="customer_name"]').value,
                email: ticketForm.querySelector('[name="email"]').value,
                category: ticketForm.querySelector('[name="category"]').value,
                subject: ticketForm.querySelector('[name="subject"]').value,
                message: ticketForm.querySelector('[name="message"]').value
            };

            const overlay = document.getElementById('submit-overlay');
            if (overlay) overlay.style.display = 'flex';

            const promise = (async () => {
                // clear existing field errors
                ticketForm.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
                ticketForm.querySelectorAll('.invalid-text').forEach(el => el.remove());

                try {
                    const res = await fetch('/submit', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCsrfToken()
                        },
                        body: JSON.stringify(payload)
                    });

                    if (res.ok) {
                        // success — redirect to success page
                        window.location.href = '/success';
                        return;
                    }

                    const err = await res.json().catch(() => null);
                    if (err && err.errors) {
                        // show field-level errors
                        for (const [field, messages] of Object.entries(err.errors)) {
                            const input = ticketForm.querySelector('[name="' + field + '"]');
                            if (input) {
                                input.classList.add('is-invalid');
                                const div = document.createElement('div');
                                div.className = 'invalid-text';
                                div.textContent = messages.join('; ');
                                input.parentElement.appendChild(div);
                            }
                        }
                        const first = Object.values(err.errors)[0][0];
                        showNotification(first, 'danger');
                        return;
                    }

                    showNotification('Submission failed. Please try again.', 'danger');
                } catch (err) {
                    console.error('Submit error:', err);
                    showNotification('Network error. Please try again.', 'danger');
                }
            })();

            // ensure overlay is hidden when done
            promise.finally(() => { if (overlay) overlay.style.display = 'none'; });
            withButtonLoading(btn, promise);
        }
    });
}

const assistantForm = document.getElementById('assistant-form');
if (assistantForm) {
    const messageContainer = document.getElementById('assistant-messages');
    const textarea = assistantForm.querySelector('[name="question"]');

    function addAssistantMessage(role, text) {
        const message = document.createElement('div');
        message.className = `chat-message chat-message-${role}`;
        message.textContent = text;
        messageContainer.appendChild(message);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    assistantForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const question = textarea.value.trim();
        if (!question) return;

        addAssistantMessage('user', question);
        textarea.value = '';
        addAssistantMessage('bot', 'Thinking...');

        try {
            const response = await apiRequest('/assistant/query', 'POST', { question });
            const botMessages = messageContainer.querySelectorAll('.chat-message-bot');
            if (botMessages.length) {
                botMessages[botMessages.length - 1].textContent = response.answer;
            } else {
                addAssistantMessage('bot', response.answer);
            }
        } catch (err) {
            const botMessages = messageContainer.querySelectorAll('.chat-message-bot');
            if (botMessages.length) {
                botMessages[botMessages.length - 1].textContent = 'Sorry, I could not process that question right now.';
            }
        }
    });
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
// Provide helper to animate stat values from code when stats are updated
function updateStatValueById(id, value) {
    const el = document.getElementById(id);
    if (!el) return;
    if (isNaN(parseInt(value, 10))) {
        el.textContent = value;
        return;
    }
    animateCounter(el, parseInt(value, 10), 700);
}

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