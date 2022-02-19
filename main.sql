--main sql file 
--COURSES UNDER A CERTAIN SUBJECT, VARIABLE HERE IS "ENGLISH"
WITH scode AS (SELECT subjects.code FROM subjects WHERE subjects.name = 'ENGLISH%'
),
coff AS (SELECT subject_memberships.course_offering_uuid   FROM subject_memberships INNER JOIN scode ON scode.code = subject_memberships.subject_code
)

SELECT DISTINCT course_offerings.name
FROM course_offerings INNER JOIN coff ON
coff.course_offering_uuid = course_offerings.uuid 
ORDER BY course_offerings.name


--QUERY FOR PARTIAL STRING MATCHING, VARIABLE HERE IS 'E%'
SELECT subjects.name FROM subjects WHERE NAME LIKE 'E%';

--COURSE OFFERINGS OF A CERTAIN COURSE
SELECT course_offerings.name, course_offerings.term FROM course_offerings WHERE course_offerings.name = 'ENGLISH%';
