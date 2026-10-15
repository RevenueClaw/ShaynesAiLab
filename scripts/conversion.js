/**
 * Conversion enhancements for Shayne's AI Lab
 * - Site-wide announcement bar
 * - Floating CTA button
 * - Blog post end-of-article email capture
 */
(function() {
    'use strict';

    // Avoid double-injection
    if (window._sailabConversionLoaded) return;
    window._sailabConversionLoaded = true;

    const GUIDE_URL = '/ai-starter-kit';
    const FORM_ACTION = 'https://api.shaynesailab.com/api/lead-magnet-signup';

    function createEl(tag, attrs, styles) {
        const el = document.createElement(tag);
        if (attrs) Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
        if (styles) Object.entries(styles).forEach(([k, v]) => el.style[k] = v);
        return el;
    }

    // ── Announcement bar ─────────────────────────────────────────────────────
    function injectAnnouncementBar() {
        if (document.getElementById('sailab-announce-bar')) return;
        const bar = createEl('div', {
            id: 'sailab-announce-bar',
            role: 'banner',
            'aria-label': 'Free guide announcement'
        }, {
            position: 'fixed',
            top: '0',
            left: '0',
            right: '0',
            zIndex: '9999',
            background: 'linear-gradient(90deg, #0f766e 0%, #115e59 100%)',
            color: '#fff',
            textAlign: 'center',
            padding: '0.55rem 1rem',
            fontSize: '0.9rem',
            fontFamily: 'Inter, system-ui, sans-serif',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            lineHeight: '1.4'
        });
        bar.innerHTML = `
            <span style="font-weight:600;">Free Guide:</span> 27 Ways to Use AI in Your Business — 
            <a href="${GUIDE_URL}" style="color:#2dd4bf; text-decoration:underline; font-weight:600;">Get it now →</a>
        `;
        document.body.appendChild(bar);
        document.body.style.paddingTop = (bar.offsetHeight + 8) + 'px';
    }

    // ── Floating action button ───────────────────────────────────────────────
    function injectFloatingCTA() {
        if (document.getElementById('sailab-fab')) return;
        const fab = createEl('a', {
            id: 'sailab-fab',
            href: GUIDE_URL,
            'aria-label': 'Get the free AI guide'
        }, {
            position: 'fixed',
            bottom: '1.25rem',
            right: '1.25rem',
            zIndex: '9998',
            background: 'linear-gradient(135deg, #2dd4bf 0%, #06b6d4 100%)',
            color: '#0f172a',
            padding: '0.85rem 1.1rem',
            borderRadius: '999px',
            fontFamily: 'Inter, system-ui, sans-serif',
            fontWeight: '700',
            fontSize: '0.9rem',
            textDecoration: 'none',
            boxShadow: '0 6px 20px rgba(45,212,191,0.25)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
            transition: 'transform 0.15s, box-shadow 0.15s'
        });
        fab.innerHTML = '🎁 <span>Free Guide</span>';
        fab.addEventListener('mouseenter', () => {
            fab.style.transform = 'translateY(-2px)';
            fab.style.boxShadow = '0 8px 24px rgba(45,212,191,0.35)';
        });
        fab.addEventListener('mouseleave', () => {
            fab.style.transform = 'none';
            fab.style.boxShadow = '0 6px 20px rgba(45,212,191,0.25)';
        });
        document.body.appendChild(fab);
    }

    // ── Blog post end CTA ────────────────────────────────────────────────────
    function injectBlogEndCTA() {
        // Only on blog article pages (paths like /blog/slug/)
        const path = location.pathname;
        if (!path.startsWith('/blog/') || path === '/blog/' || path === '/blog') return;
        if (document.getElementById('sailab-blog-cta')) return;

        // Find article container
        const article = document.querySelector('article') ||
                        document.querySelector('main') ||
                        document.querySelector('.container');
        if (!article) return;

        // Don't inject if already present
        if (article.querySelector('#sailab-blog-cta')) return;

        const cta = createEl('div', { id: 'sailab-blog-cta' }, {
            background: 'var(--bg-card, #1e293b)',
            border: '1px solid var(--brand-teal, #2dd4bf)',
            borderRadius: 'var(--radius-lg, 12px)',
            padding: '1.75rem',
            marginTop: '2.5rem',
            textAlign: 'center'
        });
        cta.innerHTML = `
            <div style="font-size:2rem; margin-bottom:0.5rem;">📥</div>
            <h3 style="margin:0 0 0.5rem; font-size:1.25rem; color:var(--text,#f8fafc);">Get the free AI operations guide</h3>
            <p style="margin:0 0 1.25rem; color:var(--text-muted,#94a3b8); font-size:0.95rem; line-height:1.5;">
                27 practical ways to use AI in your business — plus the exact tools and setup steps for each.
            </p>
            <form action="${FORM_ACTION}" method="POST" style="max-width:380px; margin:0 auto;">
                <input type="hidden" name="source" value="blog-end-cta">
                <input type="email" name="email" placeholder="you@company.com" required
                    style="width:100%; padding:0.8rem 1rem; background:var(--bg,#0f172a); border:1px solid var(--border,#334155);
                           border-radius:var(--radius,8px); color:var(--text,#f8fafc); font-size:1rem; margin-bottom:0.75rem; box-sizing:border-box;">
                <button type="submit" class="btn btn-primary" style="width:100%;">Send Me the Free Guide →</button>
            </form>
            <p style="font-size:0.75rem; color:var(--text-muted,#94a3b8); margin:0.75rem 0 0;">No spam. Unsubscribe anytime.</p>
        `;

        // Append at the end of the article/main container
        article.appendChild(cta);
    }

    // ── Initialize ───────────────────────────────────────────────────────────
    function init() {
        injectAnnouncementBar();
        injectFloatingCTA();
        injectBlogEndCTA();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
