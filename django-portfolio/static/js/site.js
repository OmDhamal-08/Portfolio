/* Portfolio interactions: smooth scroll, GSAP reveals, counters,
   typewriter, magnetic buttons, spotlight cards and HTMX hooks. */
(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const hasGsap = typeof window.gsap !== "undefined";

  if (hasGsap && window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

  /* ---------- Smooth scrolling (Lenis) ---------- */
  let lenis = null;
  if (!reduceMotion && typeof window.Lenis !== "undefined") {
    lenis = new Lenis({ duration: 1.1, smoothWheel: true });
    if (hasGsap && window.ScrollTrigger) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add((time) => lenis.raf(time * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = (time) => { lenis.raf(time); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
    // Make in-page anchor links use Lenis too
    document.addEventListener("click", (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link || link.getAttribute("href").length < 2) return;
      const target = document.querySelector(link.getAttribute("href"));
      if (target) { event.preventDefault(); lenis.scrollTo(target, { offset: -90 }); }
    });
  }

  /* ---------- Reveal animations ---------- */
  function showAll(root) {
    root.querySelectorAll("[data-reveal], [data-stagger] > *").forEach((el) => { el.style.opacity = 1; });
  }

  function initReveals(root) {
    root = root || document;
    if (!hasGsap || !window.ScrollTrigger || reduceMotion) { showAll(root); return; }

    root.querySelectorAll("[data-reveal]").forEach((el) => {
      if (el.dataset.revealed) return;
      el.dataset.revealed = "1";
      const type = el.dataset.reveal || "up";
      const from = { opacity: 0, y: 40 };
      if (type === "left") Object.assign(from, { x: -50, y: 0 });
      if (type === "right") Object.assign(from, { x: 50, y: 0 });
      if (type === "scale") Object.assign(from, { scale: 0.92, y: 0 });
      if (type === "fade") Object.assign(from, { y: 0 });
      gsap.fromTo(el, from, {
        opacity: 1, x: 0, y: 0, scale: 1,
        duration: 0.9, ease: "power3.out",
        delay: parseFloat(el.dataset.delay || 0),
        scrollTrigger: { trigger: el, start: "top 88%", once: true },
      });
    });

    root.querySelectorAll("[data-stagger]").forEach((group) => {
      if (group.dataset.revealed) return;
      group.dataset.revealed = "1";
      gsap.fromTo(group.children, { opacity: 0, y: 30 }, {
        opacity: 1, y: 0, duration: 0.7, ease: "power3.out",
        stagger: parseFloat(group.dataset.stagger || 0.08),
        scrollTrigger: { trigger: group, start: "top 88%", once: true },
      });
    });

    // Progress bars fill when they scroll into view
    root.querySelectorAll("[data-bar]").forEach((bar) => {
      if (bar.dataset.revealed) return;
      bar.dataset.revealed = "1";
      gsap.fromTo(bar, { scaleX: 0 }, {
        scaleX: 1, duration: 1.4, ease: "power3.out",
        scrollTrigger: { trigger: bar, start: "top 92%", once: true },
      });
    });

    // Timeline line draws as you scroll
    root.querySelectorAll(".timeline").forEach((timeline) => {
      const line = timeline.querySelector(".timeline-line");
      if (!line || line.dataset.revealed) return;
      line.dataset.revealed = "1";
      gsap.fromTo(line, { scaleY: 0 }, {
        scaleY: 1, ease: "none",
        scrollTrigger: { trigger: timeline, start: "top 75%", end: "bottom 70%", scrub: 0.6 },
      });
    });
  }

  /* ---------- Hero intro ---------- */
  function initHero() {
    const hero = document.querySelector("[data-hero]");
    if (!hero || !hasGsap || reduceMotion) return;
    const tl = gsap.timeline({ defaults: { ease: "power4.out" } });
    tl.from(hero.querySelectorAll("[data-hero-line]"), { yPercent: 110, opacity: 0, duration: 1.1, stagger: 0.12 })
      .from(hero.querySelectorAll("[data-hero-fade]"), { y: 20, opacity: 0, duration: 0.8, stagger: 0.08 }, "-=0.6")
      .from(hero.querySelectorAll("[data-hero-photo]"), { scale: 0.85, opacity: 0, duration: 1.2 }, "-=1");

    // Parallax on the background orbs
    document.querySelectorAll("[data-parallax]").forEach((el) => {
      gsap.to(el, {
        yPercent: parseFloat(el.dataset.parallax) * 100,
        ease: "none",
        scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true },
      });
    });
  }

  /* ---------- Number counters ---------- */
  function initCounters(root) {
    (root || document).querySelectorAll("[data-count]").forEach((el) => {
      const end = parseInt(el.dataset.count, 10) || 0;
      if (!hasGsap || reduceMotion || !window.ScrollTrigger) { el.textContent = end; return; }
      const state = { value: 0 };
      gsap.to(state, {
        value: end, duration: 1.8, ease: "power2.out",
        scrollTrigger: { trigger: el, start: "top 90%", once: true },
        onUpdate: () => { el.textContent = Math.round(state.value); },
      });
    });
  }

  /* ---------- Typewriter ---------- */
  function initTypewriter() {
    document.querySelectorAll("[data-typewriter]").forEach((el) => {
      let words;
      try { words = JSON.parse(el.dataset.typewriter); } catch (e) { return; }
      if (!words.length) return;
      if (reduceMotion) { el.textContent = words[0]; return; }
      let word = 0, char = 0, deleting = false;
      const tick = () => {
        const current = words[word];
        char += deleting ? -1 : 1;
        el.textContent = current.slice(0, char);
        let delay = deleting ? 40 : 85;
        if (!deleting && char === current.length) { deleting = true; delay = 1800; }
        else if (deleting && char === 0) { deleting = false; word = (word + 1) % words.length; delay = 350; }
        setTimeout(tick, delay);
      };
      tick();
    });
  }

  /* ---------- Magnetic buttons & spotlight cards ---------- */
  function initPointerEffects(root) {
    if (!finePointer || reduceMotion) return;
    (root || document).querySelectorAll("[data-magnetic]").forEach((el) => {
      if (el.dataset.magneticReady) return;
      el.dataset.magneticReady = "1";
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * 0.25;
        const y = (e.clientY - r.top - r.height / 2) * 0.35;
        el.style.transform = `translate(${x}px, ${y}px)`;
      });
      el.addEventListener("mouseleave", () => { el.style.transform = ""; });
    });
  }

  // One listener handles every spotlight card, including ones HTMX adds later.
  if (finePointer) {
    document.addEventListener("pointermove", (e) => {
      const card = e.target.closest && e.target.closest(".spotlight");
      if (!card) return;
      const r = card.getBoundingClientRect();
      card.style.setProperty("--mx", `${e.clientX - r.left}px`);
      card.style.setProperty("--my", `${e.clientY - r.top}px`);
    }, { passive: true });
  }

  /* ---------- Cursor glow ---------- */
  function initCursorGlow() {
    const glow = document.getElementById("cursor-glow");
    if (!glow || !finePointer || reduceMotion) return;
    let x = window.innerWidth / 2, y = window.innerHeight / 2, cx = x, cy = y;
    window.addEventListener("pointermove", (e) => { x = e.clientX; y = e.clientY; }, { passive: true });
    const loop = () => {
      cx += (x - cx) * 0.12; cy += (y - cy) * 0.12;
      glow.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      requestAnimationFrame(loop);
    };
    loop();
  }

  /* ---------- Nav state & scroll progress ---------- */
  function initScrollUI() {
    const nav = document.getElementById("site-nav");
    const progress = document.getElementById("scroll-progress");
    const update = () => {
      const y = window.scrollY;
      if (nav) nav.classList.toggle("nav-scrolled", y > 20);
      if (progress) {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
      }
    };
    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  /* ---------- Toast auto-hide ---------- */
  function initToasts() {
    document.querySelectorAll("[data-toast]").forEach((toast) => {
      setTimeout(() => {
        toast.style.transition = "opacity .4s, transform .4s";
        toast.style.opacity = "0";
        toast.style.transform = "translateY(-10px)";
        setTimeout(() => toast.remove(), 400);
      }, 6000);
    });
  }

  /* ---------- Boot ---------- */
  function boot() {
    initHero();
    initReveals(document);
    initCounters(document);
    initTypewriter();
    initPointerEffects(document);
    initCursorGlow();
    initScrollUI();
    initToasts();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();

  // Re-run animations for content that HTMX swaps in (project search results)
  document.addEventListener("htmx:afterSwap", (event) => {
    initReveals(event.detail.target);
    initPointerEffects(event.detail.target);
    if (window.ScrollTrigger) ScrollTrigger.refresh();
  });
})();
