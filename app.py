from flask import (Flask, g, flash, redirect, render_template, request, session, url_for)
import db


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/studentpage')
def studentpage():
    load_logged_in_student()
    return render_template('student_page.html')

@app.route('/adminpage', methods=['GET', 'POST'])
def adminpage():
    load_logged_in_admin()
    whatToShow=''
    if request.method == 'POST':
        if(request.form['subject_selection']=='select'):
            subject_selected = request.form['subject_selection2']
        else:
            subject_selected = request.form['subject_selection']
        print("subject : ",subject_selected)
        whatToShow='courses for a subject'
    sub_list = renderSearches(whatToShow)
    abb_list = getAllSubAbbreviation()
    return render_template('admin_page.html', subject_abb_list=abb_list, subject_list=sub_list)

def getAllSubAbbreviation():
    conn = db.start_db()
    cur = conn.cursor()
    cur.execute("SELECT abbreviation from subjects")
    return cur.fetchall()

def renderSearches(whatToShow):
    conn = db.start_db()
    cur = conn.cursor()
    if whatToShow=='all subjects':
        cur.execute("SELECT * FROM subjects")
        return cur.fetchall()
        #print(cur.fetchall())


@app.route('/adminlogin', methods=('GET', 'POST'))
def adminlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = db.start_db()
        cur = conn.cursor()
        error = None
        cur.execute("SELECT password FROM admin_info where username = %s", (username,))
        user = cur.fetchone()
        print(user)
        if user is None:
            error = 'Incorrect username.'
        elif (user[0] != password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = username
            return redirect(url_for('adminpage'))
        flash(error)
    return render_template('admin_login.html')

@app.route('/studentlogin', methods=('GET', 'POST'))
def studentlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = db.start_db()
        cur = conn.cursor()
        error = None
        cur.execute("SELECT password FROM student_login_info where username = %s", (username,))
        user = cur.fetchone()
        print(user)
        if user is None:
            error = 'Incorrect username.'
        elif (user[0] != password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = username
            return redirect(url_for('studentpage'))
        flash(error)
    return render_template('student_login.html')

def load_logged_in_admin():
    username = session.get('user_id')
    if username is None:
        g.user = None
    else:
        conn = db.start_db()
        cur = conn.cursor()
        cur.execute('SELECT username FROM admin_info WHERE username = %s', (username,))
        g.user = cur.fetchone()

def load_logged_in_student():
    username = session.get('user_id')
    if username is None:
        g.user = None
    else:
        conn = db.start_db()
        cur = conn.cursor()
        cur.execute('SELECT username FROM student_login_info WHERE username = %s', (username,))
        g.user = cur.fetchone()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('adminlogin'))


