create view c_t_s(StudentId,StudentName,CourseId,CourseName,TeacherId,TeacherName,Semester,ClassId,ClassName,Source)
as
select student.id,student.name,course.id,course.name,teacher.id,teacher.name,course_teach_stu.semester,_class._id,_class.Name,course_teach_stu.source
from _class,course,teacher,student,course_teach_stu
where course.id = course_teach_stu.course and teacher.id = course_teach_stu.teach and student.id = course_teach_stu.stu and student._class = _class._id;


create view stu_semes(StudentId,StudentName,ClassName,Semester,GAvg)
as
select StudentId,StudentName,ClassName,Semester,Avg(Source) 
from c_t_s 
group by Semester,StudentId;

create view class_semes(ClassId,ClassName,Semester,CourseName,GAvg,GMax,GMin,PassNumber,PassRate)
as
select ClassId,c_t_s.ClassName,Semester,c_t_s.CourseName,Avg(Source) as GAvg,MAX(Source) as GMax,MIN(Source) as GMin,PassNumber,PassRate
from c_t_s,
(select ClassName,c_t_s.CourseName,sum(case when source >=60 then 1 else 0 end) as PassNumber,(100*(sum(case when source >=60 then 1 else 0 end)/count(*))) as PassRate from c_t_s  group by Semester,CourseName,ClassName) as a
where a.ClassName = c_t_s.ClassName and a.CourseName=c_t_s.CourseName
group by Semester,CourseName,ClassName;

