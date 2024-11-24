from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="", 
        database="atk"
    )
    return connection

@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM barang")
    barang = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("index.html", barang=barang)

@app.route("/tambah", methods=["GET", "POST"])
def tambah_barang():
    if request.method == "POST":
        nama_barang = request.form["nama_barang"]
        kategori = request.form["kategori"]
        harga = request.form["harga"]
        stok = request.form["stok"]
        
        if not nama_barang or not harga or not stok:
            flash("Semua kolom harus diisi!", "error")
            return redirect(url_for("tambah_barang"))

        try:
            harga = float(harga)  
            stok = int(stok)  
        except ValueError:
            flash("Harga dan stok harus berupa angka valid!", "error")
            return redirect(url_for("tambah_barang"))

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO barang (nama_barang, kategori, harga, stok) VALUES (%s, %s, %s, %s)", 
            (nama_barang, kategori, harga, stok)
        )
        connection.commit()
        cursor.close()
        connection.close()
        flash("Barang berhasil ditambahkan!", "success")
        return redirect(url_for("index"))
    
    return render_template("tambah_barang.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_barang(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM barang WHERE id = %s", (id,))
    barang = cursor.fetchone()

    if request.method == "POST":
        nama_barang = request.form["nama_barang"]
        kategori = request.form["kategori"]
        harga = request.form["harga"]
        stok = request.form["stok"]
        
        if not nama_barang or not harga or not stok:
            flash("Semua kolom harus diisi!", "error")
            return redirect(url_for("edit_barang", id=id))

        try:
            harga = float(harga) 
            stok = int(stok)
        except ValueError:
            flash("Harga dan stok harus berupa angka valid!", "error")
            return redirect(url_for("edit_barang", id=id))

        cursor.execute(
            "UPDATE barang SET nama_barang = %s, kategori = %s, harga = %s, stok = %s WHERE id = %s",
            (nama_barang, kategori, harga, stok, id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        flash("Barang berhasil diperbarui!", "success")
        return redirect(url_for("index"))

    cursor.close()
    connection.close()
    return render_template("edit_barang.html", barang=barang)

@app.route("/hapus/<int:id>", methods=["GET"])
def hapus_barang(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM barang WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash("Barang berhasil dihapus!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
