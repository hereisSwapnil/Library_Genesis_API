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
        books = book.book_get(str(request.args['name']),int(request.args['res']))
        return jsonify(books)
    except:
        books = book.book_get(str(request.args['name']))
        return jsonify(books)

        
app.run(threaded=True, port=5000)