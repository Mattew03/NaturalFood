from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('cart.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    # Obtener productos disponibles
    products = conn.execute('SELECT * FROM products').fetchall()

    # Obtener los ítems del carrito
    cart_items = conn.execute('''
        SELECT c.id AS cart_id, p.name, p.price, p.image, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
    ''').fetchall()

    # Calcular el total del carrito
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    conn.close()

    # Renderizar la plantilla con productos y carrito
    return render_template('index.html', products=products, cart_items=cart_items, total=total)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica si el producto ya está en el carrito
    cursor.execute('SELECT id, quantity FROM cart WHERE product_id = ?', (product_id,))
    item = cursor.fetchone()

    if item:
        # Incrementa la cantidad
        cursor.execute('UPDATE cart SET quantity = quantity + 1 WHERE id = ?', (item['id'],))
    else:
        # Inserta el producto con cantidad = 1
        cursor.execute('INSERT INTO cart (product_id, quantity) VALUES (?, 1)', (product_id,))

    conn.commit()
    conn.close()
    return redirect(url_for('index'))




@app.route('/update_cart/<int:cart_id>', methods=['POST'])
def update_cart(cart_id):
    action = request.form.get('action')
    conn = get_db_connection()

    if action == 'increase':
        conn.execute('UPDATE cart SET quantity = quantity + 1 WHERE id = ?', (cart_id,))
    elif action == 'decrease':
        conn.execute('UPDATE cart SET quantity = quantity - 1 WHERE id = ? AND quantity > 1', (cart_id,))
    elif action == 'remove':
        conn.execute('DELETE FROM cart WHERE id = ?', (cart_id,))
    
    conn.commit()
    conn.close()

    # Redirige al carrito sin cambiar a la página principal
    return redirect(url_for('index'))  # Mantiene el carrito en la vista actual


@app.route('/checkout', methods=['POST'])
def checkout():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    phone = request.form['phone']
    address = request.form['address']
    card = request.form['card']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Guarda la orden
    cursor.execute('''
        INSERT INTO orders (first_name, last_name, phone, address, card)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, phone, address, card))
    conn.commit()

    order_id = cursor.lastrowid

    # Obtén productos del carrito
    cart_items = conn.execute('SELECT product_id, quantity FROM cart').fetchall()

    # Inserta productos en order_items
    for item in cart_items:
        cursor.execute('''
            INSERT INTO order_items (order_id, product_id, quantity)
            VALUES (?, ?, ?)
        ''', (order_id, item['product_id'], item['quantity']))
    conn.commit()

    # Limpia el carrito
    conn.execute('DELETE FROM cart')
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)