from flask import Flask, jsonify, request, render_template
app = Flask(__name__)
import scrape

@app.route('/', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        # print(request.get_json())  # parse as JSON
        query = request.get_json()['query']
        results = scrape.getData(query)
        return jsonify(results), 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')