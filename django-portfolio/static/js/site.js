/* Portfolio interactions: smooth scroll, GSAP reveals, counters,
   progress bars, typewriter and HTMX hooks. Kept subtle on purpose:
   0.2s hovers (CSS), 0.6-0.7s reveals, no parallax or bouncing. */
(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const hasGsap = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";
  const EASE = "power3.out";

  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  /* ---------- Smooth scrolling (Lenis) ---------- */
  if (!reduceMotion && typeof window.Lenis !== "undefined") {
    const lenis = new Lenis({ duration: 1.0, smoothWheel: true });
    if (hasGsap) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add((time) => lenis.raf(time * 1000));
      gsap.ticker.lagSmoothing(0);
    } else {
      const raf = (time) => { lenis.raf(time); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
    document.addEventListener("click", (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link || link.getAttribute("href").length < 2) return;
      const target = document.querySelector(link.getAttribute("href"));
      if (target) { event.preventDefault(); lenis.scrollTo(target, { offset: -80 }); }
    });
  }

  // Reduced motion keeps a plain fade; everyone else gets fade + slide up.
  const fromState = () => (reduceMotion ? { opacity: 0 } : { opacity: 0, y: 24 });

  function showAll(root) {
    root.querySelectorAll("[data-reveal], [data-stagger] > *, [data-hero-item]").forEach((el) => { el.style.opacity = 1; });
    root.querySelectorAll("[data-bar]").forEach((bar) => { bar.style.transform = "none"; });
  }

  /* ---------- Hero: badge, heading lines, text, buttons in sequence ---------- */
  function initHero() {
    const items = document.querySelectorAll("[data-hero-item]");
    if (!items.length || !hasGsap) return;
    gsap.fromTo(items, fromState(), { opacity: 1, y: 0, duration: 0.7, ease: EASE, stagger: 0.1, delay: 0.05 });
  }

  /* ---------- Scroll reveals ---------- */
  function initReveals(root) {
    root = root || document;
    if (!hasGsap) { showAll(root); return; }

    root.querySelectorAll("[data-reveal]").forEach((el) => {
      if (el.dataset.revealed) return;
      el.dataset.revealed = "1";
      gsap.fromTo(el, fromState(), {
        opacity: 1, y: 0, duration: 0.6, ease: EASE,
        delay: parseFloat(el.dataset.delay || 0),
        scrollTrigger: { trigger: el, start: "top 88%", once: true },
      });
    });

    root.querySelectorAll("[data-stagger]").forEach((group) => {
      if (group.dataset.revealed) return;
      group.dataset.revealed = "1";
      gsap.fromTo(group.children, fromState(), {
        opacity: 1, y: 0, duration: 0.6, ease: EASE,
        stagger: parseFloat(group.dataset.stagger || 0.08),
        scrollTrigger: { trigger: group, start: "top 88%", once: true },
      });
    });

    // Progress bars fill from 0 to their width when scrolled into view
    root.querySelectorAll("[data-bar]").forEach((bar) => {
      if (bar.dataset.revealed) return;
      bar.dataset.revealed = "1";
      if (reduceMotion) return;
      gsap.fromTo(bar, { scaleX: 0, transformOrigin: "left center" }, {
        scaleX: 1, duration: 0.7, ease: EASE,
        scrollTrigger: { trigger: bar, start: "top 92%", once: true },
      });
    });
  }

  /* ---------- Count-up numbers ---------- */
  function initCounters(root) {
    (root || document).querySelectorAll("[data-count]").forEach((el) => {
      const end = parseInt(el.dataset.count, 10) || 0;
      if (!hasGsap || reduceMotion) { el.textContent = end; return; }
      const state = { value: 0 };
      el.textContent = "0";
      gsap.to(state, {
        value: end, duration: 0.7, ease: "power2.out",
        scrollTrigger: { trigger: el, start: "top 92%", once: true },
        onUpdate: () => { el.textContent = Math.round(state.value); },
      });
    });
  }

  /* ---------- Typewriter ---------- */
  function initTypewriter() {
    document.querySelectorAll("[data-typewriter]").forEach((el) => {
      let words;
      try { words = JSON.parse(el.dataset.typewriter); } catch (e) { return; }
      if (!words.length || reduceMotion) return;
      let word = 0, char = words[0].length, deleting = true;
      const tick = () => {
        const current = words[word];
        char += deleting ? -1 : 1;
        el.textContent = current.slice(0, char);
        let delay = deleting ? 35 : 70;
        if (!deleting && char === current.length) { deleting = true; delay = 2200; }
        else if (deleting && char === 0) { deleting = false; word = (word + 1) % words.length; delay = 300; }
        setTimeout(tick, delay);
      };
      setTimeout(tick, 2600);
    });
  }

  /* ---------- Navbar border/shadow once the page scrolls ---------- */
  function initNav() {
    const nav = document.getElementById("site-nav");
    if (!nav) return;
    const update = () => nav.classList.toggle("is-scrolled", window.scrollY > 8);
    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  /* ---------- Toast auto-hide ---------- */
  function initToasts() {
    document.querySelectorAll("[data-toast]").forEach((toast) => {
      setTimeout(() => {
        toast.style.transition = "opacity .3s";
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
      }, 6000);
    });
  }

  /* ---------- Opening name reveal ----------
     Letters slide up, a navy line draws under the name, it holds briefly, then the white
     screen lifts away and the hero animates in. About 2s, skippable
     with a click or any key, and shown only once per browser tab. */
  function playIntro(onDone) {
    const root = document.documentElement;
    const screen = document.querySelector(".intro-screen");
    if (!root.classList.contains("intro") || !screen) { onDone(); return; }

    let started = false;
    const startPage = () => { if (!started) { started = true; onDone(); } };
    const finish = () => {
      startPage();
      root.classList.remove("intro");
      try { sessionStorage.setItem("intro-seen", "1"); } catch (e) { /* ignore */ }
      window.removeEventListener("keydown", skip);
    };
    const fail = setTimeout(finish, 4000); // never trap the visitor behind the intro

    if (!hasGsap) { clearTimeout(fail); finish(); return; }

    // Wrap each letter so it can slide up on its own.
    const name = screen.querySelector("[data-intro-name]");
    name.innerHTML = name.textContent.split("").map((ch) => `<span class="intro-char">${ch}</span>`).join("");

    const tl = gsap.timeline({ defaults: { ease: EASE } });
    tl.from(name.querySelectorAll(".intro-char"), { yPercent: 110, duration: 0.55, stagger: 0.03 })
      .to(screen.querySelector(".intro-line"), { scaleX: 1, duration: 0.5, ease: "power2.inOut" }, "-=0.3")
      .to(screen.querySelector(".intro-role"), { opacity: 1, duration: 0.35 }, "-=0.25")
      .to(screen, { yPercent: -100, duration: 0.65, ease: "power4.inOut" }, "+=0.65") // name stays on screen a moment
      .add(startPage, "-=0.35") // hero starts animating as the curtain clears
      .add(() => { clearTimeout(fail); finish(); });

    function skip() { tl.progress(1); }
    screen.addEventListener("click", skip, { once: true });
    window.addEventListener("keydown", skip);
  }

  function boot() {
    playIntro(initHero);
    initReveals(document);
    initCounters(document);
    initTypewriter();
    initNav();
    initToasts();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();

  // Animate project cards that HTMX swaps in after a search
  document.addEventListener("htmx:afterSwap", (event) => {
    initReveals(event.detail.target);
    if (hasGsap) ScrollTrigger.refresh();
  });
})();
