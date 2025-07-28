import os
from flask import Flask, render_template, url_for, jsonify, request, redirect, session, flash
import natsort
from PIL import Image
import random
from supabase import create_client, Client
from gotrue.errors import AuthApiError
import json
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a-default-fallback-secret-key-for-development')

# Supabase setup
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Check if Supabase credentials are provided
if not url or not key:
    print("Warning: Supabase URL or Key not provided. Authentication will not work.")
    supabase = None
else:
    supabase: Client = create_client(url, key)

# In-memory 'database' for frame selections. Maps gallery_id -> frame_class
FRAME_SELECTIONS = {}
app.config['GALLERIES_FOLDER'] = os.path.join('static', 'galleries')
app.config['NUM_STAGES'] = 3

# Define specific placeholders for each stage
app.config['PLACEHOLDER_PATHS'] = {
    1: 'images/placeholder_art_1.png',
    2: 'images/placeholder_art_2.png',
    3: 'images/placeholder_art_3.png'
}

def get_galleries_data():
    """Scans the filesystem to discover galleries, including image dimensions."""
    galleries = []
    base_path = app.config['GALLERIES_FOLDER']

    if not os.path.exists(base_path):
        return []

    gallery_dirs = [g for g in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, g))]
    gallery_dirs = natsort.natsorted(gallery_dirs)

    for i, gallery_name in enumerate(gallery_dirs):
        gallery_path = os.path.join(base_path, gallery_name)

        last_stage_name = f'stage-{app.config["NUM_STAGES"]}'
        last_stage_path = os.path.join(gallery_path, last_stage_name)

        thumbnail_path_rel = app.config['PLACEHOLDER_PATHS'][3] # Relative path

        if os.path.exists(last_stage_path):
            stage_images = [f for f in os.listdir(last_stage_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            if stage_images:
                thumbnail_path_rel = f'galleries/{gallery_name}/{last_stage_name}/{stage_images[0]}'

        # Get image dimensions using Pillow
        width, height = (None, None)
        is_placeholder = False
        try:
            with Image.open(os.path.join(app.static_folder, thumbnail_path_rel)) as img:
                width, height = img.size
        except FileNotFoundError:
            is_placeholder = True
            print(f"Warning: Thumbnail file not found at {thumbnail_path_rel}. Using random dimensions.")

        if is_placeholder:
            # Randomize dimensions for placeholders to create a more dynamic layout
            width = random.randint(600, 900)
            height = random.randint(400, 600)

        # Look up the selected frame, default to no frame
        selected_frame = FRAME_SELECTIONS.get(gallery_name, '')

        galleries.append({
            'id': gallery_name,
            'name': gallery_name.replace('-', ' ').title(),
            'description': f'A collection by {gallery_name.replace("-", " ").title()}.',
            'thumbnail_url': url_for('static', filename=thumbnail_path_rel),
            'width': width,
            'height': height,
            'frame_class': selected_frame
        })

    return galleries

@app.route('/select_frame/<gallery_id>/<frame_class>')
def select_frame_route(gallery_id, frame_class):
    """API endpoint to store the selected frame for a gallery."""
    if frame_class == 'no-frame': # Use a keyword for no frame
        FRAME_SELECTIONS[gallery_id] = ''
    else:
        FRAME_SELECTIONS[gallery_id] = frame_class
    print(f"Frame for {gallery_id} set to {FRAME_SELECTIONS.get(gallery_id)}") # Debug print
    return jsonify({'success': True, 'gallery_id': gallery_id, 'frame_class': FRAME_SELECTIONS.get(gallery_id)})

def get_gallery_detail_data(gallery_id):
    """
    Scans for a specific gallery's images and ensures there are always 3 stages,
    filling with the correct placeholder for each missing stage.
    """
    gallery_path = os.path.join(app.config['GALLERIES_FOLDER'], gallery_id)

    if not os.path.exists(gallery_path):
        return None

    # Read descriptions from text file
    descriptions = []
    desc_path = os.path.join(gallery_path, 'descriptions.txt')
    if os.path.exists(desc_path):
        with open(desc_path, 'r') as f:
            descriptions = [line.strip() for line in f.readlines()]

    stages_data = []
    for i in range(1, app.config['NUM_STAGES'] + 1):
        stage_name = f'stage-{i}'
        stage_path = os.path.join(gallery_path, stage_name)

        image_path = app.config['PLACEHOLDER_PATHS'][i]
        # Use description from file if available, otherwise use default
        description = descriptions[i-1] if i <= len(descriptions) else f"This is the artwork from Stage {i}."

        if os.path.exists(stage_path):
            images = [f for f in os.listdir(stage_path) if f.lower().endswith(('.png', 'jpg', 'jpeg', 'gif'))]
            if images:
                image_path = f'galleries/{gallery_id}/{stage_name}/{images[0]}'

        stages_data.append({
            'name': stage_name.replace('-', ' ').title(),
            'image_url': url_for('static', filename=image_path),
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

def find_custom_background():
    """Checks for a custom background image."""
    image_dir = os.path.join(app.static_folder, 'images')
    for ext in ['.png', '.jpg', '.jpeg', '.gif']:
        filename = 'showcase_background' + ext
        if os.path.exists(os.path.join(image_dir, filename)):
            return url_for('static', filename=f'images/{filename}')
    return None

@app.route('/showcase/')
def showcase_galleries():
    """Renders the showcase gallery overview page with dynamically found galleries."""
    galleries = get_galleries_data()
    custom_background = find_custom_background()
    return render_template('showcase_galleries.html', galleries=galleries, custom_background=custom_background)

@app.route('/showcase/gallery/<gallery_id>')
def gallery_detail(gallery_id):
    """Renders the individual gallery detail page with a guaranteed 3 stages."""
    gallery_data = get_gallery_detail_data(gallery_id)
    if gallery_data is None:
        return "Gallery not found", 404
    return render_template('gallery_detail.html', gallery=gallery_data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if not supabase:
            flash('Supabase not configured.', 'error')
            return redirect(url_for('signup'))
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            flash('Signup successful! Please check your email to verify.', 'success')
            return redirect(url_for('login'))
        except AuthApiError as e:
            flash(e.message, 'error')
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not supabase:
            flash('Supabase not configured.', 'error')
            return redirect(url_for('login'))
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            # Store user session
            session['user'] = res.user.dict()
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        except AuthApiError as e:
            flash(e.message, 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
