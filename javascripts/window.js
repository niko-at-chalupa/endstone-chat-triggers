document.addEventListener("DOMContentLoaded", (event) => {
  if (typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined") {
    gsap.registerPlugin(ScrollTrigger);

    ScrollTrigger.batch("blockquote", {
      start: "top 85%",
      onEnter: (batch) => {
        gsap.to(batch, {
          opacity: 1,
          y: 0,
          duration: 0.5,
          ease: "power4.out",
          stagger: {
            amount: 0.05,
            grid: "auto",
            from: "start"
          }
        });
      },
      once: true
    });
  }
});

document.addEventListener("DOMContentLoaded", (event) => {
  if (typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined") {
    gsap.registerPlugin(ScrollTrigger);

    ScrollTrigger.batch(".grid.cards > ul > li", {
      start: "top 85%",
      onEnter: (batch) => {
        gsap.to(batch, {
          opacity: 1,
          y: 0,
          duration: 0.5,
          ease: "power4.out",
          stagger: {
            amount: 0.05,
            grid: "auto",
            from: "start"
          }
        });
      },
      once: true
    });
  }
});
