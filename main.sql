--main sql file 
--COURSES UNDER A CERTAIN SUBJECT, VARIABLE HERE IS "ENGLISH"
WITH scode AS (SELECT subjects.code FROM subjects WHERE subjects.name = 'ENGLISH%'
),
coff AS (SELECT subject_memberships.course_offering_uuid   FROM subject_memberships INNER JOIN scode ON scode.code = subject_memberships.subject_code
)

SELECT DISTINCT course_offerings.name
FROM course_offerings INNER JOIN coff ON
coff.course_offering_uuid = course_offerings.uuid 
ORDER BY course_offerings.name;


--QUERY FOR PARTIAL STRING MATCHING, VARIABLE HERE IS 'E%'
SELECT subjects.name FROM subjects WHERE NAME LIKE 'E%';

--COURSE OFFERINGS OF A CERTAIN COURSE
SELECT course_offerings.name, course_offerings.term FROM course_offerings WHERE course_offerings.name = 'ENGLISH%';


-- provides all the instructors ever taught a particular subject (cross check pls)
with relevant_code as (select code from subjects where abbreviation = 'ENGLISH')
, relevant_course_off_uuid as (select course_offering_uuid from relevant_code join subject_memberships on relevant_code.code=subject_memberships.subject_code)
, relevant_sec_id as (select uuid from relevant_course_off_uuid join sections on relevant_course_off_uuid.course_offering_uuid=sections.course_offering_uuid)
, relevant_inst_id as (select instructor_id, count(instructor_id) from relevant_sec_id join teachings on relevant_sec_id.uuid=teachings.section_uuid group by instructor_id)
, relevant_instructors as (select name, id from relevant_inst_id join instructors on relevant_inst_id.instructor_id=instructors.id order by name)
select * from relevant_instructors;
