DROP FUNCTION check_if_inst_code_taken;
DROP FUNCTION check_if_inst_code_is_numeric;


drop trigger inst_update_trigger on instructors;
drop trigger inst_insert_trigger on instructors;
drop trigger inst_insert_numeric_trigger on instructors;
drop trigger inst_update_numeric_trigger on instructors;


