// Function to apply a selected frame style to ALL artwork containers on the page
function selectFrame(frameClass) {
    const artworkContainers = document.querySelectorAll('.artwork-frame-container');

    if (artworkContainers.length > 0) {
        artworkContainers.forEach(container => {
            // Remove any existing frame classes
            container.className = 'artwork-frame-container'; // Reset classes
            // Add the new frame class
            if (frameClass) {
                container.classList.add(frameClass);
            }
        });
        console.log(`Applied frame style: ${frameClass}`);
    } else {
        console.error('No artwork containers found on the page.');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("Art App JS Loaded");
});
