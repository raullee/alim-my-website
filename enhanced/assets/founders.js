/* ALIM.my · Founders engine. Loads after alim.js. No dependencies. */
(function () {
  "use strict";
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia && window.matchMedia("(hover:hover) and (pointer:fine)").matches;
  var ASSET = document.documentElement.getAttribute("data-fm-assets") || "../../assets/founders/";

  var cards = Array.prototype.slice.call(document.querySelectorAll(".fm-card[data-slug]"));
  var people = cards.map(function (c, i) {
    return { i: i, slug: c.getAttribute("data-slug"), key: c.getAttribute("data-key"),
      name: c.querySelector(".fm-name").textContent.trim(),
      role: (c.querySelector(".fm-role") || {}).innerHTML || "", bio: c.querySelector(".fm-bio") };
  });
  var bySlug = {}; people.forEach(function (p) { bySlug[p.slug] = p; });
  function img(p, kind, w) { return ASSET + p.key + "-" + kind + "-" + w + ".webp"; }

  /* 1. BlurText split */
  (function () {
    var h = document.querySelector(".fm-h1[data-split]");
    if (!h || reduced) return;
    var label = h.textContent.replace(/\s+/g, " ").trim(), i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var s = document.createElement("span"); s.className = "w"; s.setAttribute("aria-hidden", "true");
            s.style.setProperty("--i", i++); s.textContent = part; frag.appendChild(s);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1) { walk(n); }
      });
    })(h);
    h.setAttribute("aria-label", label);
  })();

  /* 2. Dialog */
  var dlg = document.getElementById("fm-dialog");
  var current = -1, opener = null, baseTitle = document.title;
  if (dlg && people.length) {
    var dPhoto = dlg.querySelector(".fm-d-photo img"), dNo = dlg.querySelector(".fm-d-photo .fm-no");
    var dCount = dlg.querySelector("[data-count]"), dScroll = dlg.querySelector(".fm-d-scroll");
    var dPrev = dlg.querySelector("[data-prev]"), dNext = dlg.querySelector("[data-next]");
    var render = function (idx) {
      var p = people[idx]; if (!p) return; current = idx;
      var num = ("0" + (idx + 1)).slice(-2);
      dPhoto.src = img(p, "a", 1080); dPhoto.alt = "Portrait of " + p.name;
      dPhoto.classList.remove("swap"); void dPhoto.offsetWidth; if (!reduced) dPhoto.classList.add("swap");
      dNo.textContent = "FM·" + num;
      dCount.textContent = "Founding Member · " + num + " / " + ("0" + people.length).slice(-2);
      dScroll.innerHTML = '<img class="fm-d-mphoto" src="' + img(p, "a", 1080) + '" alt="">' +
        '<h2 id="fm-d-name">' + p.name + "</h2>" + (p.role ? '<p class="fm-role">' + p.role + "</p>" : '') + p.bio.innerHTML;
      dScroll.scrollTop = 0;
      dScroll.classList.remove("swap"); void dScroll.offsetWidth; if (!reduced) dScroll.classList.add("swap");
      var prev = people[(idx - 1 + people.length) % people.length], next = people[(idx + 1) % people.length];
      dPrev.querySelector("b").textContent = prev.name; dNext.querySelector("b").textContent = next.name;
      [prev, next].forEach(function (q) { var im = new Image(); im.src = img(q, "a", 1080); });
      try { history.replaceState(null, "", "#" + p.slug); } catch (e) {}
      document.title = p.name + " · Founders · ALIM.my";
    };
    var open = function (slug, from) {
      var p = bySlug[slug]; if (!p) return;
      opener = from || document.activeElement;
      render(p.i);
      if (!dlg.open) {
        if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", "");
        document.body.classList.add("fm-lock");
      }
      try { dlg.querySelector(".fm-x").focus({ preventScroll: true }); } catch (e) {}
      if (window.gtag) try { window.gtag("event", "founder_profile_open", { founder: slug }); } catch (e) {}
    };
    var finish = function () {
      dlg.classList.remove("closing");
      if (typeof dlg.close === "function") dlg.close(); else { dlg.removeAttribute("open"); dlg.dispatchEvent(new Event("close")); }
    };
    var close = function () { if (!dlg.open) return; if (reduced) finish(); else { dlg.classList.add("closing"); setTimeout(finish, 210); } };
    dlg.addEventListener("close", function () {
      document.body.classList.remove("fm-lock");
      try { history.replaceState(null, "", location.pathname + location.search); } catch (e) {}
      document.title = baseTitle;
      if (opener && opener.focus) try { opener.focus({ preventScroll: true }); } catch (e) {}
    });
    dlg.addEventListener("cancel", function (e) { e.preventDefault(); close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); });
    dlg.querySelector(".fm-x").addEventListener("click", close);
    dPrev.addEventListener("click", function () { render((current - 1 + people.length) % people.length); });
    dNext.addEventListener("click", function () { render((current + 1) % people.length); });
    dlg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); dNext.click(); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); dPrev.click(); }
    });
    document.addEventListener("click", function (e) {
      var t = e.target.closest && e.target.closest("[data-open]");
      if (!t || dlg.contains(t)) return;
      e.preventDefault(); open(t.getAttribute("data-open"), t);
    });
    var fromHash = function () {
      var s = decodeURIComponent((location.hash || "").slice(1));
      if (bySlug[s]) open(s, document.querySelector('.fm-hit[data-open="' + s + '"]'));
    };
    window.addEventListener("hashchange", fromHash);
    fromHash();
  }

  /* 3. Tilt + spotlight */
  if (fine && !reduced) {
    document.querySelectorAll(".fm-hit").forEach(function (hit) {
      var ph = hit.querySelector(".fm-photo"), raf = null, ev = null;
      hit.addEventListener("pointermove", function (e) {
        ev = e; if (raf) return;
        raf = requestAnimationFrame(function () {
          var r = ph.getBoundingClientRect();
          var x = (ev.clientX - r.left) / r.width, y = (ev.clientY - r.top) / r.height;
          ph.style.setProperty("--mx", (x * 100).toFixed(1) + "%");
          ph.style.setProperty("--my", (y * 100).toFixed(1) + "%");
          ph.style.setProperty("--ry", ((x - .5) * 7).toFixed(2) + "deg");
          ph.style.setProperty("--rx", ((.5 - y) * 6).toFixed(2) + "deg");
          raf = null;
        });
      });
      hit.addEventListener("pointerleave", function () { ph.style.setProperty("--rx", "0deg"); ph.style.setProperty("--ry", "0deg"); });
    });
  }

  /* 4. Roll-call cursor portrait */
  (function () {
    var f = document.getElementById("fm-float");
    if (!f || !fine || reduced) return;
    var im = f.querySelector("img"), x = 0, y = 0, tx = 0, ty = 0, on = false, raf = null;
    function loop() {
      x += (tx - x) * .16; y += (ty - y) * .16;
      f.style.left = x + "px"; f.style.top = y + "px";
      raf = (on || Math.abs(tx - x) > .5) ? requestAnimationFrame(loop) : null;
    }
    document.querySelectorAll(".fm-index button").forEach(function (b) {
      b.addEventListener("mouseenter", function (e) {
        var p = bySlug[b.getAttribute("data-open")]; if (!p) return;
        im.src = img(p, "b", 640);
        if (!on) { x = tx = e.clientX - 140; y = ty = e.clientY; }
        on = true; f.classList.add("on"); if (!raf) raf = requestAnimationFrame(loop);
      });
      b.addEventListener("mousemove", function (e) { tx = e.clientX - 150; ty = e.clientY; });
      b.addEventListener("mouseleave", function () { on = false; f.classList.remove("on"); });
    });
  })();

  /* 5. Scroll: plate reveal + closing parallax */
  (function () {
    var frame = document.querySelector(".fm-frame");
    var cimg = document.querySelector(".fm-close-img img");
    if (reduced) { if (frame) frame.classList.add("in"); return; }
    var ticking = false;
    function update() {
      var vh = window.innerHeight;
      if (frame) {
        var r = frame.getBoundingClientRect();
        var p = Math.min(1, Math.max(0, (vh - r.top) / (vh * .85)));
        var e = 1 - Math.pow(1 - p, 3);
        frame.style.setProperty("--ci", (5 * (1 - e)).toFixed(2) + "%");
        frame.style.setProperty("--s", (1.1 - .1 * e).toFixed(4));
        if (p > .45) frame.classList.add("in");
      }
      if (cimg) {
        var c = cimg.parentNode.getBoundingClientRect();
        cimg.style.setProperty("--py", (((c.top + c.height / 2 - vh / 2) / vh) * -40).toFixed(1) + "px");
      }
      ticking = false;
    }
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener("resize", update);
    update();
  })();
})();
