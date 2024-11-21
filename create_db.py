import sqlite3

# Crear la conexión a la base de datos
conn = sqlite3.connect('cart.db')
cursor = conn.cursor()

# Crear la tabla de productos si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT NOT NULL
)
''')

# Crear la tabla de carrito si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

# Crear la tabla de órdenes si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders_complete (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    card TEXT NOT NULL,
    product_name TEXT NOT NULL,
    product_price REAL NOT NULL,
    product_image TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1
)
''')

# Insertar productos iniciales solo si no existen
cursor.execute('SELECT COUNT(*) FROM products')
if cursor.fetchone()[0] == 0:
    products = [
        ('Bebida Energética', 5.00, 'images/bebida.jpg'),
        ('Chía Orgánica', 8.00, 'images/superfood.jpg'),
        ('Té de Manzanilla', 10.00, 'images/botanico.jpg')
    ]
    cursor.executemany('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', products)

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("La base de datos está lista.")
