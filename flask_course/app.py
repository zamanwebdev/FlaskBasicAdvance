from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecretkey"

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        ''')
    conn.commit()
    conn.close()



init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()

        flash("User Added Successfully!", "success")
        return redirect(url_for('users'))

    return render_template('contact.html')

@app.route('/users')
def users():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    conn.close()

    return render_template('users.html', users=data)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("User Deleted!", "danger")
    return redirect(url_for('users'))
    # return "User Deleted! <br><a href='/users'>Back</a>"
    # return render_template('users.html')
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        cur.execute("UPDATE contacts SET name=?, email=? WHERE id=?", (name, email, id))
        conn.commit()
        conn.close()
        flash("User Updated!", "warning")
        return redirect(url_for('users'))

    cur.execute("SELECT * FROM contacts WHERE id=?", (id,))
    user = cur.fetchone()
    conn.close()

    return render_template('update.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        flash("Registration Successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')
# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            flash("Login Successful!", "success")
            return redirect(url_for('users'))
        else:
            flash("Invalid Credentials", "danger")

    return render_template('login.html')




if __name__ == "__main__":
    # app.run(debug=True, port=8000)
    app.run(debug=True)