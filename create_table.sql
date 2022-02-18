CREATE TABLE IF NOT EXISTS courses
(
	uuid text not NULL,
	name text,
	number int,
	CONSTRAINT courses_key primary key (uuid)
);

create table IF NOT EXISTS course_offerings(
	uuid text not NULL,
	course_uuid text not NULL,
	term_code int,
	name text,
	CONSTRAINT course_offerings_key PRIMARY KEY (uuid),
	CONSTRAINT course_uuid_ref FOREIGN KEY (course_uuid) references courses(uuid),
);

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
);

create table IF NOT EXISTS sections(
	uuid text not NULL,
	course_offering_uuid text not NULL,
	section_type text,
	number int,
	room_uuid text,
	schedule_uuid text,
	--reg_limit int,
	CONSTRAINT sections_key PRIMARY KEY (uuid),
	CONSTRAINT course_offering_uuid_ref FOREIGN KEY (course_offering_uuid) references course_offerings(uuid),
	CONSTRAINT schedule_uuid_ref FOREIGN KEY (schedule_uuid) references schedules(uuid)
	);

CREATE TABLE IF NOT EXISTS subjects(
	code text not NULL,
	name text not NULL,
	abbreviation text not NULL,
	CONSTRAINT subjects_key PRIMARY KEY (code)
	);

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
	CONSTRAINT course_offering_uuid_ref FOREIGN KEY (course_offering_uuid) references course_offerings(uuid)
	);

CREATE TABLE IF NOT EXISTS rooms(
	uuid text not NULL,
	facility_code text,
	room_code text,
	CONSTRAINT rooms_key PRIMARY KEY (uuid)
	);

CREATE TABLE IF NOT EXISTS instructors(
	id bigint not NULL,
	name text,
	CONSTRAINT instructors_key PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS subject_memberships(
	subject_code text not NULL,
	course_offering_uuid text not NULL,

    CONSTRAINT subject_memberships_key PRIMARY KEY (subject_code,course_offering_uuid),
	CONSTRAINT subject_code_ref FOREIGN KEY (subject_code) references subjects(code),
	CONSTRAINT course_offering_uuid_ref FOREIGN KEY (course_offering_uuid) references course_offerings(uuid)
);

CREATE TABLE teachings(
	instructor_id bigint not null,
	section_uuid text not null,

	CONSTRAINT teachings_key PRIMARY KEY (instructor_id,section_uuid),
	CONSTRAINT instructor_id_ref FOREIGN KEY (instructor_id) references instructors(id),
	CONSTRAINT section_uuid_ref FOREIGN KEY (section_uuid) references sections(uuid)
	);


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
