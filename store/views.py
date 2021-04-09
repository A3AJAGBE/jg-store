from flask import render_template
from datetime import datetime
from store import app

# Get the year
current_year = datetime.now().year


@app.route('/')
def index():
    return render_template('index.html', year=current_year)
