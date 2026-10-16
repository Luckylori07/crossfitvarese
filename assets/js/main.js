/* CrossFit Varese — JavaScript condiviso (nessuna dipendenza) */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement, body = doc.body;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Modalità demo: se data-demo non è "true" rimuove noindex e prefisso [DEMO] dal titolo */
  if (body.getAttribute('data-demo') !== 'true') {
    var robots = doc.querySelector('meta[name="robots"][content*="noindex"]');
    if (robots) robots.remove();
    doc.title = doc.title.replace(/^\[DEMO\]\s*/, '');
  }

  /* Header: cambia stile allo scroll + barra CTA mobile */
  var header = doc.querySelector('.site-header');
  var sticky = doc.querySelector('.sticky-cta');
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle('is-scrolled', y > 24);
    if (sticky) sticky.classList.toggle('is-visible', y > 480);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Menu mobile accessibile */
  var toggle = doc.querySelector('.nav-toggle');
  var nav = doc.getElementById('primary-nav');
  if (toggle && nav) {
    var mq = window.matchMedia('(min-width: 1080px)');
    var lastFocus = null;
    var focusables = function () { return Array.prototype.slice.call(nav.querySelectorAll('a[href]')).concat(toggle); };
    var setOpen = function (open) {
      if (open) nav.removeAttribute('inert');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
      nav.classList.toggle('is-open', open);
      body.style.overflow = open ? 'hidden' : '';
      if (open) { lastFocus = doc.activeElement; var f = nav.querySelector('a[href]'); if (f) f.focus(); }
      else if (lastFocus) { toggle.focus(); }
    };
    // su mobile il menu chiuso non deve essere raggiungibile da tastiera
    var syncHidden = function () {
      var closed = !mq.matches && !nav.classList.contains('is-open');
      if (closed) nav.setAttribute('inert', ''); else nav.removeAttribute('inert');
    };
    toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); syncHidden(); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) { setOpen(false); syncHidden(); } });
    doc.addEventListener('keydown', function (e) {
      if (!nav.classList.contains('is-open')) return;
      if (e.key === 'Escape') { setOpen(false); syncHidden(); return; }
      if (e.key === 'Tab') {
        var els = focusables(); var first = els[0], last = els[els.length - 1];
        if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    (mq.addEventListener ? mq.addEventListener.bind(mq, 'change') : mq.addListener.bind(mq))(function () { setOpen(false); syncHidden(); });
    syncHidden();
  }

  /* Intro: timer che scende a zero (una volta per sessione, solo home) */
  var clock = doc.querySelector('[data-clock]');
  if (clock && root.classList.contains('intro-on')) {
    var n = 3;
    var tick = setInterval(function () {
      n -= 1;
      clock.textContent = '00:0' + n;
      if (n <= 0) { clearInterval(tick); clock.parentNode.classList.add('is-zero'); }
    }, 450);
    setTimeout(function () { root.classList.remove('intro-on'); }, 2700);
  }

  /* Reveal allo scroll */
  var targets = doc.querySelectorAll('[data-reveal], .rule-draw');
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add('is-in'); });
  }

  /* Parallax leggero (solo transform) */
  var px = Array.prototype.slice.call(doc.querySelectorAll('[data-parallax]'));
  if (px.length && !reduced) {
    var ticking = false;
    var update = function () {
      var vh = window.innerHeight;
      px.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var host = el.parentElement.getBoundingClientRect();
        if (host.bottom < -100 || host.top > vh + 100) return;
        var k = parseFloat(el.getAttribute('data-parallax')) || 0.1;
        var offset = (el.classList.contains('hero-media'))
          ? (window.scrollY || 0) * k
          : ((host.top + host.height / 2) - vh / 2) * -k;
        if (!el.classList.contains('hero-media')) {
          var max = host.height * 0.065;
          offset = Math.max(-max, Math.min(max, offset));
        }
        el.style.transform = 'translate3d(0,' + offset.toFixed(1) + 'px,0)';
      });
      ticking = false;
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* Lightbox accessibile (<dialog>) */
  var dlg = doc.querySelector('dialog.lightbox');
  var items = Array.prototype.slice.call(doc.querySelectorAll('.g-item'));
  if (dlg && items.length && typeof dlg.showModal === 'function') {
    var img = dlg.querySelector('img'), cap = dlg.querySelector('.lb-caption');
    var idx = 0, opener = null;
    var show = function (i) {
      idx = (i + items.length) % items.length;
      var it = items[idx];
      img.src = it.getAttribute('data-full');
      img.alt = it.getAttribute('data-alt') || '';
      cap.textContent = (it.getAttribute('data-caption') || '') + '  (' + (idx + 1) + ' di ' + items.length + ')';
    };
    items.forEach(function (it, i) {
      it.addEventListener('click', function () { opener = it; show(i); dlg.showModal(); });
    });
    dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
    dlg.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
    dlg.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
    dlg.addEventListener('close', function () { if (opener) opener.focus(); });
  }
})();
