import os
from flask import Flask, render_template, url_for
import natsort

app = Flask(__name__)
app.config['GALLERIES_FOLDER'] = os.path.join('static', 'galleries')
app.config['PLACEHOLDER_IMAGE'] = url_for('static', filename='images/placeholder_art_1.png')
app.config['NUM_STAGES'] = 3

def get_galleries_data():
    """Scans the filesystem to discover galleries and their data."""
    galleries = []
    base_path = app.config['GALLERIES_FOLDER']

    if not os.path.exists(base_path):
        return []

    gallery_dirs = [g for g in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, g))]
    gallery_dirs = natsort.natsorted(gallery_dirs)

    for gallery_name in gallery_dirs:
        gallery_path = os.path.join(base_path, gallery_name)

        # Determine the path for the final stage to get the thumbnail
        last_stage_name = f'stage-{app.config["NUM_STAGES"]}'
        last_stage_path = os.path.join(gallery_path, last_stage_name)

        thumbnail_url = app.config['PLACEHOLDER_IMAGE']
        if os.path.exists(last_stage_path):
            stage_images = [f for f in os.listdir(last_stage_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            if stage_images:
                thumbnail_url = url_for('static', filename=f'galleries/{gallery_name}/{last_stage_name}/{stage_images[0]}')

        galleries.append({
            'id': gallery_name,
            'name': gallery_name.replace('-', ' ').title(),
            'description': f'A collection from {gallery_name.replace("-", " ").title()}. View the developmental trail.',
            'thumbnail': thumbnail_url
        })

    return galleries

def get_gallery_detail_data(gallery_id):
    """
    Scans for a specific gallery's images and ensures there are always 3 stages,
    filling with placeholders if necessary.
    """
    gallery_path = os.path.join(app.config['GALLERIES_FOLDER'], gallery_id)

    if not os.path.exists(gallery_path):
        return None

    stages_data = []
    for i in range(1, app.config['NUM_STAGES'] + 1):
        stage_name = f'stage-{i}'
        stage_path = os.path.join(gallery_path, stage_name)

        image_url = app.config['PLACEHOLDER_IMAGE']
        description = f"Artwork for {stage_name.replace('-', ' ').title()} has not been uploaded yet."

        if os.path.exists(stage_path):
            images = [f for f in os.listdir(stage_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            if images:
                image_url = url_for('static', filename=f'galleries/{gallery_id}/{stage_name}/{images[0]}')
                description = f"This is the artwork from {stage_name.replace('-', ' ').title()}."

        stages_data.append({
            'name': stage_name.replace('-', ' ').title(),
            'image_url': image_url,
            'description': description
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
    """Renders the individual gallery detail page with a guaranteed 3 stages."""
    gallery_data = get_gallery_detail_data(gallery_id)
    if gallery_data is None:
        return "Gallery not found", 404
    return render_template('gallery_detail.html', gallery=gallery_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
