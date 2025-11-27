document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('searchInput');
  const newsCards = document.querySelectorAll('.news-card');
  const categoryButtons = document.querySelectorAll('.category-btn');

  function filterNews() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = document.querySelector('.category-btn.active')?.dataset.category || 'Semua';

    newsCards.forEach(card => {
      const title = card.querySelector('h2').textContent.toLowerCase();
      const excerpt = card.querySelector('p').textContent.toLowerCase();
      const category = card.dataset.category;

      if (
        (title.includes(searchTerm) || excerpt.includes(searchTerm)) &&
        (selectedCategory === 'Semua' || category === selectedCategory)
      ) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  }

  searchInput.addEventListener('input', filterNews);

  categoryButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      categoryButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterNews();
    });
  });
});
