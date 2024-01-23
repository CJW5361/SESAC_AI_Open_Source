from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', image_names=[1, 2, 3, 4, 5, 6])

if __name__ == '__main__':
    app.run(debug=True)
