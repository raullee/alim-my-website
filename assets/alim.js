/* ===========================================================================
   ALIM.my — "THE DOSSIER PRINTS ITSELF" — engine
   Runs the press. Content-independent; every hook is optional so interior
   pages (no hero/plate) still get theme, reveals, nav, cursor.
   No dependencies. Degrades to a static, fully-legible page.
   =========================================================================== */
(function () {
  "use strict";
  var docEl = document.documentElement;
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- 1. NIGHT CHARTER (theme) ------------------------------------------ */
  (function theme() {
    var btn = document.getElementById("theme-toggle");
    var KEY = "alim-charter";
    function apply(on) {
      docEl.classList.toggle("charter", on);
      if (btn) btn.setAttribute("aria-pressed", on ? "true" : "false");
    }
    var saved = null;
    try { saved = localStorage.getItem(KEY); } catch (e) {}
    // Default is warm paper (the signature): only go dark on an explicit saved choice.
    if (saved === "1") apply(true);
    else apply(false);
    if (btn) btn.addEventListener("click", function () {
      var on = !docEl.classList.contains("charter");
      apply(on);
      try { localStorage.setItem(KEY, on ? "1" : "0"); } catch (e) {}
    });
  })();

  /* ---- 2. MOBILE NAV ----------------------------------------------------- */
  (function mobileNav() {
    var t = document.getElementById("nav-toggle");
    var m = document.getElementById("mobile-nav");
    if (!t || !m) return;
    t.addEventListener("click", function () {
      var open = m.classList.toggle("open");
      t.setAttribute("aria-expanded", open ? "true" : "false");
    });
    m.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { m.classList.remove("open"); t.setAttribute("aria-expanded", "false"); }
    });
  })();

  /* ---- 3. REVEALS (Cooper: blur resolves to focus) ----------------------- */
  (function reveals() {
    var nodes = document.querySelectorAll(".reveal, .linemask, .misreg");
    if (!nodes.length) return;
    if (reduced || !("IntersectionObserver" in window)) {
      nodes.forEach(function (n) { n.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    nodes.forEach(function (n) { io.observe(n); });
  })();

  /* ---- 4. FOOTER YEAR / dynamic docket stamps ---------------------------- */
  (function stamps() {
    var y = document.querySelectorAll("[data-year]");
    var now = new Date().getFullYear();
    y.forEach(function (n) { n.textContent = now; });
  })();

  /* ---- 5. INK-DOT CURSOR + MAGNETIC BUTTONS ------------------------------ */
  (function cursor() {
    if (reduced) return;
    var fine = window.matchMedia && window.matchMedia("(hover:hover) and (pointer:fine)").matches;
    if (!fine) return;
    var dot = document.getElementById("dot");
    var mx = 0, my = 0, dx = 0, dy = 0, raf = null;
    var magnets = Array.prototype.slice.call(document.querySelectorAll("[data-magnet]"));
    function loop() {
      dx += (mx - dx) * 0.22; dy += (my - dy) * 0.22;
      if (dot) { dot.style.left = dx + "px"; dot.style.top = dy + "px"; }
      // magnetic pull
      magnets.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
        var d = Math.hypot(mx - cx, my - cy);
        var pull = Math.max(0, 1 - d / 150);
        el.style.transform = pull > 0
          ? "translate(" + (mx - cx) * pull * 0.28 + "px," + (my - cy) * pull * 0.28 + "px)"
          : "";
      });
      raf = null;
    }
    function schedule() { if (!raf) raf = requestAnimationFrame(loop); }
    window.addEventListener("mousemove", function (e) {
      mx = e.clientX; my = e.clientY;
      if (dot) dot.style.opacity = "1";
      schedule();
    }, { passive: true });
    document.addEventListener("mouseleave", function () { if (dot) dot.style.opacity = "0"; });
    document.querySelectorAll("a,button,[data-magnet],summary,input,textarea,select").forEach(function (el) {
      el.addEventListener("mouseenter", function () { if (dot) dot.classList.add("lg"); });
      el.addEventListener("mouseleave", function () { if (dot) dot.classList.remove("lg"); });
    });
  })();

  /* ---- 6. THE PLATE — WebGL printing press ------------------------------- */
  /* An animated riso halftone field. On load and on hero-scroll it resolves
     from misregistered, coarse plates toward solid ink, then re-agitates as
     you scroll past. Fully optional + graceful fallback. */
  var plate = (function () {
    var canvas = document.getElementById("plate");
    if (!canvas || reduced) { if (canvas) document.body.classList.add("no-webgl"); return null; }
    var gl = canvas.getContext("webgl", { antialias: true, alpha: true, premultipliedAlpha: false })
      || canvas.getContext("experimental-webgl");
    if (!gl) { document.body.classList.add("no-webgl"); return null; }

    var vsrc =
      "attribute vec2 p; varying vec2 uv;" +
      "void main(){ uv = p*0.5+0.5; gl_Position = vec4(p,0.0,1.0); }";

    // Riso halftone press: three ink plates (vermillion, ochre, indigo) as
    // rotated dot grids that converge into register as u_resolve -> 1.
    var fsrc =
      "precision mediump float; varying vec2 uv;" +
      "uniform vec2 u_res; uniform float u_time; uniform float u_resolve; uniform float u_dpr;" +
      "float dots(vec2 c, float scale, float ang, float grow){" +
      "  float s=sin(ang), co=cos(ang);" +
      "  vec2 r=vec2(c.x*co-c.y*s, c.x*s+c.y*co);" +
      "  vec2 g=fract(r*scale)-0.5;" +
      "  float d=length(g);" +
      "  return smoothstep(grow+0.03, grow-0.03, d);" +   // filled dot where d<grow
      "}" +
      "void main(){" +
      "  vec2 c=(uv*u_res)/u_res.y;" +          // aspect-correct coords
      "  float t=u_time*0.05;" +
      "  float res=clamp(u_resolve,0.0,1.0);" +
      // misregistration offset shrinks as it resolves
      "  float mis=(1.0-res)*0.06 + 0.006;" +
      "  float scale=mix(26.0, 58.0, res);" +   // coarse plate -> fine ink
      "  float grow=mix(0.14, 0.34, res);" +    // dots grow to flood the field
      // ink concentrates toward lower-right (the press bed), soft radial bias
      "  vec2 bed=vec2(0.72*u_res.x/u_res.y,0.40);" +
      "  float bias=smoothstep(1.15,0.15,length(c-bed));" +
      "  grow*=mix(0.55,1.0,bias);" +
      "  float verm=dots(c+vec2(mis, mis*0.6+t*0.02), scale, 0.26, grow);" +
      "  float ochr=dots(c+vec2(-mis*0.8, mis+t*0.015), scale*0.94, 1.31, grow*0.8);" +
      "  float indg=dots(c+vec2(mis*0.3,-mis*0.9), scale*1.06, 2.30, grow*0.5);" +
      "  vec3 pverm=vec3(0.847,0.192,0.122);" +
      "  vec3 pochr=vec3(0.722,0.525,0.180);" +
      "  vec3 pindg=vec3(0.208,0.333,0.541);" +
      // multiply overprint over warm paper
      "  vec3 col=vec3(1.0);" +
      "  col*=mix(vec3(1.0),pverm,verm*0.9);" +
      "  col*=mix(vec3(1.0),pochr,ochr*0.55);" +
      "  col*=mix(vec3(1.0),pindg,indg*0.4);" +
      "  float alpha=max(verm*0.9,max(ochr*0.5,indg*0.4));" +
      "  alpha*=mix(0.28,0.92,res)*bias;" +      // faint while unresolved, fades at edges
      "  gl_FragColor=vec4(col,alpha);" +
      "}";

    function compile(type, src) {
      var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { return null; }
      return s;
    }
    var vs = compile(gl.VERTEX_SHADER, vsrc), fs = compile(gl.FRAGMENT_SHADER, fsrc);
    if (!vs || !fs) { document.body.classList.add("no-webgl"); return null; }
    var prog = gl.createProgram();
    gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { document.body.classList.add("no-webgl"); return null; }
    gl.useProgram(prog);

    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, "p");
    gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    var uRes = gl.getUniformLocation(prog, "u_res");
    var uTime = gl.getUniformLocation(prog, "u_time");
    var uResolve = gl.getUniformLocation(prog, "u_resolve");

    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    function size() {
      var w = canvas.clientWidth, h = canvas.clientHeight;
      canvas.width = Math.floor(w * dpr); canvas.height = Math.floor(h * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
    }
    window.addEventListener("resize", size); size();

    var resolve = 0, target = 1, start = performance.now(), running = true;
    function frame(now) {
      if (!running) return;
      resolve += (target - resolve) * 0.05;
      gl.uniform2f(uRes, canvas.width, canvas.height);
      gl.uniform1f(uTime, (now - start) / 1000);
      gl.uniform1f(uResolve, resolve);
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);

    // pause when off-screen (battery)
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting && !running) { running = true; requestAnimationFrame(frame); }
          else if (!e.isIntersecting) { running = false; }
        });
      }, { threshold: 0.01 }).observe(canvas);
    }
    return { setTarget: function (v) { target = v; } };
  })();

  /* ---- 7. HERO SCROLL MORPH (opsz/wght + 3D tilt + parallax + resolve) --- */
  (function heroMorph() {
    var stage = document.getElementById("stage");
    if (!stage || reduced) return;
    var h1 = document.getElementById("h1");
    var tilt = document.getElementById("plate-tilt");
    var pin = stage.querySelector(".pin");
    var ticking = false;
    function onScroll() {
      if (ticking) return; ticking = true;
      requestAnimationFrame(function () {
        var rect = stage.getBoundingClientRect();
        var total = stage.offsetHeight - window.innerHeight;
        var p = total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 0;
        if (pin) pin.style.setProperty("--p", p.toFixed(3));
        // display morphs from light+condensed to heavy as it "inks in", then settles
        if (h1) {
          var wght = 300 + Math.sin(Math.min(p, 0.6) / 0.6 * Math.PI * 0.5) * 480; // 300 -> ~780
          var opsz = 24 + p * 120;
          h1.style.setProperty("--wght", wght.toFixed(0));
          h1.style.setProperty("--opsz", Math.min(144, opsz).toFixed(0));
        }
        if (tilt) {
          var rx = (0.5 - p) * 6, ry = p * 4;
          tilt.style.transform = "rotateX(" + rx.toFixed(2) + "deg) rotateY(" + ry.toFixed(2) + "deg) scale(" + (1 + p * 0.08).toFixed(3) + ")";
        }
        // the press resolves as you scroll in, then re-agitates on the way out
        if (plate) plate.setTarget(p < 0.7 ? 0.35 + p : Math.max(0.2, 1.6 - p));
        ticking = false;
      });
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    onScroll();
  })();
})();
