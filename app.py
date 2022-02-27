import re
from flask import (Flask, g, flash, redirect,
                   render_template, request, session, url_for)
import db
import random

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'



@app.route('/')
def main():
    return render_template('entry.html')


@app.route('/studenthomepage', methods=['GET', 'POST'])
def studenthomepage():
    load_logged_in_student()
    if request.method == 'POST':
        if 'part 1' in request.form:
            return redirect(url_for('admin_courses', privilegeLevel = 'student'))
        if 'part 2' in request.form:
            return redirect(url_for('admin_instructors', privilegeLevel = 'student'))
        if 'part 3' in request.form:
            return redirect(url_for('admin_subjects', privilegeLevel = 'student'))
        if 'part 5' in request.form:
            return redirect(url_for('schedules_for_students', privilegeLevel = 'student'))
    return render_template('student_page.html')


@app.route('/adminhomepage', methods=['GET', 'POST'])
def adminhomepage():
    load_logged_in_admin()
    if request.method == 'POST':
        if 'part 1' in request.form:
            return redirect(url_for('admin_courses', privilegeLevel = 'admin'))
        if 'part 2' in request.form:
            return redirect(url_for('admin_instructors', privilegeLevel = 'admin'))
        if 'part 3' in request.form:
            return redirect(url_for('admin_subjects', privilegeLevel = 'admin'))
        if 'part 4' in request.form:
            return redirect(url_for('admin_rooms', privilegeLevel = 'admin'))
        if 'part 5' in request.form:
            return redirect(url_for('schedules_for_students', privilegeLevel = 'admin'))
    return render_template('admin_homepage.html')




@app.route('/<privilegeLevel>/courses', methods=['GET', 'POST'])
def admin_courses(privilegeLevel):
    if(privilegeLevel=='admin'):
        load_logged_in_admin()
        if request.method == 'POST':
            if 'search' in request.form:
                return redirect(url_for('adminpage_1', privilegeLevel = 'admin'))
            if 'update' in request.form:
                return redirect(url_for('adminpage_10', privilegeLevel = 'admin'))
            if 'add' in request.form:
                return redirect(url_for('adminpage_10', privilegeLevel = 'admin'))
    else:
        load_logged_in_student()
        if request.method == 'POST':
            if 'search' in request.form:
                return redirect(url_for('adminpage_1', privilegeLevel = 'student'))
    return render_template('admin_courses.html', privilegeLevel=privilegeLevel)

@app.route('/<privilegeLevel>/instructors', methods=['GET', 'POST'])
def admin_instructors(privilegeLevel):
    if(privilegeLevel=='admin'):
        load_logged_in_admin()
        if request.method == 'POST':
            if 'search' in request.form:
                return redirect(url_for('search_instructor', privilegeLevel = 'admin'))
            if 'update' in request.form:
                return redirect(url_for('adminpage_4', privilegeLevel = 'admin'))
            if 'add' in request.form:
                return redirect(url_for('adminpage_7', privilegeLevel = 'admin'))
    else:
        load_logged_in_student()
        if request.method == 'POST':
            if 'search' in request.form:
                return redirect(url_for('search_instructor', privilegeLevel = 'student'))
    return render_template('admin_instructors.html', privilegeLevel = privilegeLevel)

@app.route('/<privilegeLevel>/subjects', methods=['GET', 'POST'])
def admin_subjects(privilegeLevel):
    if(privilegeLevel=='admin'):
        load_logged_in_admin()
        if request.method == 'POST':
            if 'search' in request.form:
                return redirect(url_for('search_subject', privilegeLevel = 'admin'))
            if 'update' in request.form:
                return redirect(url_for('adminpage_5', privilegeLevel = 'admin'))
            if 'add' in request.form:
                return redirect(url_for('adminpage_8', privilegeLevel = 'admin'))
    else:
        load_logged_in_student()
        if request.method == 'POST':
            if 'search' in request.form:
                return redirect(url_for('search_subject', privilegeLevel = 'student'))
    return render_template('admin_subjects.html', privilegeLevel=privilegeLevel)

