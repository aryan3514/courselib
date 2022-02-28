
--INSTRUCTORS VS COURSES VIEW--
CREATE OR REPLACE VIEW insts_vs_courses AS
WITH secs AS (SELECT instructors.id, instructors.name, teachings.section_uuid FROM instructors INNER JOIN teachings ON teachings.instructor_id = instructors.id
),
couid AS (SELECT secs.id, secs.name, sections.course_offering_uuid FROM sections INNER JOIN secs ON secs.section_uuid = sections.uuid
),
names AS (SELECT couid.id, couid.name as inst_name, course_offerings.course_uuid FROM course_offerings INNER JOIN couid ON couid.course_offering_uuid = course_offerings.uuid
),
finc AS (SELECT names.id, names.inst_name, courses.name as course_name FROM names INNER JOIN courses ON names.course_uuid=courses.uuid)
select distinct * from finc;


--SUBJECTS VS COURSES VIEW--
CREATE OR REPLACE VIEW subs_vs_courses AS
WITH secs AS (SELECT subjects.code AS scd, subjects.name, subject_memberships.course_offering_uuid FROM subject_memberships INNER JOIN subjects ON subjects.code = subject_memberships.subject_code
),
names AS (SELECT secs.scd, secs.name as subname, course_offerings.course_uuid FROM course_offerings INNER JOIN secs ON secs.course_offering_uuid = course_offerings.uuid
),
finc AS (SELECT names.scd, names.subname, courses.name FROM names INNER JOIN courses ON names.course_uuid=courses.uuid)

select distinct * from finc;


CREATE OR REPLACE VIEW all_info_view AS
WITH a as (select number as sec_number, course_offerings.uuid, CONCAT(name,' - ',term_code) as course_offering_name, sections.uuid as sec_uuid, section_type, room_uuid, schedule_uuid from course_offerings join sections on course_offerings.uuid=sections.course_offering_uuid and room_uuid!='null')
, aa as (select sec_number, uuid, course_offering_name, instructor_id, section_type, room_uuid, schedule_uuid from a join teachings on section_uuid=sec_uuid)
, aaa as (select sec_number, uuid, course_offering_name, CONCAT(instructors.name, ' - ', sec_number) as instructor_name, section_type, room_uuid, schedule_uuid from aa join instructors on instructors.id=instructor_id)
, aaaa as (select sec_number, aaa.uuid, course_offering_name, instructor_name, section_type, facility_code, room_code, schedule_uuid from aaa join rooms on rooms.uuid=room_uuid)
, aaaaa as (select sec_number, aaaa.uuid, course_offering_name, instructor_name, section_type, facility_code, room_code, start_time, end_time, mon, tues, wed, thurs, fri, sat, sun from aaaa join schedules on schedules.uuid=schedule_uuid)
, final_course_off_sections_instructors_schedule_grades_info as (select sec_number, uuid, course_offering_name, instructor_name, section_type, facility_code, room_code, start_time, end_time, mon, tues, wed, thurs, fri, sat, sun, a_count, ab_count, b_count, bc_count, c_count, d_count, f_count, s_count, u_count, cr_count, n_count, p_count, i_count, nw_count, nr_count, other_count from aaaaa join grade_distributions on section_number=sec_number and course_offering_uuid=uuid)
select * from final_course_off_sections_instructors_schedule_grades_info;


CREATE OR REPLACE VIEW inst_vs_off_term_view AS
WITH a as (select CONCAT(name,' - ',term_code) as course_off_name_term, sections.uuid as sec_uuid, number as sec_number from course_offerings join sections on course_offerings.uuid=sections.course_offering_uuid and room_uuid!='null')
, aa as (select course_off_name_term, sec_number, instructor_id from a join teachings on section_uuid=sec_uuid)
, relevant_instructors as (select course_off_name_term, CONCAT(instructors.name, ' - ', sec_number) as instructor_name_sec  from aa join instructors on instructors.id=instructor_id)
select * from relevant_instructors order by instructor_name_sec;







