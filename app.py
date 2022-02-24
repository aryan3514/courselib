import re
from flask import (Flask, g, flash, redirect,
                   render_template, request, session, url_for)
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

@app.route('/adminhomepage', methods=['GET', 'POST'])
def adminhomepage():
    load_logged_in_admin()
    if request.method == 'POST':
        if 'part 1' in request.form:
            return redirect(url_for('admin_courses'))
        if 'part 2' in request.form:
            return redirect(url_for('admin_instructors'))
        if 'part 3' in request.form:
            return redirect(url_for('admin_subjects'))
        if 'part 4' in request.form:
            return redirect(url_for('admin_rooms'))
    return render_template('admin_homepage.html')


@app.route('/admin_courses', methods=['GET', 'POST'])
def admin_courses():
    load_logged_in_admin()
    if request.method == 'POST':
        if 'search' in request.form:
            return redirect(url_for('adminpage_1'))
        if 'update' in request.form:
            return redirect(url_for('adminpage_10'))
        if 'add' in request.form:
            return redirect(url_for('adminpage_10'))
    return render_template('admin_courses.html')

@app.route('/admin_instructors', methods=['GET', 'POST'])
def admin_instructors():
    load_logged_in_admin()
    if request.method == 'POST':
        if 'search' in request.form:
            return redirect(url_for('adminpage_1'))
        if 'update' in request.form:
            return redirect(url_for('adminpage_4'))
        if 'add' in request.form:
            return redirect(url_for('adminpage_7'))
    return render_template('admin_instructors.html')

@app.route('/admin_subjects', methods=['GET', 'POST'])
def admin_subjects():
    load_logged_in_admin()
    if request.method == 'POST':
        if 'search' in request.form:
            return redirect(url_for('adminpage_1'))
        if 'update' in request.form:
            return redirect(url_for('adminpage_5'))
        if 'add' in request.form:
            return redirect(url_for('adminpage_8'))
    return render_template('admin_subjects.html')

@app.route('/admin_rooms', methods=['GET', 'POST'])
def admin_rooms():
    load_logged_in_admin()
    if request.method == 'POST':
        if 'search' in request.form:
            return redirect(url_for('adminpage_1'))
        if 'update' in request.form:
            return redirect(url_for('adminpage_6'))
        if 'add' in request.form:
            return redirect(url_for('adminpage_9'))
    return render_template('admin_rooms.html')


@app.route('/adminpage', methods=['GET', 'POST'])
def adminpage():
    load_logged_in_admin()
    if request.method == 'POST':
        if 'part 1' in request.form:
            return redirect(url_for('adminpage_1'))
        if 'part 2' in request.form:
            return redirect(url_for('adminpage_2'))
        if 'part 3' in request.form:
            return redirect(url_for('adminpage_3'))
        if 'part 4' in request.form:
            return redirect(url_for('adminpage_4'))
        if 'part 5' in request.form:
            return redirect(url_for('adminpage_5'))
        if 'part 6' in request.form:
            return redirect(url_for('adminpage_6'))
        if 'part 7' in request.form:
            return redirect(url_for('adminpage_7'))
        if 'part 8' in request.form:
            return redirect(url_for('adminpage_8'))
        if 'part 9' in request.form:
            return redirect(url_for('adminpage_9'))
        if 'part 10' in request.form:
            return redirect(url_for('adminpage_10'))
    return render_template('admin_page.html')


