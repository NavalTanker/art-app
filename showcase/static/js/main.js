// Function to apply a selected frame style to ALL artwork containers on the page
function selectFrame(frameImageUrl) {
    // Get all elements with the class 'artwork-frame-container'
    const artworkContainers = document.querySelectorAll('.artwork-frame-container');

    if (artworkContainers.length > 0) {
        artworkContainers.forEach(container => {
            // Set the background image of the container to simulate a frame
            container.style.backgroundImage = `url('${frameImageUrl}')`;
            container.style.backgroundSize = '100% 100%'; // Stretch frame to fit container
            container.style.backgroundRepeat = 'no-repeat';
            container.style.backgroundPosition = 'center';

            // We can add a class to signify that a frame has been applied
            container.classList.add('frame-applied');
        });
        console.log(`Applied frame ${frameImageUrl} to ${artworkContainers.length} artworks.`);
    } else {
        console.error('No artwork containers found on the page.');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("Art App JS Loaded");
    // You can add more initialization logic here if needed
});
