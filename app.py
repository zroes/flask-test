from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import scrape


app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        # print(request.get_json())  # parse as JSON
        print(request.get_json())
        query = request.get_json()['query']
        includes = request.get_json()['includes']
        results = scrape.getData(query, includes)
        return jsonify(results), 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')