@app.route('/adminpage/1', methods=['GET', 'POST'])
def adminpage_1():
    load_logged_in_admin()
    whatToDo = ''
    subject_selected = ''
    inst_selected = ''

    if request.method == 'POST':

        if 'subject go' in request.form:

            if(request.form['subject_selection'] == '' and request.form['subject_selection2'] == 'select'):
                whatToDo = 'nothing'
            elif(request.form['subject_selection'] == ''):
                subject_selected = request.form['subject_selection2']
                whatToDo = 'get instructors'
            else:
                subject_selected = request.form['subject_selection']
                whatToDo = 'get instructors'
            print("subject : ", subject_selected)

        if 'instructor go' in request.form:
            if(request.form['instructor_selection'] == '' and request.form['instructor_selection2'] == 'select'):
                whatToDo = 'nothing'
            elif(request.form['instructor_selection'] == ''):
                inst_selected = request.form['instructor_selection2']
                whatToDo = 'get instructors'
            else:
                inst_selected = request.form['instructor_selection']
                whatToDo = 'get instructors'
            print("instructor : ", inst_selected)
    inst_list = searchInstsForSub(subject_selected)
    abb_list = getAllSubAbbreviation()
    return render_template('admin_page_1.html', subject_abb_list=abb_list, instructor_list=inst_list, sub=subject_selected, inst=inst_selected)


@app.route('/adminpage/2', methods=['GET', 'POST'])
def adminpage_2():
    load_logged_in_admin()
    courses_selected = ''
    course_selected = ''
    if request.method == 'POST':
        if 'course go' in request.form:
            if(request.form['course_selection'] == ''):
                courses_selected = ''
            else:
                courses_selected = request.form['course_selection']
        else:
            course_selected = request.form['select a course']
            print('course : ', course_selected)
            return redirect(url_for('adminpage_2_course', course=course_selected))
    course_list = []
    if courses_selected != '':
        course_list = getAllCourseswithCommonStart(courses_selected)
    return render_template('admin_page_2.html', courses=course_list)


@app.route('/adminpage/2/<course>', methods=['GET', 'POST'])
def adminpage_2_course(course):
    load_logged_in_admin()
    course_off_selected = ''
    course_off_list = getAllCourseOff(course)
    if request.method == 'POST':
        if 'course offering go' in request.form:
            if(request.form['course_off_selection'] == 'select'):
                course_off_selected = ''
            else:
                course_off_selected = request.form['course_off_selection']
            print("course off : ", course_off_selected)
    return render_template('admin_page_2_course.html', course=course, course_off_list=course_off_list, course_off_selected=course_off_selected)


@app.route('/adminpage/3', methods=['GET', 'POST'])
def adminpage_3():
    load_logged_in_admin()
    instructor_selected = ''
    if request.method == 'POST':
        if 'instructor go' in request.form:
            if(request.form['instructor_selection'] == ''):
                instructor_selected = ''
            else:
                instructor_selected = request.form['instructor_selection']
    instructor_list = []
    if instructor_selected != '':
        instructor_list = getAllInstructorswithCommonStart(
            instructor_selected.lower())
    return render_template('admin_page_3.html', instructors=instructor_list)


@app.route('/adminpage/4', methods=['GET', 'POST'])
def adminpage_4():
    load_logged_in_admin()
    insts_selected = ''
    inst_selected = ''
    if request.method == 'POST':
        if 'instructor go' in request.form:
            if(request.form['instructor_selection'] == ''):
                insts_selected = ''
            else:
                insts_selected = request.form['instructor_selection']
        else:
            inst_selected = request.form['select a instructor']
            print('Instructor : ', inst_selected)
            return redirect(url_for('adminpage_4_instructor', instructor=inst_selected))
    inst_list = []
    if insts_selected != '':
        inst_list = getAllInstructorswithCommonStart(insts_selected.lower())
    return render_template('admin_page_4.html', instructors=inst_list)


@app.route('/adminpage/4/<instructor>', methods=['GET', 'POST'])
def adminpage_4_instructor(instructor):
    load_logged_in_admin()
    inst_newname = ''
    inst_newcode = ''
    if request.method == 'POST':
        if 'instructor kill' in request.form:
            print("kill", instructor)
            return render_template('delete_dump.html', whodel=instructor)
        if 'instructor go' in request.form:
            sub_newname = request.form['instructor_selection']

            sub_newcode = request.form['instructor_selection2']
            return render_template('change_done.html')
    return render_template('admin_page_4_instructor.html', instructor=instructor)



