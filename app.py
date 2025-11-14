from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_bottoms_for_color(color_name):
    match_dict = {
        'red': ['black', 'white', 'beige'],
        'blue': ['white', 'khaki', 'grey'],
        'green': ['cream', 'brown', 'black'],
        'yellow': ['blue', 'denim', 'white'],
        'white': ['black', 'navy blue', 'red'],
        'black': ['grey', 'white', 'mustard'],
        'pink': ['white', 'blue', 'denim'],
        'orange': ['brown', 'white', 'olive'],
        'purple': ['black', 'grey', 'white'],
        'brown': ['cream', 'green', 'maroon'],
    }

    color = color_name.lower() if color_name else ''
    return match_dict.get(color, ['black', 'white', 'blue'])

def generate_links(bottom_color):
    base_links = {
        "Amazon": f"https://www.amazon.in/s?k={bottom_color}+pants",
        "Flipkart": f"https://www.flipkart.com/search?q={bottom_color}+pants",
        "Meesho": f"https://www.meesho.com/search?q={bottom_color}+pants",
        "Myntra": f"https://www.myntra.com/{bottom_color}-pants",
        "Ajio": f"https://www.ajio.com/search/?text={bottom_color}+pants"
    }
    return base_links

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        top_color = request.form.get('top_color')
        uploaded_file_urls = []

        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file.filename == '':
                    continue
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    uploaded_file_urls.append(f'uploads/{filename}')

        bottom_colors = get_bottoms_for_color(top_color)
        shopping_links = {color: generate_links(color) for color in bottom_colors}

        return render_template(
            'result.html',
            top_color=top_color,
            image_urls=uploaded_file_urls,
            bottom_colors=bottom_colors,
            shopping_links=shopping_links
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
