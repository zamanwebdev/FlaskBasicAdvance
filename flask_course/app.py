from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

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
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()

        # return f"Hello {username}, we received your message!"

        return f"Saved! Hello {name}, your email is {email}"
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
    return "User Deleted! <br><a href='/users'>Back</a>"

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
        return "Updated Successfully! <br><a href='/users'>Back</a>"

    cur.execute("SELECT * FROM contacts WHERE id=?", (id,))
    user = cur.fetchone()
    conn.close()

    return render_template('update.html', user=user)


if __name__ == "__main__":
    # app.run(debug=True, port=8000)
    app.run(debug=True)