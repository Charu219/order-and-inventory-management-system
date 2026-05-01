from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'secret123'

mysql = MySQL(app)

# ================= HOME =================
@app.route('/')
def home():
    return redirect(url_for('login'))


# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT id, role FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

        if user:
            session['user_id'] = user[0]
            session['role'] = user[1]

            if user[1] == 'admin':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('user_dashboard'))

        return "Invalid username or password"

    return render_template('login.html')


# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ================= ADMIN DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    # Total Orders
    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    # Delivered Orders
    cur.execute("SELECT COUNT(*) FROM orders WHERE status='DELIVERED'")
    delivered_orders = cur.fetchone()[0]

    # Cancelled Orders
    cur.execute("SELECT COUNT(*) FROM orders WHERE status='CANCELLED'")
    cancelled_orders = cur.fetchone()[0]

    # Total Revenue (ONLY delivered orders)
    cur.execute("""
        SELECT IFNULL(SUM(total_amount), 0)
        FROM orders
        WHERE status='DELIVERED'
    """)
    total_revenue = cur.fetchone()[0]

    # Daily sales (last 6 days)
    cur.execute("""
        SELECT DATE(order_date), SUM(total_amount)
        FROM orders
        WHERE status='DELIVERED'
        GROUP BY DATE(order_date)
        ORDER BY DATE(order_date) DESC
        LIMIT 6
    """)
    rows = cur.fetchall()

    cur.close()

    # Reverse so chart shows oldest → newest
    dates = [str(r[0]) for r in reversed(rows)]
    sales = [float(r[1]) for r in reversed(rows)]

    return render_template(
        'dashboard.html',
        total_revenue=total_revenue,
        total_orders=total_orders,
        delivered_orders=delivered_orders,
        cancelled_orders=cancelled_orders,
        months=dates,
        sales=sales
    )


# ================= USER DASHBOARD =================
@app.route('/user-dashboard')
def user_dashboard():
    if 'user_id' not in session or session['role'] != 'user':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM orders WHERE user_id=%s", (session['user_id'],))
    total_orders = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders WHERE user_id=%s AND status='DELIVERED'", (session['user_id'],))
    delivered = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders WHERE user_id=%s AND status='PLACED'", (session['user_id'],))
    active = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders WHERE user_id=%s AND status='CANCELLED'", (session['user_id'],))
    cancelled = cur.fetchone()[0]

    cur.execute("""
        SELECT order_id, order_date, total_amount, status
        FROM orders
        WHERE user_id=%s
        ORDER BY order_date DESC
        LIMIT 5
    """, (session['user_id'],))
    recent_orders = cur.fetchall()

    return render_template(
        'user_dashboard.html',
        total_orders=total_orders,
        delivered=delivered,
        active=active,
        cancelled=cancelled,
        recent_orders=recent_orders
    )


# ================= USER PRODUCTS =================
@app.route('/products')
def products():
    if 'user_id' not in session or session['role'] != 'user':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    return render_template('products.html', products=products)


# ================= ADMIN PRODUCTS =================
@app.route('/admin/products', methods=['GET', 'POST'])
def admin_products():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    # ✅ ADD PRODUCT
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']

        cur.execute(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
            (name, price, stock)
        )
        mysql.connection.commit()
        return redirect('/admin/products')

    # ✅ FETCH PRODUCTS
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    return render_template('admin_products.html', products=products)




@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (product_id,))

    mysql.connection.commit()

    return redirect(url_for('admin_products'))

    



# ================= USER ORDERS =================
@app.route('/orders')
def orders():
    if 'user_id' not in session or session['role'] != 'user':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT order_id, order_date, total_amount, status
        FROM orders
        WHERE user_id=%s
        ORDER BY order_date DESC
    """, (session['user_id'],))
    orders = cur.fetchall()

    return render_template('orders.html', orders=orders)


# ================= ADMIN ORDERS =================
@app.route('/admin/orders')
def admin_orders():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT order_id, user_id, order_date, total_amount, status
        FROM orders
        ORDER BY order_date DESC
    """)
    orders = cur.fetchall()
    cur.close()

    return render_template('admin_orders.html', orders=orders)



@app.route('/admin/order/update/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    new_status = request.form['status']

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE orders SET status=%s WHERE order_id=%s",
        (new_status, order_id)
    )
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('admin_orders'))





@app.route('/admin/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE order_id=%s", (order_id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('admin_orders'))











# ================= PLACE ORDER =================
@app.route('/place-order', methods=['POST'])
def place_order():
    if 'user_id' not in session or session['role'] != 'user':
        return redirect(url_for('login'))

    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    cur = mysql.connection.cursor()
    cur.execute("SELECT price, stock FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()

    if not product or product[1] < quantity:
        return redirect(url_for('products'))

    total = product[0] * quantity

    cur.execute(
        "INSERT INTO orders (user_id, order_date, total_amount, status) VALUES (%s, NOW(), %s, 'PLACED')",
        (session['user_id'], total)
    )
    order_id = cur.lastrowid

    cur.execute(
        "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
        (order_id, product_id, quantity)
    )

    cur.execute(
        "UPDATE products SET stock = stock - %s WHERE id = %s",
        (quantity, product_id)
    )

    mysql.connection.commit()
    return redirect(url_for('orders'))


# ================= CANCEL ORDER =================
@app.route('/cancel-order/<int:order_id>')
def cancel_order(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, status FROM orders WHERE order_id=%s", (order_id,))
    order = cur.fetchone()

    if not order or order[1] != 'PLACED':
        return redirect(url_for('orders'))

    if session['role'] != 'admin' and order[0] != session['user_id']:
        return "Access Denied", 403

    cur.execute(
        "SELECT product_id, quantity FROM order_items WHERE order_id=%s",
        (order_id,)
    )
    items = cur.fetchall()

    for item in items:
        cur.execute(
            "UPDATE products SET stock = stock + %s WHERE id=%s",
            (item[1], item[0])
        )

    cur.execute("UPDATE orders SET status='CANCELLED' WHERE order_id=%s", (order_id,))
    mysql.connection.commit()

    return redirect(url_for('orders'))


# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            return render_template('register.html', error="Username already exists")

        cur.execute("""
            INSERT INTO users
            (username, password, role, first_name, last_name, phone, email)
            VALUES (%s, %s, 'user', %s, %s, %s, %s)
        """, (username, password, first_name, last_name, phone, email))

        mysql.connection.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


# ================= SALES DATA =================
@app.route('/sales-data')
def sales_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT DATE(order_date), SUM(total_amount)
        FROM orders
        WHERE status='PLACED'
        GROUP BY DATE(order_date)
    """)
    data = cur.fetchall()

    return {'data': data}


# ================= RUN =================
if __name__ == '__main__':
    app.run()
