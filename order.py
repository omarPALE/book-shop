from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = 'orders.db'

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_number INTEGER
        )
    ''')
    conn.commit() 
    conn.close()

initialize_database()

@app.route('/purchase/<int:item_number>', methods=['POST'])
def purchase(item_number):
    # Check if item is in stock
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stock FROM catalog WHERE item_number = ?', (item_number,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return jsonify({'error': 'Book not found in catalog'}), 404

    stock = result[0]
    if stock == 0:
        conn.close()
        return jsonify({'error': 'Book out of stock'}), 400

    # Decrement stock
    cursor.execute('UPDATE catalog SET stock = ? WHERE item_number = ?', (stock - 1, item_number))
    conn.commit()

    # Record purchase
    conn.close()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (item_number) VALUES (?)', (item_number,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Purchase successful'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
