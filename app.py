from flask import Flask, request, jsonify, render_template
from database import Database

app = Flask(__name__)

# Neo4j configuration
uri = "neo4j+ssc://af4ae13c.databases.neo4j.io"
username = "neo4j"
password = "uxIzr3XjB7RXu8wsIeYO_E8OTKfZhxdnRZwlUicNdLU"
db = Database(uri, username, password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_author', methods=['POST'])
def add_author():
    data = request.json
    name = data['name']
    db.add_author(name)
    return jsonify({"message": "Author added!"})

@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.json
    title = data['title']
    year = data.get('year', 'Unknown')
    db.add_book(title, year)
    return jsonify({"message": "Book added!"})

@app.route('/link_author_book', methods=['POST'])
def link_author_book():
    data = request.json
    author = data['author']
    book = data['book']
    result = db.link_author_book(author, book)
    return jsonify(result)

@app.route('/get_books_by_author/<author>', methods=['GET'])
def get_books_by_author(author):
    books = db.get_books_by_author(author)
    if not books:
        return jsonify({"message": "No books found for this author."})
    return jsonify(books)

@app.route('/delete_author', methods=['DELETE'])
def delete_author():
    data = request.json
    name = data['name']
    result = db.delete_author(name)
    return jsonify(result)

@app.route('/delete_book', methods=['DELETE'])
def delete_book():
    data = request.json
    title = data['title']
    result = db.delete_book(title)
    return jsonify(result)

@app.route('/get_all_authors', methods=['GET'])
def get_all_authors():
    authors = db.get_all_authors()
    if not authors:
        return jsonify({"message": "No authors found."})
    return jsonify(authors)

@app.route('/get_all_books', methods=['GET'])
def get_all_books():
    books = db.get_all_books()
    if not books:
        return jsonify({"message": "No books found."})
    return jsonify(books)

@app.route('/find_co_authors/<author>', methods=['GET'])
def find_co_authors(author):
    co_authors = db.find_co_authors(author)
    if not co_authors:
        return jsonify({"message": "No co-authors found for this author."})
    return jsonify(co_authors)

@app.route('/find_books_by_multiple_authors', methods=['POST'])
def find_books_by_multiple_authors():
    data = request.json
    authors = data['authors']
    books = db.find_books_by_multiple_authors(authors)
    if not books:
        return jsonify({"message": "No books found for these authors."})
    return jsonify(books)

@app.route('/get_authors_by_book/<book_title>', methods=['GET'])
def get_authors_by_book(book_title):
    authors = db.get_authors_by_book(book_title)
    return jsonify(authors)

@app.route('/get_books_by_year_range', methods=['GET'])
def get_books_by_year_range():
    start_year = int(request.args.get('start'))
    end_year = int(request.args.get('end'))
    books = db.get_books_by_year_range(start_year, end_year)
    return jsonify(books)

@app.route('/find_shortest_path', methods=['GET'])
def find_shortest_path():
    author1 = request.args.get('author1')
    author2 = request.args.get('author2')
    if not author1 or not author2:
        return jsonify({"message": "Both author1 and author2 parameters are required"}), 400

    path = db.find_shortest_path_between_authors(author1, author2)
    if 'path' in path:
        return jsonify({"path": path['path']})
    else:
        return jsonify({"message": path['message']}), 404

if __name__ == '__main__':
    app.run(debug=True)