@app.route('/adminpage/5', methods=['GET', 'POST'])
def adminpage_5():
    load_logged_in_admin()
    subs_selected = ''
    sub_selected = ''
    if request.method == 'POST':
        if 'subject go' in request.form:
            if(request.form['subject_selection'] == ''):
                subs_selected = ''
            else:
                subs_selected = request.form['subject_selection']
        else:
            sub_selected = request.form['select a subject']
            print('subject : ', sub_selected)
            return redirect(url_for('adminpage_5_subject', subject=sub_selected))
    sub_list = []
    if subs_selected != '':
        sub_list = getAllSubjectswithCommonStart(subs_selected.lower())
    return render_template('admin_page_5.html', subjects=sub_list)


@app.route('/adminpage/5/<subject>', methods=['GET', 'POST'])
def adminpage_5_subject(subject):
    load_logged_in_admin()
    sub_newname = ''
    sub_newcode = ''
    sub_newabbr = ''
    if request.method == 'POST':
        if 'subject kill' in request.form:
            print("kill", subject)
            return render_template('delete_dump.html', whodel=subject)
        if 'subject go' in request.form:
            sub_newname = request.form['subject_selection']
            sub_newcode = request.form['subject_selection2']
            sub_newabbr = request.form['subject_selection3']
            return render_template('change_done.html')

            
    return render_template('admin_page_5_subject.html', subject=subject)



@app.route('/adminpage/6', methods=['GET', 'POST'])
def adminpage_6():
    load_logged_in_admin()
    room_selected = ''
    room_newfacility = ''
    room_newroom = ' '
    if request.method == 'POST':
        if 'room kill' in request.form:
            return render_template('delete_dump.html', whodel = "the given room")
        if 'room go' in request.form:
            room_selected = request.form['room_selection']
            room_newfacility = request.form['room_selection2']
            room_newroom = request.form['room_selection3']
            return render_template('change_done.html')
    room_list = getAllRooms()
    print(room_selected, room_newfacility, room_newroom)
    return render_template('admin_page_6.html', room_list=room_list, room = room_selected)



@app.route('/adminpage/7', methods=['GET', 'POST'])
def adminpage_7():
    load_logged_in_admin()
    inst_newname = ''
    inst_newcode = ''
    if request.method == 'POST':
        if 'instructor go' in request.form:

            inst_newname = request.form['instructor_selection']

            inst_newcode = request.form['instructor_selection2']
    print(inst_newname, inst_newcode)
    return render_template('admin_page_7.html')


@app.route('/adminpage/8', methods=['GET', 'POST'])
def adminpage_8():
    load_logged_in_admin()
    sub_newname = ''
    sub_newcode = ''
    if request.method == 'POST':
        if 'subject go' in request.form:

            sub_newname = request.form['subject_selection']

            sub_newcode = request.form['subject_selection2']
    print(sub_newname, sub_newcode)
    return render_template('admin_page_8.html')


@app.route('/adminpage/9', methods=['GET', 'POST'])
def adminpage_9():
    load_logged_in_admin()
    room_newname = ''
    room_newcode = ''
    if request.method == 'POST':
        if 'room go' in request.form:

            room_newname = request.form['room_selection']

            room_newcode = request.form['room_selection2']

    #NEED TO CREATE A NEW KEY
    print(room_newname, room_newcode)
    return render_template('admin_page_9.html')


@app.route('/adminpage/10', methods=['GET', 'POST'])
def adminpage_10():
    load_logged_in_admin()
    courses_selected = ''
    course_selected = ''
    if request.method == 'POST':
        if 'course go' in request.form:
            if(request.form['course_selection'] == ''):
                courses_selected = ''
            else:
                courses_selected = request.form['course_selection']
        else:
            course_selected = request.form['select a course']
            return redirect(url_for('adminpage_10_course', course=course_selected))
    course_list = []

    if courses_selected != '':
        course_list = getAllCourseswithCommonStart(courses_selected.lower())
    return render_template('admin_page_10.html', courses=course_list)


