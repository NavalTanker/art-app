// Function to apply a selected frame style and save it to the backend
function selectFrame(galleryId, frameClass) {
    const artworkContainers = document.querySelectorAll('.artwork-frame-container');

    // 1. Visually update the frames on the current page
    if (artworkContainers.length > 0) {
        artworkContainers.forEach(container => {
            container.className = 'artwork-frame-container'; // Reset classes
            if (frameClass) {
                container.classList.add(frameClass);
            }
        });
    }

    // 2. Send the choice to the backend to persist it
    const frameClassForApi = frameClass ? frameClass : 'no-frame';
    fetch(`/select_frame/${galleryId}/${frameClassForApi}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(`Frame for ${data.gallery_id} successfully set to ${data.frame_class}`);
            } else {
                console.error('Failed to set frame.');
            }
        })
        .catch(error => console.error('Error selecting frame:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("Art App JS Loaded");

    // Modal functionality
    const aboutModal = document.getElementById('about-modal');
    const aboutButton = document.getElementById('about-button');
    const closeButton = document.querySelector('.close-button');

    if (aboutButton) {
        aboutButton.onclick = function() {
            aboutModal.style.display = 'block';
        }
    }

    if (closeButton) {
        closeButton.onclick = function() {
            aboutModal.style.display = 'none';
        }
    }

    window.onclick = function(event) {
        if (event.target == aboutModal) {
            aboutModal.style.display = 'none';
        }
    }
});
