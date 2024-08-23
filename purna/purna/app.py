from flask import Flask, render_template, request
import artwork_description  # Import your script with the image-to-text and emotion analysis functions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_url = request.form['image_url']
        description, emotion = artwork_description.main(image_url)  # Assuming you have a function that does this
        return render_template('index.html', description=description, emotion=emotion)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)