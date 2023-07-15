from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure SQLite database
conn = sqlite3.connect('users.db',check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
conn.commit()

@app.route('/')
def index():
    if 'failed_attempts' not in session:
        session['failed_attempts'] = 0
    return render_template('index.html', error_message=session.get('error_message'))

@app.route('/report', methods=['POST'])
def report():
    username = request.form['username']
    password = request.form['password']

    # Password format checking
    valid = (any(c.islower() for c in password) and any(c.isupper() for c in password) and password[-1].isdigit() and
        len(password) >= 8)
    v1 = 1
    v2 = 1
    v3 = 1
    v4 = 1
    if any(c.islower() for c in password):
        v1=0
    if  any(c.isupper() for c in password):
        v2 = 0
    if password[-1].isdigit() :
        v3 = 0
    if len(password) >= 8 :
        v4 = 0
    if valid:
        # Store username and password in the database
        c.execute('INSERT INTO users VALUES (?, ?)', (username, password))
        conn.commit()
        session['failed_attempts'] = 0  # Reset failed attempts counter
    else:
        # Check failed attempts and display error message if necessary
        session['failed_attempts'] += 1
        if session['failed_attempts'] >= 3:
            session['error_message'] = "Three consecutive failed attempts. Please try again later."
            return redirect('/')
    
    return render_template('report.html', valid=valid , v1=v1,v2=v2,v3=v3,v4=v4)

if __name__ == '__main__':
    app.run(debug=True)
