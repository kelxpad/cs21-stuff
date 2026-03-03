CREATE OR REPLACE FUNCTION public.f_studentloas_needstanding_tba(p_unitid integer, p_aytermid integer)
 RETURNS SETOF t_studentloas_needstanding_tba
 LANGUAGE sql
AS $function$
select ce.classenlistmentid, sl.studentloaid,
studentno, lastname || ', ' || firstname || ' ' || middlename as fullname,
s_abbrevprogramtext(programid, programmajorid) as  programname,
ls.status,
lr.reason, sl.details,
sl.startayterm, sl.actualendayterm,
sl.insertedon,
classcode, class,
s_hasaccountability(s.studentid)

from classes as c
join classenlistments as ce using (classid)
join studentterms using (studenttermid)
join students as s using (studentid)
join persons using (personid)
join studentloas as sl on (s.studentid =  sl.studentid and (sl.startayterm = c.aytermid or sl.appliedendayterm = c.aytermid))
join loareasons as lr using (loareasonid)
join loastatuses as ls using (loastatusid)
left join classinstructors as ci using (classid)
left join loaclassstandings as lcs on (ce.classenlistmentid = lcs.classenlistmentid AND sl.studentloaid = lcs.studentloaid)
LEFT JOIN enlistmentdrops as ed ON (ce.classenlistmentid = ed.classenlistmentid)
LEFT JOIN drops as d ON (d.dropid = ed.dropid AND d.status = 5)
/*to check if standing has been given already...*/
/*okay na kaya na nastop na ng aytermid, o icheck ko kung tapos na
ang grading sa mga ito?*/

where c.offeringunit = $1
and c.aytermid = $2
and ci.classinstructorid is null
and (lcs.loaclassstandingid is null AND d.dropid is null)
and sl.loastatusid = 1
$function$
