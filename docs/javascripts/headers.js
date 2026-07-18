function whenGsapReady(callback) {
  if (window.gsap && window.SplitText && window.ScrollTrigger) {
    callback();
  } else {
    requestAnimationFrame(() => whenGsapReady(callback));
  }
}

whenGsapReady(() => {
  gsap.registerPlugin(SplitText, ScrollTrigger);

  const headerInstances = [];

  function buildHeader(wrap) {
    const originalH4 = wrap.querySelector("h4");
    if (!originalH4 || originalH4.dataset.processed) return;
    originalH4.dataset.processed = "true";

    const originalHTML = originalH4.innerHTML;

    const computedStyle = window.getComputedStyle(originalH4);
    const fontSize = computedStyle.fontSize;
    const lineHeight = computedStyle.lineHeight;
    const fontWeight = computedStyle.fontWeight;
    const fontFamily = computedStyle.fontFamily;
    const color = computedStyle.color;

    // --- Static (dimmed) version ---
    const staticH4 = document.createElement("h4");
    staticH4.innerHTML = originalHTML;
    staticH4.className = "headertext-nonanimated";
    staticH4.style.fontSize = fontSize;
    staticH4.style.lineHeight = lineHeight;
    staticH4.style.fontWeight = fontWeight;
    staticH4.style.fontFamily = fontFamily;
    staticH4.style.color = color;
    staticH4.style.margin = "0";
    staticH4.style.padding = "0";
    staticH4.querySelectorAll("span.highlight").forEach(span => {
      span.replaceWith(document.createTextNode(span.textContent));
    });

    // --- Animated version ---
    const animatedH4 = originalH4;
    animatedH4.className = "headertext-animated";
    animatedH4.innerHTML = originalHTML;
    animatedH4.style.margin = "0";
    animatedH4.style.padding = "0";
    animatedH4.style.fontSize = fontSize;
    animatedH4.style.lineHeight = lineHeight;
    animatedH4.style.fontWeight = fontWeight;
    animatedH4.style.fontFamily = fontFamily;
    animatedH4.style.color = color;

    animatedH4.querySelectorAll("span.highlight").forEach(span => {
      span.replaceWith(document.createTextNode(span.textContent));
    });

    wrap.innerHTML = "";
    wrap.appendChild(staticH4);
    wrap.appendChild(animatedH4);

    // Ensure the wrap is a positioning context for the absolute layer
    wrap.style.position = wrap.style.position || "relative";

    staticH4.style.position = "relative";
    staticH4.style.zIndex = "1";
    staticH4.style.opacity = "0.2";
    staticH4.style.pointerEvents = "none";
    staticH4.style.userSelect = "none";
    staticH4.style.webkitUserSelect = "none";

    animatedH4.style.position = "absolute";
    animatedH4.style.top = "0";
    animatedH4.style.left = "0";
    animatedH4.style.width = "100%";
    animatedH4.style.height = "100%";
    animatedH4.style.zIndex = "2";
    animatedH4.style.visibility = "visible";

    // Split into words, preserving original spacing exactly
    const animatedSplit = new SplitText(animatedH4, {
      type: "words",
      wordsClass: "word",
      reduceWhiteSpace: false,
    });

    animatedSplit.words.forEach(word => {
      word.style.color = color;
      word.style.fontSize = fontSize;
      word.style.lineHeight = lineHeight;
      word.style.fontWeight = fontWeight;
      word.style.fontFamily = fontFamily;

      // Reset box model so word-splitting doesn't add stray spacing
      word.style.margin = "0";
      word.style.padding = "0";
      word.style.display = "inline-block";
      word.style.boxSizing = "border-box";
    });

    // Hide words immediately — prevents flash of unstyled/unanimated content
    gsap.set(animatedSplit.words, { opacity: 0 });

    headerInstances.push({
      wrap,
      animatedSplit,
    });
  }

  function playAnimation(instance) {
    const { animatedSplit } = instance;
    if (!animatedSplit || !animatedSplit.words) return;

    gsap.to(animatedSplit.words, {
      opacity: 1,
      duration: 0.6,
      ease: "power1.out",
      stagger: 0.06,
    });
  }

  function init() {
    document.querySelectorAll(".animated-header-wrap").forEach((wrap) => {
      buildHeader(wrap);
    });

    headerInstances.forEach(instance => {
      ScrollTrigger.create({
        trigger: instance.wrap,
        start: "top 80%",
        once: true,
        onEnter: () => playAnimation(instance),
      });
    });
  }

  init();
});