document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".slide");
  const totalSlides = slides.length;
  const counterEl = document.getElementById("slideCounter");
  const progressFill = document.getElementById("progressFill");
  const btnPrev = document.getElementById("btnPrev");
  const btnNext = document.getElementById("btnNext");
  const btnFullscreen = document.getElementById("btnFullscreen");

  let currentIndex = 0;

  function getSlideIndexFromHash() {
    const hash = window.location.hash;
    if (hash && hash.startsWith("#")) {
      const pageNum = parseInt(hash.replace("#", ""), 10);
      if (!isNaN(pageNum) && pageNum >= 1 && pageNum <= totalSlides) {
        return pageNum - 1;
      }
    }
    return 0;
  }

  function updateSlide(index) {
    if (index < 0) index = 0;
    if (index >= totalSlides) index = totalSlides - 1;

    currentIndex = index;

    slides.forEach((slide, i) => {
      if (i === currentIndex) {
        slide.classList.add("active");
      } else {
        slide.classList.remove("active");
      }
    });

    // Update Counter
    if (counterEl) {
      counterEl.textContent = `#${currentIndex + 1} / ${totalSlides}`;
    }

    // Update Progress
    if (progressFill) {
      const pct = ((currentIndex + 1) / totalSlides) * 100;
      progressFill.style.width = `${pct}%`;
    }

    // Update URL hash without polluting history if replacing
    const targetHash = `#${currentIndex + 1}`;
    if (window.location.hash !== targetHash) {
      history.replaceState(null, null, targetHash);
    }
  }

  function nextSlide() {
    if (currentIndex < totalSlides - 1) {
      updateSlide(currentIndex + 1);
    }
  }

  function prevSlide() {
    if (currentIndex > 0) {
      updateSlide(currentIndex - 1);
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  }

  // Keyboard navigation
  window.addEventListener("keydown", (e) => {
    switch (e.key) {
      case "ArrowRight":
      case "PageDown":
      case " ":
        e.preventDefault();
        nextSlide();
        break;
      case "ArrowLeft":
      case "PageUp":
      case "Backspace":
        e.preventDefault();
        prevSlide();
        break;
      case "Home":
        e.preventDefault();
        updateSlide(0);
        break;
      case "End":
        e.preventDefault();
        updateSlide(totalSlides - 1);
        break;
      case "f":
      case "F":
        toggleFullscreen();
        break;
    }
  });

  // Buttons
  if (btnNext) btnNext.addEventListener("click", nextSlide);
  if (btnPrev) btnPrev.addEventListener("click", prevSlide);
  if (btnFullscreen) btnFullscreen.addEventListener("click", toggleFullscreen);

  // Hash change listener
  window.addEventListener("hashchange", () => {
    const targetIndex = getSlideIndexFromHash();
    if (targetIndex !== currentIndex) {
      updateSlide(targetIndex);
    }
  });

  // Init
  const initialIndex = getSlideIndexFromHash();
  updateSlide(initialIndex);
});