@app.route('/<privilegeLevel>/rooms', methods=['GET', 'POST'])
def admin_rooms(privilegeLevel):
    if(privilegeLevel=='admin'):
        load_logged_in_admin()
        if request.method == 'POST':
            if 'update' in request.form:
                return redirect(url_for('adminpage_6', privilegeLevel = 'admin'))
            if 'add' in request.form:
                return redirect(url_for('adminpage_9', privilegeLevel = 'admin'))
    else:
        load_logged_in_student()
        if request.method == 'POST':
            if 'search' in request.form:
                return redirect(url_for('adminpage_1', privilegeLevel = 'student'))
    return render_template('admin_rooms.html', privilegeLevel=privilegeLevel)




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
#
#

@app.route('/<privilegeLevel>/adminpage/1', methods=['GET', 'POST'])
def adminpage_1(privilegeLevel):
    if(privilegeLevel=='admin'):
        load_logged_in_admin()
    else:
        load_logged_in_student()
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




@app.route('/adminpage/3', methods=['GET', 'POST'])
def adminpage_3(privilegeLevel):
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


@app.route('/<privilegeLevel>/instructors/updateOrDelete', methods=['GET', 'POST'])
def adminpage_4(privilegeLevel):
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
            return redirect(url_for('adminpage_4_instructor', instructor=inst_selected, privilegeLevel=privilegeLevel))
    inst_list = []
    if insts_selected != '':
        inst_list = getAllInstructorswithCommonStart(insts_selected.lower())
    return render_template('admin_page_4.html', instructors=inst_list)


@app.route('/<privilegeLevel>/instructors/updateOrDelete/<instructor>', methods=['GET', 'POST'])
def adminpage_4_instructor(instructor, privilegeLevel):
    load_logged_in_admin()
    inst_newname = ''
    inst_newcode = ''
    if request.method == 'POST':
        if 'instructor kill' in request.form:
            print("kill", instructor)
            deleteInstructor(instructor)
            return render_template('delete_dump.html', whodel=instructor)
        if 'instructor go' in request.form:
            sub_newname = request.form['instructor_selection']
            sub_newcode = request.form['instructor_selection2']

            if (updateInstructor(sub_newname, sub_newcode,instructor)!=0):
                return render_template('change_done.html')
            else:
                return render_template('notification.html', msg = 'Update Failed : Instructor ID already taken OR it is NOT NUMERIC !')

    return render_template('admin_page_4_instructor.html', instructor=instructor)

    


@app.route('/<privilegeLevel>/adminpage/5', methods=['GET', 'POST'])
def adminpage_5(privilegeLevel):
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
            return redirect(url_for('adminpage_5_subject', subject=sub_selected, privilegeLevel=privilegeLevel))
    sub_list = []
    if subs_selected != '':
        sub_list = getAllSubjectswithCommonStart(subs_selected.lower())
    return render_template('admin_page_5.html', subjects=sub_list)


@app.route('/<privilegeLevel>/adminpage/5/<subject>', methods=['GET', 'POST'])
def adminpage_5_subject(subject, privilegeLevel):
    load_logged_in_admin()
    sub_newname = ''
    sub_newcode = ''
    sub_newabbr = ''
    if request.method == 'POST':
        if 'subject kill' in request.form:
            print("kill", subject)
            deleteSubject(subject)
            return render_template('delete_dump.html', whodel=subject)
        if 'subject go' in request.form:
            sub_newname = request.form['subject_selection']
            sub_newcode = request.form['subject_selection2']
            sub_newabbr = request.form['subject_selection3']

            if (updateSubject(sub_newname, sub_newcode, sub_newabbr,subject)):
                return render_template('change_done.html')
            else:
                return render_template('notification.html', msg = 'Update Failed : Subject ID or Subject Name or Subject Abbreviation already taken !')
                     
    return render_template('admin_page_5_subject.html', subject=subject)



@app.route('/<privilegeLevel>/adminpage/6', methods=['GET', 'POST'])
def adminpage_6(privilegeLevel):
    load_logged_in_admin()
    room_selected = ''
    room_newfacility = ''
    room_newroom = ' '
    if request.method == 'POST':
        if 'room kill' in request.form:
            deleteRoom(room_selected)
            return render_template('delete_dump.html', whodel = "the given room")
        if 'room go' in request.form:
            room_selected = request.form['room_selection']
            room_newfacility = request.form['room_selection2']
            room_newroom = request.form['room_selection3']

            if (updateRoom(room_newroom, room_newfacility, room_selected)):
                return render_template('change_done.html')
            else:
                return render_template('notification.html', msg = 'Update Failed : Room with the same code already exists in the facility !')

    room_list = getAllRooms()
    print(room_selected, room_newfacility, room_newroom)
    return render_template('admin_page_6.html', room_list=room_list, room = room_selected)



