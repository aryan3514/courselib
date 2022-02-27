-- drop 
ALTER table teachings drop constraint section_uuid_ref;
ALTER table teachings drop constraint instructor_id_ref;
ALTER table teachings drop constraint teachings_key;


ALTER table subject_memberships drop CONSTRAINT course_offering_uuid_ref;
ALTER table subject_memberships drop CONSTRAINT subject_code_ref;
ALTER table subject_memberships drop CONSTRAINT subject_memberships_key;


ALTER table instructors drop CONSTRAINT instructors_key;


ALTER table rooms drop CONSTRAINT rooms_key;


ALTER table grade_distributions drop CONSTRAINT course_offering_uuid_ref;
ALTER table grade_distributions drop CONSTRAINT grade_distributions_key;


ALTER table subjects drop CONSTRAINT subjects_key;


ALTER table sections drop CONSTRAINT schedule_uuid_ref;
ALTER table sections drop CONSTRAINT course_offering_uuid_ref;
ALTER table sections drop CONSTRAINT sections_key;


ALTER table schedules drop CONSTRAINT schedules_key;


ALTER table course_offerings drop CONSTRAINT course_uuid_ref;
ALTER table course_offerings drop CONSTRAINT course_offerings_key;


ALTER table courses drop CONSTRAINT courses_key;











-- add
ALTER table courses add CONSTRAINT courses_primary_key primary key (uuid);


ALTER table course_offerings add CONSTRAINT course_off_primary_key PRIMARY KEY (uuid);
ALTER table course_offerings add CONSTRAINT course_uuid_foreign_key FOREIGN KEY (course_uuid) references courses(uuid) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER table schedules add CONSTRAINT schedules_primary_key PRIMARY KEY (uuid);


ALTER table sections add CONSTRAINT sections_primary_key PRIMARY KEY (uuid);
ALTER table sections add CONSTRAINT course_offering_uuid_foreign_key FOREIGN KEY (course_offering_uuid) references course_offerings(uuid) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER table sections add CONSTRAINT schedule_uuid_foreign_key FOREIGN KEY (schedule_uuid) references schedules(uuid);


ALTER table subjects add CONSTRAINT subjects_primary_key PRIMARY KEY (code);


ALTER table grade_distributions add CONSTRAINT grade_distributions_primary_key PRIMARY KEY (course_offering_uuid, section_number);
ALTER table grade_distributions add CONSTRAINT course_offering_uuid_foreign_key FOREIGN KEY (course_offering_uuid) references course_offerings(uuid) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER table rooms add CONSTRAINT rooms_primary_key PRIMARY KEY (uuid);


ALTER table instructors add CONSTRAINT instructors_primary_key PRIMARY KEY (id);


ALTER table subject_memberships add CONSTRAINT subject_memberships_primary_key PRIMARY KEY (subject_code,course_offering_uuid);
ALTER table subject_memberships add CONSTRAINT subject_code_foreign_key FOREIGN KEY (subject_code) references subjects(code) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER table subject_memberships add CONSTRAINT course_offering_uuid_foreign_key FOREIGN KEY (course_offering_uuid) references course_offerings(uuid) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER table teachings add CONSTRAINT teachings_primary_key PRIMARY KEY (instructor_id,section_uuid);
ALTER table teachings add CONSTRAINT instructor_id_foreign_key FOREIGN KEY (instructor_id) references instructors(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER table teachings add CONSTRAINT section_uuid_foreign_key FOREIGN KEY (section_uuid) references sections(uuid) ON UPDATE CASCADE ON DELETE CASCADE;




