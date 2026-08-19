from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Create database and table
def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Display all products
@app.route("/")
def index():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    return render_template("index.html", products=products)


# Add a new product
@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"]
    quantity = request.form["quantity"]
    price = request.form["price"]

    conn = sqlite3.connect("inventory.db")
    conn.execute(
        "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
        (name, quantity, price)
    )
    conn.commit()
    conn.close()

    return redirect("/")


# Delete a product
@app.route("/delete/<int:id>")
def delete_product(id):
    conn = sqlite3.connect("inventory.db")
    conn.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


# Edit product page
@app.route("/edit/<int:id>")
def edit_product(id):
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (id,)
    ).fetchone()
    conn.close()

    return render_template("edit.html", product=product)


# Update product
@app.route("/update/<int:id>", methods=["POST"])
def update_product(id):
    name = request.form["name"]
    quantity = request.form["quantity"]
    price = request.form["price"]

    conn = sqlite3.connect("inventory.db")
    conn.execute("""
        UPDATE products
        SET name = ?, quantity = ?, price = ?
        WHERE id = ?
    """, (name, quantity, price, id))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)