@app.route('/<privilegeLevel>/adminpage/7', methods=['GET', 'POST'])
def adminpage_7(privilegeLevel):
    load_logged_in_admin()
    inst_newname = ''
    inst_newcode = ''
    if request.method == 'POST':
        if 'instructor go' in request.form:

            inst_newname = request.form['instructor_selection']

            inst_newcode = request.form['instructor_selection2']

            if(addInstructor(inst_newname, inst_newcode)!=0):
                return render_template('change_done.html')
            else:
                return render_template('notification.html', msg = 'Addition Failed : Instructor ID already taken OR it is NOT numeric  !')
    return render_template('admin_page_7.html')


@app.route('/<privilegeLevel>/adminpage/8', methods=['GET', 'POST'])
def adminpage_8(privilegeLevel):
    load_logged_in_admin()
    sub_newname = ''
    sub_newcode = ''
    sub_newabbr = ''
    if request.method == 'POST':
        if 'subject go' in request.form:

            sub_newcode = request.form['subject_selection']

            sub_newname = request.form['subject_selection2']

            sub_newabbr = request.form['subject_selection3']


            if addSubject(sub_newname, sub_newcode, sub_newabbr):
                return render_template('change_done.html')
            else:
                return render_template('notification.html', msg = 'Addition Failed : Subject ID or Subject Name or Subject Abbreviation already taken !')


    #print(sub_newname, sub_newcode)
    return render_template('admin_page_8.html')


@app.route('/<privilegeLevel>/adminpage/9', methods=['GET', 'POST'])
def adminpage_9(privilegeLevel):
    load_logged_in_admin()
    room_fac = ''
    room_rcode = ''
    if request.method == 'POST':
        if 'room go' in request.form:

            room_fac = request.form['room_selection']

            room_rcode = request.form['room_selection2']
            addRoom(room_fac,room_rcode)
            return render_template('change_done.html')


    #NEED TO CREATE A NEW KEY
    #print(room_newname, room_newcode)
    return render_template('admin_page_9.html')


@app.route('/<privilegeLevel>/adminpage/10', methods=['GET', 'POST'])
def adminpage_10(privilegeLevel):
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
            return redirect(url_for('adminpage_10_course', course=course_selected, privilegeLevel=privilegeLevel))
    course_list = []

    if courses_selected != '':
        course_list = getAllCourseswithCommonStart(courses_selected.lower())
    return render_template('admin_page_10.html', courses=course_list)


@app.route('/<privilegeLevel>/adminpage/10/<course>', methods=['GET', 'POST'])
def adminpage_10_course(course, privilegeLevel):
    load_logged_in_admin()
    course_newname = ''
    if request.method == 'POST':
        if 'course go' in request.form:
            course_newname = request.form['course_selection']
            updateCourse(course,course_newname)
            return render_template('change_done.html')

    return render_template('admin_page_10_course.html', course=course)






@app.route('/<privilegeLevel>/subjects/search', methods=['GET', 'POST'])
def search_subject(privilegeLevel):
    if privilegeLevel=='admin':
        load_logged_in_admin()
    else:
        load_logged_in_student()
    subs_selected = ''
    sub_selected = ''
    if request.method == 'POST':
        if 'subject go' in request.form:
            if(request.form['subject_selection'] == ''):
                subs_selected = ''
            else:
                subs_selected = request.form['subject_selection']
    sub_list = []
    if subs_selected != '':
        sub_list = getAllSubjectswithCommonStart(subs_selected.lower())
    return render_template('search_subject.html', subjects=sub_list)

@app.route('/<privilegeLevel>/instructors/search', methods=['GET', 'POST'])
def search_instructor(privilegeLevel):
    if privilegeLevel=='admin':
        load_logged_in_admin()
    else:
        load_logged_in_student()
    insts_selected = ''
    inst_selected = ''
    if request.method == 'POST':
        if 'instructor go' in request.form:
            if(request.form['instructor_selection'] == ''):
                insts_selected = ''
            else:
                insts_selected = request.form['instructor_selection']
    inst_list = []
    if insts_selected != '':
        inst_list = getAllInstructorswithCommonStart(insts_selected.lower())
    print("here")
    return render_template('search_instructor.html', instructors=inst_list)


