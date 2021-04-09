from store import app


@app.route('/')
def index():
    return 'The Jewelry Gallery'
