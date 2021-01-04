import os
from flask import Flask , render_template, jsonify, request, redirect, url_for, session, escape

app = Flask(__name__)

app.secret_key = "Super_secret_key"


@app.route('/')
def index():
    return "Hello"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
