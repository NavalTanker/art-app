from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('home.html')

@app.route('/showcase/')
def showcase_galleries():
    """Renders the showcase gallery overview page."""
    # In a real app, you might fetch gallery data from a database here
    num_galleries = 6 # Matching the template
    return render_template('showcase_galleries.html', num_galleries=num_galleries)

@app.route('/showcase/gallery/<int:gallery_id>')
def gallery_detail(gallery_id):
    """Renders the individual gallery detail page."""
    # In a real app, you'd fetch specific gallery data based on gallery_id
    # For now, we just pass the ID to the template
    num_art_stages = 3 # Matching the template
    num_frames = 4 # Matching the template
    return render_template('gallery_detail.html', gallery_id=gallery_id, num_art_stages=num_art_stages, num_frames=num_frames)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
