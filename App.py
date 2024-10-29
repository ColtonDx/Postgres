from flask import Flask, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_write_db_connection():
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="mydbuser",
        password="MyDBPassword",
        host="dbwrite.contoso.com",
        port="5432"
    )
    return conn

def get_read_db_connection():
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="mydbuser",
        password="MyDBPassword",
        host="10.0.0.20",
        port="5432"
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    users = []
    search_performed = False
    if request.method == 'POST' and 'search' in request.form:
        search_term = request.form.get('search', '').strip()
        if search_term:
            conn = get_read_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE first_name LIKE %s OR last_name LIKE %s",
                           (f'%{search_term}%', f'%{search_term}%'))
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            search_performed = True

    return render_template('index.html', users=users, search_performed=search_performed)

@app.route('/add_user', methods=['POST'])
def add_user():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    if first_name and last_name:
        conn = get_write_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name) VALUES (%s, %s)", (first_name, last_name))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