@app.route('/adminpage/10/<course>', methods=['GET', 'POST'])
def adminpage_10_course(course):
    load_logged_in_admin()
    course_newname = ''
    if request.method == 'POST':
        if 'course go' in request.form:
            course_newname = request.form['course_selection']
            
    return render_template('admin_page_10_course.html', course=course)

# HELPER FUNCTIONS
#
#
#
#
#
#
#
#
#
#
#
#


def getAllRooms():
    conn = db.start_db()
    cur = conn.cursor()
    q = """
    SELECT facility_code || ' - ' || room_code AS new FROM rooms
    """
    cur.execute(q)
    return cur.fetchall()


def getAllCourseOff(course_name):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
    WITH relevant_course_uuid as (select uuid from courses where name=%s)
    , relevant_course_off_name as (select name, term_code from relevant_course_uuid join course_offerings on course_offerings.course_uuid=relevant_course_uuid.uuid)
    select * from relevant_course_off_name;
    """
    cur.execute(q, (course_name,))
    return cur.fetchall()


def getAllCourseswithCommonStart(start):
    conn = db.start_db()
    cur = conn.cursor()
    print("start : ", start)
    q = """
    SELECT DISTINCT courses.name FROM courses WHERE LOWER(name) LIKE %s
    """
    cur.execute(q, ('%' + start+'%',))
    return cur.fetchall()


def getAllSubAbbreviation():
    conn = db.start_db()
    cur = conn.cursor()
    cur.execute("SELECT abbreviation from subjects")
    return cur.fetchall()


def getAllInstructorswithCommonStart(start):
    conn = db.start_db()
    cur = conn.cursor()
    print("start : ", start)
    q = """
    SELECT instructors.name FROM instructors WHERE LOWER(name) LIKE %s
    """
    cur.execute(q, ('%'+start+'%',))
    return cur.fetchall()


def getAllSubjectswithCommonStart(start):
    conn = db.start_db()
    cur = conn.cursor()
    print("start : ", start)
    q = """
    SELECT subjects.name FROM subjects WHERE LOWER(name) LIKE %s
    """
    cur.execute(q, ('%'+start+'%',))
    return cur.fetchall()


def searchInstsForSub(sub):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
    WITH relevant_code as (select code from subjects where abbreviation = %s),
    relevant_course_off_uuid as (select course_offering_uuid from relevant_code join subject_memberships on relevant_code.code=subject_memberships.subject_code), 
    relevant_sec_id as (select uuid from relevant_course_off_uuid join sections on relevant_course_off_uuid.course_offering_uuid=sections.course_offering_uuid), 
    relevant_inst_id as (select instructor_id, count(instructor_id) from relevant_sec_id join teachings on relevant_sec_id.uuid=teachings.section_uuid group by instructor_id), 
    relevant_instructors as (select name, id from relevant_inst_id join instructors on relevant_inst_id.instructor_id=instructors.id order by name) 
    select * from relevant_instructors
    """
    cur.execute(q, (sub,))
    return cur.fetchall()


def changeInstructorName(inst_selected, inst_newname):
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
        cur.execute(
            "SELECT password FROM admin_info where username = %s", (username,))
        user = cur.fetchone()
        print(user)
        if user is None:
            error = 'Incorrect username.'
        elif (user[0] != password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = username
            return redirect(url_for('adminhomepage'))
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
        cur.execute(
            "SELECT password FROM student_login_info where username = %s", (username,))
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
        cur.execute(
            'SELECT username FROM admin_info WHERE username = %s', (username,))
        g.user = cur.fetchone()


def load_logged_in_student():
    username = session.get('user_id')
    if username is None:
        g.user = None
    else:
        conn = db.start_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT username FROM student_login_info WHERE username = %s', (username,))
        g.user = cur.fetchone()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('adminlogin'))
