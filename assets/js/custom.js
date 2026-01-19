// Add scroll event listener to close search results
document.addEventListener('DOMContentLoaded', function() {
  let scrollTimer;
  
  window.addEventListener('scroll', function() {
    // Add scrolling class to body
    document.body.classList.add('scrolling');
    
    // Clear existing timer
    clearTimeout(scrollTimer);
    
    // Remove scrolling class after scroll stops
    scrollTimer = setTimeout(function() {
      document.body.classList.remove('scrolling');
    }, 150);
    
    // Close search results on scroll
    const searchResults = document.querySelector('.search-results');
    const searchInput = document.querySelector('#search-query');
    
    if (searchResults && searchInput) {
      searchResults.style.display = 'none';
      searchInput.blur(); // Remove focus from search input
    }
  });
  
  // Re-show search results when user focuses back on search
  const searchInput = document.querySelector('#search-query');
  if (searchInput) {
    searchInput.addEventListener('focus', function() {
      const searchResults = document.querySelector('.search-results');
      if (searchResults && this.value.length > 0) {
        searchResults.style.display = 'block';
      }
    });
  }
});
