DELIMITER $
create trigger verify_insert_data
before insert on course
for each row
BEGIN
	if new.name='' then
    set new.name=null;
	end if ;
    if new.id='' then
    set new.id=null;
	end if ;
    if new.college='' then
    set new.college=null;
	end if ;
end
$
DELIMITER ;

DELIMITER $
create trigger verify_update_data
before update on course
for each row
BEGIN
	if new.name='' then
    set new.name=null;
	end if ;
    if new.id='' then
    set new.id=null;
	end if ;
    if new.college='' then
    set new.college=null;
	end if ;
end
$
DELIMITER ;

DELIMITER $
create trigger verify_student_insert_data
before insert on student
for each row
BEGIN
	if new.name='' then
    set new.name=null;
	end if ;
    if new.id='' then
    set new.id=null;
	end if ;
    if new._class='' then
    set new._class=null;
	end if ;
end
$
DELIMITER ;

DELIMITER $
create trigger verify_student_update_data
before update on student
for each row
BEGIN
	if new.name='' then
    set new.name=null;
	end if ;
    if new.id='' then
    set new.id=null;
	end if ;
    if new._class='' then
    set new._class=null;
	end if ;
end
$
DELIMITER ;

drop trigger verify_update_data