def deleteInstructor(instructor):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        DELETE FROM instructors WHERE name||' - '||id=%s;
        """
    cur.execute(q, (instructor,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    return ra


def updateInstructor(name, newCode, instructor):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        UPDATE instructors SET id=%s, name=%s WHERE name||' - '||id=%s;
        """
    cur.execute(q, (newCode, name, instructor,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    return ra

def addInstructor(name, code):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        INSERT INTO instructors(id,name) VALUES (%s,%s);
        """
    cur.execute(q, (name,code,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    print(ra)
    return ra

#SUBJECT

def updateSubject(newname, newcode, newabbr,subject):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        UPDATE subjects SET name=%s, code=%s , abbreviation=%s WHERE name=%s;
        """
    cur.execute(q, (newname, newcode, newabbr,subject,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    return ra

def addSubject(name, code, abbr):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        INSERT INTO subjects(code,name, abbreviation) VALUES (%s,%s,%s);
        """
    cur.execute(q, (name,code,abbr,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    print(ra)
    return ra

def deleteSubject(subject):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        DELETE FROM subjects WHERE name=%s;
        """
    cur.execute(q, (subject,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    return ra


# ROOM

def updateRoom(newroom, newfac, old):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        UPDATE rooms SET room_code=%s, facility_code=%s WHERE facility_code||' - '||room_code=%s;
        """
    cur.execute(q, (newroom, newfac, old,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    return ra
    
def addRoom(fac, room):
    conn = db.start_db()
    cur = conn.cursor()
    key = randomKeyGenerator()
    q = """
        INSERT INTO rooms(uuid,facility_code, room_code) VALUES (%s,%s,%s);
        """
    cur.execute(q, (key,fac,room,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    print(ra)
    return ra

def deleteRoom(room):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        DELETE FROM rooms WHERE facility_code||' - '||room_code=%s;
        """
    cur.execute(q, (room,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    return ra


#COURSEEEEEE  
def updateCourse(old,new):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        UPDATE courses SET name=%s WHERE name=%s;
        """
    cur.execute(q, (new,old,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    return ra



def deleteRoom(name):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
        DELETE FROM courses WHERE name=%s;
        """
    cur.execute(q, (name,))
    conn.commit()
    ra = cur.rowcount
    cur.close()
    return ra

@app.route('/<privilegeLevel>/schedules', methods=['GET', 'POST'])
def schedules_for_students(privilegeLevel):
    if privilegeLevel=='admin':
        load_logged_in_admin()
    else:
        load_logged_in_student()
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
            return redirect(url_for('schedules_course', course=course_selected, privilegeLevel=privilegeLevel))
    course_list = []
    if courses_selected != '':
        course_list = getAllCourseswithCommonStart(courses_selected)
    return render_template('admin_page_2.html', courses=course_list)


@app.route('/<privilegeLevel>/schedules/<course>', methods=['GET', 'POST'])
def schedules_course(course, privilegeLevel):
    if privilegeLevel=='admin':
        load_logged_in_admin()
    else:
        load_logged_in_student()
    course_off_term_selected = ''
    course_off_list = getAllCourseOff(course)
    instForCourseOffTerm = []
    allInfo = ''
    showInst = "No"
    showAllInfo="No"
    showOld = "Yes"
    if request.method == 'POST':
        if 'course offering go' in request.form:
            if(request.form['course_off_selection'] == 'select'):
                course_off_term_selected = ''
            else:
                course_off_term_selected = request.form['course_off_selection']
                instForCourseOffTerm = getInstForCourseOffTerm(course_off_term_selected)
                showInst="Yes"
            print("course off : ", course_off_term_selected)
            return render_template('admin_page_2_course.html',showOld="No", course=course, course_off_list=course_off_list, course_off_term_selected=course_off_term_selected, instForCourseOffTerm=instForCourseOffTerm, showInst=showInst, allInfo=allInfo, showAllInfo=showAllInfo)

        if 'inst go' in request.form:
            courseOffTerm = request.form['course_off_term']
            inst_sec_number = request.form['inst_select']
            allInfo = getAllInfo(courseOffTerm, inst_sec_number)
            showInst="No"
            showAllInfo="Yes"
            showOld = "No"
            print("debug : ", request.form['course_off_term'], request.form['inst_select'])
            #return render_template('admin_page_2_course.html',showOld=showOld, course=course, course_off_list=course_off_list, course_off_term_selected=course_off_term_selected, instForCourseOffTerm=instForCourseOffTerm, showInst=showInst, allInfo=allInfo, showAllInfo=showAllInfo)

    return render_template('admin_page_2_course.html',showOld=showOld, course=course, course_off_list=course_off_list, course_off_term_selected=course_off_term_selected, instForCourseOffTerm=instForCourseOffTerm, showInst=showInst, allInfo=allInfo, showAllInfo=showAllInfo)





















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
def randomKeyGenerator():
    a = []
    for i in range(32):
        a.append(str(random.randint(0,9)))
    return "".join(a[:8]) + "-" + "".join(a[8:12]) + "-" + "".join(a[12:20]) + "-" + "".join(a[20:])


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
    SELECT instructors.name ||' - '|| instructors.id, instructors.id FROM instructors WHERE LOWER(name) LIKE %s
    """
    cur.execute(q, ('%'+start+'%',))
    return cur.fetchall()


def getAllSubjectswithCommonStart(start):
    conn = db.start_db()
    cur = conn.cursor()
    print("start : ", start)
    q = """
    SELECT subjects.name, subjects.code FROM subjects WHERE LOWER(name) LIKE %s
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

def getInstForCourseOffTerm(offTerm):
    conn = db.start_db()
    cur = conn.cursor()
    q = """
    WITH a as (select CONCAT(name,' - ',term_code) as course_off_name_term, sections.uuid as sec_uuid, number as sec_number from course_offerings join sections on course_offerings.uuid=sections.course_offering_uuid and CONCAT(name,' - ',term_code)=%s and room_uuid!='null')
    , aa as (select course_off_name_term, sec_number, instructor_id from a join teachings on section_uuid=sec_uuid)
    , relevant_instructors as (select course_off_name_term, CONCAT(instructors.name, ' - ', sec_number) as instructor_name_sec  from aa join instructors on instructors.id=instructor_id)
    select * from relevant_instructors order by instructor_name_sec;
    """
    cur.execute(q, (offTerm,))
    return cur.fetchall()

def getAllInfo(courseOffTerm, inst_sec_number):
    conn = db.start_db()
    cur = conn.cursor()
    q="""
    WITH a as (select number as sec_number, course_offerings.uuid, CONCAT(name,' - ',term_code) as course_offering_name, sections.uuid as sec_uuid, section_type, room_uuid, schedule_uuid from course_offerings join sections on course_offerings.uuid=sections.course_offering_uuid and CONCAT(name,' - ',term_code)=%s and room_uuid!='null')
    , aa as (select sec_number, uuid, course_offering_name, instructor_id, section_type, room_uuid, schedule_uuid from a join teachings on section_uuid=sec_uuid)
    , aaa as (select sec_number, uuid, course_offering_name, CONCAT(instructors.name, ' - ', sec_number) as instructor_name, section_type, room_uuid, schedule_uuid from aa join instructors on instructors.id=instructor_id and CONCAT(instructors.name, ' - ', sec_number)=%s)
    , aaaa as (select sec_number, aaa.uuid, course_offering_name, instructor_name, section_type, facility_code, room_code, schedule_uuid from aaa join rooms on rooms.uuid=room_uuid)
    , aaaaa as (select sec_number, aaaa.uuid, course_offering_name, instructor_name, section_type, facility_code, room_code, start_time, end_time, mon, tues, wed, thurs, fri, sat, sun from aaaa join schedules on schedules.uuid=schedule_uuid)
    , final_course_off_sections_instructors_schedule_grades_info as (select sec_number, uuid, course_offering_name, instructor_name, section_type, facility_code, room_code, start_time, end_time, mon, tues, wed, thurs, fri, sat, sun, a_count, ab_count, b_count, bc_count, c_count, d_count, f_count, s_count, u_count, cr_count, n_count, p_count, i_count, nw_count, nr_count, other_count from aaaaa join grade_distributions on section_number=sec_number and course_offering_uuid=uuid)
    select * from final_course_off_sections_instructors_schedule_grades_info;
    """
    cur.execute(q, (courseOffTerm, inst_sec_number,))
    return cur.fetchone()

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
            return redirect(url_for('studenthomepage'))
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
        g.privilegeLevel = 'admin'


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
        g.privilegeLevel = 'student'


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('adminlogin'))