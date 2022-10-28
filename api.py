import flask
from flask import request, jsonify
import book

app = flask.Flask(__name__)

# @app.route('/', methods=['GET'])
# def home():
#     pass

@app.route('/api/v1/resources/books', methods=['GET'])
def get_book_by_text():
    try:
        name = str(request.args['name'])
    except:
        name = ""
    
    try:
        mainres = int(request.args['mainres'])
    except:
        mainres = ""
    
    try:
        results = int(request.args['results'])
    except:
        results = ""

    if name != "":
        if mainres != "" and results == "":
            books = book.book_get(name = str(request.args['name']),mainres = int(request.args['mainres']))
            return jsonify(books)
        elif mainres == "" and results != "":
            books = book.book_get(name = str(request.args['name']),results = int(request.args['results']))
            return jsonify(books)
        elif mainres == "" and results == "":
            books = book.book_get(name = str(request.args['name']))
            return jsonify(books)
        elif mainres != "" and results != "":
            books = book.book_get(name = str(request.args['name']),mainres = int(request.args['mainres']),results = int(request.args['results']))
            return jsonify(books)
    elif name == "":
        books = book.book_get("")
        return jsonify(books)

        
app.run(threaded=True, port=5000)