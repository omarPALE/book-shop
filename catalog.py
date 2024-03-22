from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = 'catalog.db'

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS catalog (
            item_number INTEGER PRIMARY KEY,
            title TEXT,
            stock INTEGER,
            cost REAL,
            topic TEXT
        )
    ''')
    initial_data = [
        (1, "How to get a good grade in DOS in 40 minutes a day", 10, 25.0, "distributed systems"),
        (2, "RPCs for Noobs", 15, 30.0, "distributed systems"),
        (3, "Xen and the Art of Surviving Undergraduate School", 20, 20.0, "undergraduate school"),
        (4, "Cooking for the Impatient Undergrad", 12, 35.0, "undergraduate school")
    ]

    for data in initial_data:
        cursor.execute('INSERT OR REPLACE INTO catalog (item_number, title, stock, cost, topic) VALUES (?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

initialize_database()

@app.route('/query', methods=['GET'])
def query_by_subject():
    topic = request.args.get('topic')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM catalog WHERE topic = ?', (topic,))
    books = cursor.fetchall()
    conn.close()
    return jsonify(books), 200

@app.route('/query/<int:item_number>', methods=['GET'])
def query_by_item(item_number):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM catalog WHERE item_number = ?', (item_number,))
    book = cursor.fetchone()
    conn.close()
    if book:
        return jsonify(book), 200
    else:
        return jsonify({'error': 'Book not found'}), 404

# Add update endpoint if needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
