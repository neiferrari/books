from flask import Flask, g, jsonify, request
import psycopg2

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = psycopg2.connect(
                                user = "postgres",
                                password = "PIKqPhxx35Ymhm3MIgdR",
                                host = "containers-us-west-17.railway.app",
                                port = "5679",
                                database = "railway"
                                )
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Get Home w/ #Books
@app.route('/',methods=['GET'])
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books_table")
    books = cursor.fetchall()
    num_books = len(books)
    cursor.close()
    home_display = f"""
    <h1>API Books</h1>
    <p>API w/ {num_books} Books.</p>"""
    return home_display

#Get Books
@app.route('/books', methods = ['GET'])
def get_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books_table")
    books = cursor.fetchall()
    cursor.close()
    return jsonify(books)

#To Add Book
@app.route('/resources/book/add',methods=['POST'])
def add_book():
    book = request.get_json()
    id_book = book['id']
    author = book['author']
    year = book['year']
    title = book['title']
    description = book['description']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books_table (id, author, year, title, description) VALUES (%s, %s, %s, %s, %s)", (id_book, author, year, title, description))
    conn.commit()
    return jsonify({'message': 'OK, Added Book'})

#To Delete Book
@app.route('/resources/book/delete/<int:id>',methods=['DELETE'])
def delete_book(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books_table WHERE id = %s",(id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'OK, Deleted Book'})

#To Update Book
@app.route('/resources/book/update/', methods=['PUT'])
def update_book():
    description=request.args['description']
    title=request.args['title']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE books_table SET description = %s WHERE title = %s", (description, title))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'OK, Updated Book'})

#Run App
if __name__ == '__main__':
    app.run(debug=True)