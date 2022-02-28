
CREATE OR REPLACE FUNCTION check_if_inst_code_taken()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.id IN (select instructors.id from instructors) THEN
    RETURN NULL;
  END IF;
	RETURN NEW;
END;
$$;







CREATE OR REPLACE FUNCTION check_if_inst_code_is_numeric()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NOT (NEW.id ~ '^[0-9]*$') THEN
    RETURN NULL;
  END IF;
	RETURN NEW;
END;
$$;






CREATE OR REPLACE FUNCTION check_if_sub_code_taken()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.code IN (select subjects.code from subjects) THEN
    RETURN NULL;
  END IF;
	RETURN NEW;
END;
$$;


CREATE OR REPLACE FUNCTION check_if_sub_abbr_taken()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF NEW.abbreviation IN (select subjects.abbreviation from subjects) THEN
    RETURN NULL;
  END IF;
	RETURN NEW;
END;
$$;


CREATE OR REPLACE FUNCTION check_if_room_taken()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF (NEW.facility_code,NEW.room_code) IN (select rooms.facility_code, rooms.room_code from rooms) THEN
    RETURN NULL;
  END IF;
	RETURN NEW;
END;
$$; 

CREATE OR REPLACE FUNCTION check_if_student_already_watchlisted()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF (NEW.student_id, NEW.course_offering_name_term_code, NEW.section_type, NEW.instructor_name_sec_number) IN (select * from student_watchlist) THEN
    RETURN NULL;
  END IF;
	RETURN NEW;
END;
$$;
--TRIGGER 1--

--BEFORE UPDATE

CREATE or REPLACE TRIGGER inst_update_trigger
    BEFORE UPDATE ON instructors
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_inst_code_taken();

--TRIGGER 2--


--BEFORE INSERT

CREATE or replace TRIGGER inst_insert_trigger
    BEFORE INSERT ON instructors
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_inst_code_taken();


--TRIGGER 3--

CREATE or replace TRIGGER inst_insert_numeric_trigger
    BEFORE INSERT ON instructors
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_inst_code_is_numeric();


--TRIGGER 4--

CREATE or replace TRIGGER inst_update_numeric_trigger
    BEFORE UPDATE ON instructors
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_inst_code_is_numeric();


--TRIGGER 5--

CREATE or replace TRIGGER sub_code_update_trigger
    BEFORE UPDATE ON subjects
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_sub_code_taken();

--TRIGGER 6--

CREATE or replace TRIGGER sub_code_insert_trigger
    BEFORE INSERT ON subjects
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_sub_code_taken();


--TRIGGER 7--

CREATE or replace TRIGGER sub_abbr_update_trigger
    BEFORE UPDATE ON subjects
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_sub_abbr_taken();
  
CREATE or replace TRIGGER sub_abbr_insert_trigger
    BEFORE INSERT ON subjects
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_sub_abbr_taken();

--TRIGGER 8--

CREATE or replace TRIGGER room_insert_trigger
    BEFORE INSERT ON rooms
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_room_taken();
  
CREATE or replace TRIGGER room_update_trigger
    BEFORE UPDATE ON rooms
    FOR EACH ROW
    EXECUTE PROCEDURE check_if_room_taken(); 

CREATE OR REPLACE TRIGGER watchlist_trigger
    BEFORE INSERT ON student_watchlist
    FOR EACH ROW 
    EXECUTE PROCEDURE check_if_student_already_watchlisted();

