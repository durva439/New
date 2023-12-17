from flask import Flask, request, jsonify, session
import sqlite3
import cursor

app=Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn 
        

@app.route('/books',methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3], genre=row[4])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)
            
    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        new_genre = request.form['genre']
        sql = """INSERT INTO book (author, language, title, genre)
                 VALUES (?, ?, ?, ?)"""
        cursor = cursor.execute(sql, (new_author, new_lang, new_title, new_genre))
        conn.commit()
        return f"Book with id:{cursor.lastrowid} created sucessfully"

@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
     conn = db_connection()
     cursor = conn.cursor()
     book = None
     if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404
            
        
     if request.method == 'PUT':
        sql = """UPDATE book SET title=?,author=?,language=?,genre=?
                 WHERE id=? """
        
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        genre = request.form['genre']
        updated_book = {
                    'id': id,
                    'author': author,
                    'language':language,
                    'title': title,
                    'genre': genre
                }
        conn.execute(sql, (author, language, title, genre, id))
        conn.commit()
        return jsonify(updated_book)
            
     if request.method == 'DELETE':
        sql = """ DELETE FROM book WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The book with id:{} has been deleted.".format(id),200      
                
        
    
if __name__ == '__main__':
    app.run(debug=True)