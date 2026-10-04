/* Darjeeling Himalayas · Hill Cart interactions
   Free libraries (CDN): GSAP + ScrollTrigger, Lenis. Maps are server-drawn SVG (no map API).
   Everything degrades: without JS the site stays readable, navigable and every form submits. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var track = function (name, data) { window.dataLayer = window.dataLayer || []; window.dataLayer.push(Object.assign({ event: name }, data || {})); };
  var store = {
    get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };
  var fmt = function (n) { n = Math.round(n); var s = String(n), t = s.slice(-3), h = s.slice(0, -3); if (h) t = h.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + "," + t; return t; };

  /* analytics hooks */
  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-cta]");
    if (a) track("cta_click", { cta: a.dataset.cta, href: a.getAttribute("href") || "" });
  });
  $$("form[data-cta-form]").forEach(function (f) { f.addEventListener("submit", function () { track("form_submit", { form: f.dataset.ctaForm }); }); });

  /* masthead + floating CTA visibility */
  var mast = $(".mast"), fab = $("[data-fab]");
  var onScroll = function () {
    var y = window.scrollY;
    if (mast) mast.classList.toggle("is-scrolled", y > 24);
    if (fab) fab.classList.toggle("is-on", y > 480);
  };

  /* mega menus: hover intent on desktop, click anywhere, Esc closes */
  var drops = $$(".nav__drop");
  var closeAll = function (except) { drops.forEach(function (d) { if (d !== except) { d.classList.remove("is-open"); $("button", d).setAttribute("aria-expanded", "false"); } }); };
  drops.forEach(function (drop) {
    var btn = $("button", drop), timer;
    var open = function () { clearTimeout(timer); closeAll(drop); drop.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); };
    var close = function () { drop.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); drop.classList.contains("is-open") ? close() : open(); });
    if (window.matchMedia("(hover: hover)").matches) {
      drop.addEventListener("mouseenter", function () { clearTimeout(timer); timer = setTimeout(open, 90); });
      drop.addEventListener("mouseleave", function () { clearTimeout(timer); timer = setTimeout(close, 180); });
    }
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav__drop")) closeAll(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeAll(); closeSearch(); closeFab(); } });

  /* mobile sheet */
  var sheet = $(".sheet");
  $$("[data-sheet-open]").forEach(function (b) { b.addEventListener("click", function () { sheet.classList.add("is-open"); document.body.style.overflow = "hidden"; $(".sheet__close", sheet).focus(); }); });
  $$("[data-sheet-close]").forEach(function (b) { b.addEventListener("click", function () { sheet.classList.remove("is-open"); document.body.style.overflow = ""; }); });

  /* search overlay: loads a small JSON index on first open */
  var search = $(".search"), input = $("#q"), results = $(".search__results"), index = null;
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[c]; }); };
  var norm = function (s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
  function openSearch() {
    if (!search) return;
    if (sheet) sheet.classList.remove("is-open");
    search.hidden = false; document.body.style.overflow = "hidden"; input.focus();
    if (!index) fetch(input.dataset.searchUrl).then(function (r) { return r.json(); }).then(function (d) { index = d.map(function (row) { return { t: row[0], u: row[1], k: row[2], c: row[3], n: norm(row[0] + " " + row[3] + " " + row[2]) }; }); run(); });
    track("search_open");
  }
  function closeSearch() { if (search && !search.hidden) { search.hidden = true; document.body.style.overflow = ""; } }
  function run() {
    if (!index) return;
    var q = norm(input.value.trim());
    if (q.length < 2) { results.innerHTML = ""; return; }
    var words = q.split(/\s+/);
    var hits = index.filter(function (r) { return words.every(function (w) { return r.n.indexOf(w) > -1; }); })
      .sort(function (a, b) { return (norm(a.t).indexOf(words[0]) === 0 ? -1 : 0) - (norm(b.t).indexOf(words[0]) === 0 ? -1 : 0) || a.t.length - b.t.length; })
      .slice(0, 14);
    results.innerHTML = hits.length ? hits.map(function (r) { return '<li><a href="' + esc(r.u) + '"><b>' + esc(r.t) + '</b><small>' + esc(r.k) + (r.c ? " · " + esc(r.c) : "") + "</small></a></li>"; }).join("")
      : '<li class="small muted" style="padding:12px">Nothing found. <a href="/plan/">Ask us instead</a>.</li>';
  }
  $$("[data-search-open]").forEach(function (b) { b.addEventListener("click", openSearch); });
  $$("[data-search-close]").forEach(function (b) { b.addEventListener("click", closeSearch); });
  if (search) {
    search.addEventListener("click", function (e) { if (e.target === search) closeSearch(); });
    input.addEventListener("input", run);
    document.addEventListener("keydown", function (e) { if (e.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); } });
  }

  /* floating CTA */
  var fabPanel = $("#fab-panel"), fabBtn = $(".fab__toggle");
  function closeFab() { if (fabPanel && !fabPanel.hidden) { fabPanel.hidden = true; fabBtn.setAttribute("aria-expanded", "false"); } }
  if (fab && fabBtn) {
    fabBtn.addEventListener("click", function (e) { e.stopPropagation(); var o = fabPanel.hidden; fabPanel.hidden = !o; fabBtn.setAttribute("aria-expanded", String(o)); if (o) track("fab_open"); });
    document.addEventListener("click", function (e) { if (!e.target.closest("[data-fab]")) closeFab(); });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* trip buy bar: appears once the page head scrolls away */
  var buybar = $("[data-buybar]");
  if (buybar && "IntersectionObserver" in window) {
    buybar.hidden = false;
    var head = $(".phead") || $("main section");
    new IntersectionObserver(function (en) {
      var on = !en[0].isIntersecting;
      buybar.classList.toggle("is-on", on);
      document.body.classList.toggle("has-buybar", on);
    }).observe(head);
  }

  /* planning nudge on long reads: once per visit, after 55% of the page */
  var nudge = $("[data-nudge]");
  if (nudge && !store.get("nudge-closed")) {
    var shown = false;
    window.addEventListener("scroll", function () {
      if (shown) return;
      var h = document.documentElement.scrollHeight - innerHeight;
      if (h > 0 && scrollY / h > 0.55) { shown = true; nudge.hidden = false; track("nudge_shown"); }
    }, { passive: true });
    $("[data-nudge-close]", nudge).addEventListener("click", function () { nudge.hidden = true; store.set("nudge-closed", "1"); });
  }

  /* THE CLIMB: altimeter follows the chapter in view */
  var alti = $("[data-alti]");
  if (alti && "IntersectionObserver" in window) {
    var read = $("[data-alti-read]", alti), mark = $("[data-alti-mark]", alti), name = $("[data-alti-name]", alti);
    var max = parseFloat(alti.dataset.max || "5200"), cur = 0, raf = null;
    var setAlt = function (target, label) {
      if (mark) mark.style.bottom = Math.min(100, target / max * 100) + "%";
      if (name) name.textContent = label;
      if (reduce) { read.firstChild.nodeValue = fmt(target) + " m"; cur = target; return; }
      var from = cur, t0 = performance.now();
      cancelAnimationFrame(raf);
      var step = function (t) {
        var k = Math.min(1, (t - t0) / 700), e = 1 - Math.pow(1 - k, 3);
        cur = from + (target - from) * e;
        read.firstChild.nodeValue = fmt(cur) + " m";
        if (k < 1) raf = requestAnimationFrame(step);
      };
      raf = requestAnimationFrame(step);
    };
    var chs = $$("[data-alt]");
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) setAlt(parseFloat(x.target.dataset.alt), x.target.dataset.altName || ""); });
    }, { rootMargin: "-45% 0px -45% 0px" });
    chs.forEach(function (c) { io.observe(c); });
  }

  /* split-flap fare board: letters shuffle into place when the board scrolls in */
  var boards = $$("[data-flap-board]");
  if (boards.length && !reduce && "IntersectionObserver" in window) {
    var CH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789₹–";
    boards.forEach(function (board) {
      var cells = $$(".flap span", board);
      cells.forEach(function (c) { c.dataset.final = c.textContent; });
      var played = false;
      new IntersectionObserver(function (en, obs) {
        if (!en[0].isIntersecting || played) return;
        played = true; obs.disconnect();
        cells.forEach(function (c, i) {
          var n = 6 + (i % 7), k = 0;
          var tick = setInterval(function () {
            k++;
            if (k >= n) { c.textContent = c.dataset.final; clearInterval(tick); return; }
            c.textContent = c.dataset.final === " " ? " " : CH[Math.floor(Math.random() * CH.length)];
          }, 55);
        });
      }, { threshold: 0.3 }).observe(board);
    });
  }

  /* list filters; ?tier=Value etc. preselects */
  $$("[data-filter-group]").forEach(function (group) {
    var target = $(group.dataset.filterGroup), state = {};
    var apply = function () {
      $$("[data-item]", target).forEach(function (el) {
        var ok = Object.keys(state).every(function (k) { return !state[k] || (" " + (el.dataset[k] || "") + " ").indexOf(" " + state[k] + " ") > -1; });
        el.hidden = !ok;
      });
      $$("[data-section]", target).forEach(function (sec) { sec.hidden = !$$("[data-item]", sec).some(function (el) { return !el.hidden; }); });
      var empty = $("[data-filter-empty]", group.parentNode);
      if (empty) empty.hidden = $$("[data-item]", target).some(function (el) { return !el.hidden; });
    };
    $$("button[data-key]", group).forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.dataset.key;
        $$('button[data-key="' + k + '"]', group).forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
        state[k] = b.dataset.value; apply();
      });
    });
    $$("select[data-key]", group).forEach(function (s) { s.addEventListener("change", function () { state[s.dataset.key] = s.value; apply(); }); });
    var params = new URLSearchParams(location.search);
    $$("select[data-key]", group).forEach(function (s) { var v = params.get(s.dataset.key); if (v) { s.value = v; state[s.dataset.key] = v; } });
    $$("button[data-key]", group).forEach(function (b) { if (params.get(b.dataset.key) === b.dataset.value) b.click(); });
    if (Object.keys(state).length) apply();
  });

  /* plan wizard */
  $$("[data-wizard]").forEach(function (form) {
    var steps = $$(".wizard__step", form), labels = $$(".wizard__steps li", form), bar = $(".wizard__bar span", form), i = 0;
    if ($(".errorlist", form)) i = steps.length - 1;
    var show = function (n) {
      i = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (s, k) { s.classList.toggle("is-on", k === i); });
      labels.forEach(function (l, k) { l.classList.toggle("is-on", k <= i); });
      bar.style.width = ((i + 1) / steps.length * 100) + "%";
      track("wizard_step", { step: i + 1 });
    };
    form.setAttribute("data-ready", "");
    $$("[data-next]", form).forEach(function (b) { b.addEventListener("click", function () {
      var bad = $$("input, select, textarea", steps[i]).filter(function (el) { return !el.checkValidity(); });
      if (bad.length) { bad[0].reportValidity(); return; }
      show(i + 1); var f = steps[i].querySelector("input, select, textarea"); if (f) f.focus();
    }); });
    $$("[data-prev]", form).forEach(function (b) { b.addEventListener("click", function () { show(i - 1); }); });
    show(i);
  });

  /* atlas: pins and legend highlight each other */
  $$(".atlas").forEach(function (fig) {
    var pins = $$(".atlas__pin", fig), items = $$(".atlas__legend li", fig);
    var hot = function (n, on) {
      pins.forEach(function (p) { if (p.dataset.n === n) p.classList.toggle("is-hot", on); });
      items.forEach(function (li) { if (li.dataset.n === n) li.classList.toggle("is-hot", on); });
    };
    pins.concat(items).forEach(function (el) {
      el.addEventListener("mouseenter", function () { hot(el.dataset.n, true); });
      el.addEventListener("mouseleave", function () { hot(el.dataset.n, false); });
    });
  });

  /* contents rail: highlight the section in view */
  var tocLinks = $$(".toc-side a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) tocLinks.forEach(function (a) { a.classList.toggle("is-on", a.getAttribute("href") === "#" + en.target.id); }); });
    }, { rootMargin: "-30% 0px -60% 0px" });
    tocLinks.forEach(function (a) { var t = document.getElementById(a.getAttribute("href").slice(1)); if (t) tio.observe(t); });
  }

  /* budget builder: per-day costs by tier, land and nights */
  var bud = $("[data-budget]");
  if (bud) {
    var rates = JSON.parse(bud.dataset.budget);
    var calc = function () {
      var tier = $("[name=tier]:checked", bud).value, nights = +$("[name=nights]", bud).value, people = +$("[name=people]", bud).value;
      var land = $("[name=land]", bud).value, r = rates.tiers[tier], mult = rates.lands[land] || 1;
      var rows = [["Beds", r.bed * nights / 2 * mult], ["Food", r.food * (nights + 1) * mult], ["Local transport", r.move * (nights + 1) * mult], ["Entry fees, permits, guides", r.fees * (nights + 1) * mult], ["From Siliguri and back", r.gate]];
      var pp = rows.reduce(function (s, x) { return s + x[1]; }, 0);
      $("[data-out-nights]", bud).textContent = nights + (nights === 1 ? " night" : " nights");
      $("[data-out-people]", bud).textContent = people;
      $("[data-out-pp]", bud).textContent = "₹" + fmt(Math.round(pp / 100) * 100);
      $("[data-out-total]", bud).textContent = "₹" + fmt(Math.round(pp * people / 100) * 100);
      $("[data-out-day]", bud).textContent = "₹" + fmt(Math.round(pp / (nights + 1) / 50) * 50);
      $("[data-out-rows]", bud).innerHTML = rows.map(function (x) { return '<div class="ledger__row"><span><i class="ledger__key"></i>' + x[0] + '</span><i></i><b>₹' + fmt(Math.round(x[1] / 50) * 50) + '</b></div>'; }).join("");
      var link = $("[data-out-plan]", bud); if (link) link.href = "/plan/?land=" + encodeURIComponent(land) + "&budget=" + tier;
    };
    $$("input, select", bud).forEach(function (el) { el.addEventListener("input", calc); });
    calc();
  }

  /* season finder */
  var sf = $("[data-season]");
  if (sf) {
    var data = JSON.parse($("#season-data").textContent), grid = $("[data-season-out]", sf);
    var m = $("[name=month]", sf), land = $("[name=sland]", sf);
    var draw = function () {
      var mi = +m.value, ls = land.value;
      var rows = data.filter(function (p) { return (!ls || p.rs === ls) && p.b[mi] >= 1; }).sort(function (a, b) { return b.b[mi] - a.b[mi]; });
      grid.innerHTML = rows.length ? rows.map(function (p) { return '<a class="ecard" href="' + esc(p.u) + '" data-land="' + esc(p.rs) + '">' + (p.i ? '<img src="' + esc(p.i) + '" alt="" loading="lazy">' : '<span></span>') + '<span><span class="ecard__kind">' + (p.b[mi] === 2 ? "Best month" : "Good month") + '</span><b>' + esc(p.n) + '</b><span class="small">' + esc(p.r) + (p.a ? " · " + fmt(p.a) + " m" : "") + '</span></span></a>'; }).join("") : "<p>Nothing is at its best here this month. Try another land.</p>";
    };
    m.addEventListener("change", draw); land.addEventListener("change", draw); draw();
  }

  /* smooth scroll + reveals + mist + track */
  if (!reduce && window.Lenis) {
    var lenis = new Lenis({ lerp: 0.12 });
    if (window.gsap && window.ScrollTrigger) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      var rafL = function (t) { lenis.raf(t); requestAnimationFrame(rafL); };
      requestAnimationFrame(rafL);
    }
  }
  if (!reduce && window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    $$(".rv").forEach(function (el) { gsap.to(el, { opacity: 1, y: 0, duration: 1, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 90%", once: true } }); });
    var hero = $(".hero");
    if (hero) {
      var title = $(".h-hero", hero);
      if (title) gsap.from(title, { y: 50, opacity: 0, duration: 1.3, ease: "power4.out" });
      gsap.to($(".hero__img img", hero), { scale: 1.12, yPercent: 6, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
      $$(".mist", hero).forEach(function (mist, i) { gsap.to(mist, { yPercent: -60 - i * 30, opacity: 0, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "70% top", scrub: true } }); });
    }
    $$(".phead__img img").forEach(function (img) { gsap.to(img, { yPercent: 8, scale: 1.06, ease: "none", scrollTrigger: { trigger: img.closest(".phead"), start: "top top", end: "bottom top", scrub: true } }); });
    $$(".track-svg path[data-draw]").forEach(function (p) {
      var L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
      gsap.to(p, { strokeDashoffset: 0, ease: "none", scrollTrigger: { trigger: p.closest("section") || p, start: "top 80%", end: "bottom 40%", scrub: true } });
    });
    $$(".ledger__bar span").forEach(function (s) { var w = s.style.width; s.style.width = "0%"; gsap.to(s, { width: w, duration: 1.1, ease: "power3.out", scrollTrigger: { trigger: s, start: "top 92%", once: true } }); });
  } else {
    doc.classList.remove("js");
  }
})();
