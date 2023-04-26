from flask import Flask, g
import psycopg2

app = flask(__name__)

def get_db():
    db=getattr(g,'_database',None)
    if db in None:
        db = psycopg2.connect(
                                user="postgres",
                                password="PIKqPhxx35Ymhm3MIgdR",
                                host="containers-us-west-17.railway.app",
                                port="5679",
                                database="railway"
                                )
    return db

@app.teardown_appcontext
def close_connection(exception):
    db=getattr(g,'_database',None)
    if db is not None:
        db.close()

@app.route('/',methods=['GET'])
def home():
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM books_table")
    totalRows=cursor.fetchall()
    num_books=len(totalRows)
    cursor.close()

    home_display=f"""
    <h1>API Books</h1>
    <p>API w/ {num_books} Books."""
    return home_display

if __name__ == '__main__':
    app.run(debug=True)
