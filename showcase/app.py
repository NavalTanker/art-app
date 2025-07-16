import os
from flask import Flask, render_template, url_for, jsonify
import natsort # For natural sorting of directory names (e.g., 'stage-1', 'stage-2', 'stage-10')

app = Flask(__name__)
app.config['GALLERIES_FOLDER'] = os.path.join('static', 'galleries')

def get_galleries_data():
    """Scans the filesystem to discover galleries and their data."""
    galleries = []
    base_path = app.config['GALLERIES_FOLDER']

    if not os.path.exists(base_path):
        return []

    # Get list of gallery directories, ignore files like .DS_Store
    gallery_dirs = [g for g in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, g))]

    # Sort galleries naturally (e.g., gallery-1, gallery-2, gallery-10)
    gallery_dirs = natsort.natsorted(gallery_dirs)

    for gallery_name in gallery_dirs:
        gallery_path = os.path.join(base_path, gallery_name)

        # Get stages, sort them naturally
        stage_dirs = [s for s in os.listdir(gallery_path) if os.path.isdir(os.path.join(gallery_path, s)) and s.startswith('stage-')]
        sorted_stages = natsort.natsorted(stage_dirs)

        if not sorted_stages:
            continue

        # Find the thumbnail: image from the last stage
        thumbnail_url = url_for('static', filename='images/placeholder_gallery.png') # Default
        last_stage_path = os.path.join(gallery_path, sorted_stages[-1])

        # Find first image in the last stage folder
        stage_images = [f for f in os.listdir(last_stage_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if stage_images:
            # Construct URL path correctly
            thumbnail_url = url_for('static', filename=f'galleries/{gallery_name}/{sorted_stages[-1]}/{stage_images[0]}')

        galleries.append({
            'id': gallery_name,
            'name': gallery_name.replace('-', ' ').title(),
            'description': f'A collection of works from {gallery_name.replace("-", " ").title()}.',
            'thumbnail': thumbnail_url
        })

    return galleries

def get_gallery_detail_data(gallery_id):
    """Scans the filesystem for a specific gallery's stages and images."""
    gallery_path = os.path.join(app.config['GALLERIES_FOLDER'], gallery_id)

    if not os.path.exists(gallery_path):
        return None

    # Get stages, sort them naturally
    stage_dirs = [s for s in os.listdir(gallery_path) if os.path.isdir(os.path.join(gallery_path, s)) and s.startswith('stage-')]
    sorted_stages = natsort.natsorted(stage_dirs)

    stages_data = []
    for stage_name in sorted_stages:
        stage_path = os.path.join(gallery_path, stage_name)
        images = [f for f in os.listdir(stage_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if images:
            # For simplicity, we take the first image found in the stage folder.
            image_url = url_for('static', filename=f'galleries/{gallery_id}/{stage_name}/{images[0]}')
            stages_data.append({
                'name': stage_name.replace('-', ' ').title(),
                'image_url': image_url,
                'description': f"This is the artwork from {stage_name.replace('-', ' ').title()}."
            })

    return {
        'id': gallery_id,
        'name': gallery_id.replace('-', ' ').title(),
        'stages': stages_data
    }


@app.route('/')
def home():
    """Renders the home page."""
    return render_template('home.html')

@app.route('/showcase/')
def showcase_galleries():
    """Renders the showcase gallery overview page with dynamically found galleries."""
    galleries = get_galleries_data()
    return render_template('showcase_galleries.html', galleries=galleries)

@app.route('/showcase/gallery/<gallery_id>')
def gallery_detail(gallery_id):
    """Renders the individual gallery detail page with dynamically found stages."""
    gallery_data = get_gallery_detail_data(gallery_id)
    if gallery_data is None:
        return "Gallery not found", 404
    return render_template('gallery_detail.html', gallery=gallery_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
