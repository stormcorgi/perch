// Perch Application Scripts

document.addEventListener('DOMContentLoaded', function () {

  // ============================================================
  // Theme Toggle (dark / light)
  // ============================================================
  const html = document.documentElement;
  const themeToggle = document.getElementById('theme-toggle');

  // Restore saved theme
  const saved = localStorage.getItem('perch-theme');
  if (saved === 'light') {
    html.classList.remove('dark');
  } else {
    html.classList.add('dark'); // default dark
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const isDark = html.classList.toggle('dark');
      localStorage.setItem('perch-theme', isDark ? 'dark' : 'light');
    });
  }

  // ============================================================
  // Actress Search (main page)
  // ============================================================
  const searchInput = document.getElementById('actress-search');
  const actressCards = document.querySelectorAll('.actress-card');

  if (searchInput && actressCards.length) {
    // Store original names in data attribute
    actressCards.forEach(function (card) {
      // data-name already set by Jinja2
    });

    searchInput.addEventListener('input', function () {
      const q = this.value.toLowerCase().trim();
      let visibleCount = 0;

      actressCards.forEach(function (card) {
        const name = (card.dataset.name || '').toLowerCase();
        if (name.includes(q)) {
          card.classList.remove('hidden');
          visibleCount++;
        } else {
          card.classList.add('hidden');
        }
      });

      // Show "no results" message
      const emptyMsg = document.getElementById('search-empty');
      if (emptyMsg) {
        emptyMsg.classList.toggle('hidden', visibleCount > 0);
      }

      // Update count
      const countEl = document.getElementById('actress-count');
      if (countEl) {
        countEl.textContent = visibleCount;
      }
    });

    // Clear search on Escape
    searchInput.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        this.value = '';
        this.dispatchEvent(new Event('input'));
        this.blur();
      }
    });
  }

  // ============================================================
  // Image lazy loading
  // ============================================================
  const lazyImages = document.querySelectorAll('img[loading="lazy"]');
  if ('loading' in HTMLImageElement.prototype) {
    // Native lazy loading supported — already set via HTML attr
  } else {
    // Fallback: IntersectionObserver for older browsers
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src || img.src;
          observer.unobserve(img);
        }
      });
    });
    lazyImages.forEach(function (img) {
      observer.observe(img);
    });
  }

});
