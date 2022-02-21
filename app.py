from flask import (Flask, g, flash, redirect, render_template, request, session, url_for)
import db


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def main():
    return render_template('entry.html')

@app.route('/studentpage')
def studentpage():
    load_logged_in_student()
    return render_template('student_page.html')

@app.route('/adminpage', methods=['GET', 'POST'])
def adminpage():
    load_logged_in_admin()
    if request.method == 'POST':
        if 'part 1' in request.form:
            return redirect(url_for('adminpage_1'))
        if 'part 2' in request.form:
            return redirect(url_for('adminpage_2'))
    return render_template('admin_page.html')

@app.route('/adminpage/1', methods=['GET', 'POST'])
def adminpage_1():
    load_logged_in_admin()
    whatToDo=''
    subject_selected=''
    inst_selected=''

    if request.method == 'POST':

        if 'subject go' in request.form:

            if(request.form['subject_selection']=='' and request.form['subject_selection2']=='select'):
                    whatToDo='nothing'
            elif(request.form['subject_selection']==''):
                subject_selected = request.form['subject_selection2']
                whatToDo='get instructors'
            else:
                subject_selected = request.form['subject_selection']
                whatToDo='get instructors'
            print("subject : ",subject_selected)

        if 'instructor go' in request.form:
            if(request.form['instructor_selection']=='' and request.form['instructor_selection2']=='select'):
                    whatToDo='nothing'
            elif(request.form['instructor_selection']==''):
                inst_selected = request.form['instructor_selection2']
                whatToDo='get instructors'
            else:
                inst_selected = request.form['instructor_selection']
                whatToDo='get instructors'
            print("instructor : ",inst_selected)
    inst_list = searchInstsForSub(subject_selected)
    abb_list = getAllSubAbbreviation()
    return render_template('admin_page_1.html', subject_abb_list=abb_list, instructor_list=inst_list, sub=subject_selected, inst=inst_selected)


@app.route('/adminpage/2', methods=['GET', 'POST'])
def adminpage_2():
    load_logged_in_admin()
    course_selected=''
    if request.method == 'POST':
        if 'course go' in request.form:
            if(request.form['course_selection']==''):
                course_selected=''
            else:
                course_selected=request.form['course_selection']
    course_list=[]
    if course_selected!='':
        course_list = getAllCourseswithCommonStart(course_selected)
    return render_template('admin_page_2.html', courses=course_list)

def getAllCourseswithCommonStart(start):
    conn = db.start_db()
    cur = conn.cursor()
    print("start : ", start)
    q = """
    SELECT courses.name FROM courses WHERE NAME LIKE %s
    """
    cur.execute(q, (start+'%',))
    return cur.fetchall()

def getAllSubAbbreviation():
    conn = db.start_db()
    cur = conn.cursor()
    cur.execute("SELECT abbreviation from subjects")
    return cur.fetchall()

def searchInstsForSub(sub):
    conn = db.start_db()
    cur = conn.cursor()
    cur.execute("WITH relevant_code as (select code from subjects where abbreviation = %s), relevant_course_off_uuid as (select course_offering_uuid from relevant_code join subject_memberships on relevant_code.code=subject_memberships.subject_code), relevant_sec_id as (select uuid from relevant_course_off_uuid join sections on relevant_course_off_uuid.course_offering_uuid=sections.course_offering_uuid), relevant_inst_id as (select instructor_id, count(instructor_id) from relevant_sec_id join teachings on relevant_sec_id.uuid=teachings.section_uuid group by instructor_id), relevant_instructors as (select name, id from relevant_inst_id join instructors on relevant_inst_id.instructor_id=instructors.id order by name) select * from relevant_instructors", (sub,))
    return cur.fetchall()


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


