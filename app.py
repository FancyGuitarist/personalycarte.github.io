from flask import Flask, render_template
from pathlib import Path

root_path = Path(__file__).parent
app = Flask(__name__, template_folder=root_path)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
