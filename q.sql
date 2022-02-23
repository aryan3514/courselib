with relevant_course_uuid as (select uuid from courses where name='Explorations in Transnational/Comparative History (Humanities)')
, relevant_course_off_name as (select name, term_code from relevant_course_uuid join course_offerings on course_offerings.course_uuid=relevant_course_uuid.uuid)
select * from relevant_course_off_name;