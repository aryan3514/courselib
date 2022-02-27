CREATE TABLE IF NOT EXISTS courses
(
	uuid text not NULL,
	name text,
	number int,
	CONSTRAINT courses_key primary key (uuid)
	-- CONSTRAINT courses_primary_key primary key (uuid)
);

-- ALTER table courses drop CONSTRAINT courses_key;
-- ALTER table courses add CONSTRAINT courses_primary_key primary key (uuid);




create table IF NOT EXISTS course_offerings(
	uuid text not NULL,
	course_uuid text not NULL,
	term_code int,
	name text,
	CONSTRAINT course_offerings_key PRIMARY KEY (uuid),
	-- CONSTRAINT course_off_primary_key PRIMARY KEY (uuid),
	CONSTRAINT course_uuid_ref FOREIGN KEY (course_uuid) references courses(uuid)
	-- CONSTRAINT course_uuid_foreign_key FOREIGN KEY (course_uuid) references courses(uuid) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ALTER table course_offerings drop CONSTRAINT course_offerings_key;
-- ALTER table course_offerings add CONSTRAINT course_off_primary_key PRIMARY KEY (uuid);

-- ALTER table course_offerings drop CONSTRAINT course_uuid_ref;
-- ALTER table course_offerings add CONSTRAINT course_uuid_foreign_key FOREIGN KEY (course_uuid) references courses(uuid) ON DELETE CASCADE ON UPDATE CASCADE;




CREATE TABLE IF NOT EXISTS schedules(
	uuid text not NULL,
	start_time int not NULL,
	end_time int not NULL,
	mon boolean not NULL,
	tues boolean not NULL,
	wed boolean not NULL,
	thurs boolean not NULL,
	fri boolean not NULL,
	sat boolean not NULL,
	sun boolean not NULL,
	CONSTRAINT schedules_key PRIMARY KEY (uuid)
	-- CONSTRAINT schedules_primary_key PRIMARY KEY (uuid)
);

-- ALTER table schedules drop CONSTRAINT schedules_key;
-- ALTER table schedules add CONSTRAINT schedules_primary_key PRIMARY KEY (uuid);




create table IF NOT EXISTS sections(
	uuid text not NULL,
	course_offering_uuid text not NULL,
	section_type text,
	number int,
	room_uuid text,
	schedule_uuid text,
	CONSTRAINT sections_key PRIMARY KEY (uuid),
	-- CONSTRAINT sections_primary_key PRIMARY KEY (uuid),
	CONSTRAINT course_offering_uuid_ref FOREIGN KEY (course_offering_uuid) references course_offerings(uuid),
	-- CONSTRAINT course_offering_uuid_foreign_key FOREIGN KEY (course_offering_uuid) references course_offerings(uuid) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT schedule_uuid_ref FOREIGN KEY (schedule_uuid) references schedules(uuid)
	-- CONSTRAINT schedule_uuid_foreign_key FOREIGN KEY (schedule_uuid) references schedules(uuid)
	);

-- ALTER table sections drop CONSTRAINT sections_key;
-- ALTER table sections add CONSTRAINT sections_primary_key PRIMARY KEY (uuid);

-- ALTER table sections drop CONSTRAINT course_offering_uuid_ref;
-- ALTER table sections add CONSTRAINT course_offering_uuid_foreign_key FOREIGN KEY (course_offering_uuid) references course_offerings(uuid) ON DELETE CASCADE ON UPDATE CASCADE;

-- ALTER table sections drop CONSTRAINT schedule_uuid_ref;
-- ALTER table sections add CONSTRAINT schedule_uuid_foreign_key FOREIGN KEY (schedule_uuid) references schedules(uuid);




CREATE TABLE IF NOT EXISTS subjects(
	code text not NULL,
	name text not NULL,
	abbreviation text not NULL,
	CONSTRAINT subjects_key PRIMARY KEY (code)
	-- CONSTRAINT subjects_primary_key PRIMARY KEY (code)
	);

-- ALTER table subjects drop CONSTRAINT subjects_key;
-- ALTER table subjects add CONSTRAINT subjects_primary_key PRIMARY KEY (code);




CREATE TABLE IF NOT EXISTS grade_distributions(
	course_offering_uuid text not NULL,
	section_number int not NULL,
	a_count int,
	ab_count int,
	b_count int,
	bc_count int,
	c_count int,
	d_count int,
	f_count int,
	s_count int,
	u_count int,
	cr_count int,
	n_count int,
	p_count int,
	i_count int,
	nw_count int,
	nr_count int,
	other_count int,

	CONSTRAINT grade_distributions_key PRIMARY KEY (course_offering_uuid, section_number),
	-- CONSTRAINT grade_distributions_primary_key PRIMARY KEY (course_offering_uuid, section_number),
	CONSTRAINT course_offering_uuid_ref FOREIGN KEY (course_offering_uuid) references course_offerings(uuid)
	-- CONSTRAINT course_offering_uuid_foreign_key FOREIGN KEY (course_offering_uuid) references course_offerings(uuid) ON DELETE CASCADE ON UPDATE CASCADE
	);

-- ALTER table grade_distributions drop CONSTRAINT grade_distributions_key;
-- ALTER table grade_distributions add CONSTRAINT grade_distributions_primary_key PRIMARY KEY (course_offering_uuid, section_number);

-- ALTER table grade_distributions drop CONSTRAINT course_offering_uuid_ref;
-- ALTER table grade_distributions add CONSTRAINT course_offering_uuid_foreign_key FOREIGN KEY (course_offering_uuid) references course_offerings(uuid) ON DELETE CASCADE ON UPDATE CASCADE;





CREATE TABLE IF NOT EXISTS rooms(
	uuid text not NULL,
	facility_code text,
	room_code text,
	CONSTRAINT rooms_key PRIMARY KEY (uuid)
	-- 	CONSTRAINT rooms_primary_key PRIMARY KEY (uuid)
	);

-- ALTER table rooms drop CONSTRAINT rooms_key;
-- ALTER table rooms add CONSTRAINT rooms_primary_key PRIMARY KEY (uuid);




CREATE TABLE IF NOT EXISTS instructors(
	id text not NULL,
	name text,
	CONSTRAINT instructors_key PRIMARY KEY (id)
	-- 	CONSTRAINT instructors_primary_key PRIMARY KEY (id)
);

-- ALTER table instructors drop CONSTRAINT instructors_key;
-- ALTER table instructors add CONSTRAINT instructors_primary_key PRIMARY KEY (id);




-- ok
CREATE TABLE IF NOT EXISTS subject_memberships(
	subject_code text not NULL,
	course_offering_uuid text not NULL,

    CONSTRAINT subject_memberships_key PRIMARY KEY (subject_code,course_offering_uuid),
    -- CONSTRAINT subject_memberships_primary_key PRIMARY KEY (subject_code,course_offering_uuid),
	CONSTRAINT subject_code_ref FOREIGN KEY (subject_code) references subjects(code),
	-- CONSTRAINT subject_code_foreign_key FOREIGN KEY (subject_code) references subjects(code) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT course_offering_uuid_ref FOREIGN KEY (course_offering_uuid) references course_offerings(uuid)
	-- CONSTRAINT course_offering_uuid_foreign_key FOREIGN KEY (course_offering_uuid) references course_offerings(uuid) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ALTER table subject_memberships drop CONSTRAINT subject_memberships_key;
-- ALTER table subject_memberships add CONSTRAINT subject_memberships_primary_key PRIMARY KEY (subject_code,course_offering_uuid);

-- ALTER table subject_memberships drop CONSTRAINT subject_code_ref;
-- ALTER table subject_memberships add CONSTRAINT subject_code_foreign_key FOREIGN KEY (subject_code) references subjects(code) ON DELETE CASCADE ON UPDATE CASCADE;

-- ALTER table subject_memberships drop CONSTRAINT course_offering_uuid_ref;
-- ALTER table subject_memberships add CONSTRAINT course_offering_uuid_foreign_key FOREIGN KEY (course_offering_uuid) references course_offerings(uuid) ON DELETE CASCADE ON UPDATE CASCADE;




-- ok
CREATE TABLE IF NOT EXISTS teachings(
	instructor_id text not null,
	section_uuid text not null,

	CONSTRAINT teachings_key PRIMARY KEY (instructor_id,section_uuid),
	-- CONSTRAINT teachings_primary_key PRIMARY KEY (instructor_id,section_uuid),
	CONSTRAINT instructor_id_ref FOREIGN KEY (instructor_id) references instructors(id) ON UPDATE CASCADE ON DELETE CASCADE,
	-- CONSTRAINT instructor_id_foreign_key FOREIGN KEY (instructor_id) references instructors(id) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT section_uuid_ref FOREIGN KEY (section_uuid) references sections(uuid)
	-- 	CONSTRAINT section_uuid_foreign_key FOREIGN KEY (section_uuid) references sections(uuid) ON UPDATE CASCADE ON DELETE CASCADE
);



-- ALTER table teachings drop constraint teachings_key;
-- ALTER table teachings add CONSTRAINT teachings_primary_key PRIMARY KEY (instructor_id,section_uuid);

--ALTER table teachings drop constraint instructor_id_ref;
--ALTER table teachings add CONSTRAINT instructor_id_foreign_key FOREIGN KEY (instructor_id) references instructors(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- ALTER table teachings drop constraint section_uuid_ref;
-- ALTER table teachings add CONSTRAINT section_uuid_foreign_key FOREIGN KEY (section_uuid) references sections(uuid) ON UPDATE CASCADE ON DELETE CASCADE;




CREATE TABLE IF NOT EXISTS login_for_student(
	id text not null,
	password text not null,
	CONSTRAINT login_for_student_primary_key PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS student_watchlist(
	student_id text not null,
	course_offering_name_term_code text not null,
	section_type text,
	instructor_name_sec_number text,
	CONSTRAINT student_watchlist_primary_key PRIMARY KEY (student_id,course_offering_name_term_code),
	CONSTRAINT sstudent_id_foreign_key FOREIGN KEY (student_id) references login_for_student(id)
);

CREATE TABLE IF NOT EXISTS login_for_admin(
	id text not null,
	password text not null,
	CONSTRAINT login_for_admin_primary_key PRIMARY KEY (id)
);






/*
\COPY courses FROM 'courses.csv' DELIMITER ',' CSV HEADER;
\COPY course_offerings FROM 'course_offerings.csv' DELIMITER ',' CSV HEADER;
\COPY schedules FROM 'schedules.csv' DELIMITER ',' CSV HEADER;
\COPY sections FROM 'sections.csv' DELIMITER ',' CSV HEADER;
\COPY subjects FROM 'subjects.csv' DELIMITER ',' CSV HEADER;
\COPY grade_distributions FROM 'grade_distributions.csv' DELIMITER ',' CSV HEADER;
\COPY rooms FROM 'rooms.csv' DELIMITER ',' CSV HEADER;
\COPY instructors FROM 'instructors.csv' DELIMITER ',' CSV HEADER;
\COPY subject_memberships FROM 'subject_memberships.csv' DELIMITER ',' CSV HEADER;
\COPY teachings FROM 'teachings.csv' DELIMITER ',' CSV HEADER;

*/





