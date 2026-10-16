// Exit-intent email capture for product landing pages.
// Include on any page with: <script src="/scripts/exit-intent.js" defer data-source="page-name"></script>
(function() {
    const SOURCE = document.currentScript?.dataset?.source || 'product-page';
    const SHOWN_KEY = 'sailab_exit_shown_' + SOURCE;
    if (sessionStorage.getItem(SHOWN_KEY)) return;

    const modalHtml = `
        <div class="exit-overlay" id="exitModal" aria-hidden="true" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.7); z-index:1000; align-items:center; justify-content:center; padding:1rem;">
            <div class="exit-modal" role="dialog" aria-modal="true" aria-labelledby="exitTitle" style="background:var(--bg-card); border:1px solid var(--brand-teal); border-radius:var(--radius-lg); padding:2rem; max-width:480px; width:100%; text-align:center; position:relative;">
                <button class="close" id="exitClose" aria-label="Close" style="position:absolute; top:0.75rem; right:1rem; background:none; border:none; color:var(--text-muted); font-size:1.5rem; cursor:pointer;">&times;</button>
                <div style="font-size:2.5rem; margin-bottom:0.5rem;">🚀</div>
                <h3 id="exitTitle" style="margin-bottom:0.75rem;">Wait — Get the Free AI Starter Kit First</h3>
                <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:1rem;">Not ready to buy? Get "27 Ways to Use AI in Your Business" plus our best automation ideas. No pitch, just useful stuff.</p>
                <form id="exitForm" action="https://api.shaynesailab.com/api/lead-magnet-signup" method="POST">
                    <input type="hidden" name="source" value="${SOURCE}-exit-intent">
                    <input type="email" name="email" placeholder="you@company.com" required style="width:100%; padding:0.8rem 1rem; background:var(--bg); border:1px solid var(--border); border-radius:var(--radius); color:var(--text); font-size:1rem; margin-bottom:0.8rem; box-sizing:border-box;">
                    <button type="submit" class="btn btn-primary" style="width:100%;">Send Me the Free Guide →</button>
                </form>
                <p style="font-size:0.75rem; color:var(--text-muted); margin:0.75rem 0 0;">No spam. Unsubscribe anytime.</p>
            </div>
        </div>
    `;

    const wrapper = document.createElement('div');
    wrapper.innerHTML = modalHtml;
    document.body.appendChild(wrapper.firstElementChild);

    const modal = document.getElementById('exitModal');
    const closeBtn = document.getElementById('exitClose');
    const form = document.getElementById('exitForm');

    function show() {
        if (sessionStorage.getItem(SHOWN_KEY)) return;
        sessionStorage.setItem(SHOWN_KEY, '1');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        if (typeof window.track === 'function') {
            window.track('email_capture', {page: location.pathname, source: SOURCE + '-exit-intent', target: ''});
        }
    }

    function hide() {
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    document.addEventListener('mouseout', function(e) {
        if (e.clientY < 10) show();
    });

    closeBtn.addEventListener('click', hide);
    modal.addEventListener('click', function(e) { if (e.target === modal) hide(); });
    document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && modal.style.display === 'flex') hide(); });

    form.addEventListener('submit', function() {
        setTimeout(hide, 100);
    });
})();
