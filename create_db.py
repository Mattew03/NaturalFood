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
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    card TEXT NOT NULL
)
''')

# Crear la tabla de ítems de órdenes si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
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


# Verificar y agregar columna 'quantity' en order_items si no existe
cursor.execute("PRAGMA table_info(order_items)")
columns = [column[1] for column in cursor.fetchall()]
if 'quantity' not in columns:
    cursor.execute('ALTER TABLE order_items ADD COLUMN quantity INTEGER DEFAULT 1')

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("La base de datos está lista.")
