// This script initializes the Masonry layout for the gallery grid.

document.addEventListener('DOMContentLoaded', function() {
    const grid = document.querySelector('.gallery-grid');

    if (grid) {
        // Initialize Masonry after all images have been loaded
        imagesLoaded(grid, function() {
            new Masonry(grid, {
                itemSelector: '.gallery-card',
                columnWidth: '.grid-sizer', // Use a sizer element for column width
                percentPosition: true,
                gutter: 20 // The space between items
            });
        });
    }
});
