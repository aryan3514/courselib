
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
