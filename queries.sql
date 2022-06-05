/* ----------- QUERY 3.1 -------------- */
select ID_Project, Title, Description, Start_Date, Finish_Date, Duration, Funding_Amount, ID_org, ID_Program, ID_Executive 
from project 
where Duration = 2  /* and Start_Date =  and  Finish_Date = */ and ID_Executive = 15; /*edit parameters to customize QUERY*/

/* ----------- QUERY 3.1 -------------- */
select p.ID_Project, p.Title, r.First_Name, r.Last_Name, r.Gender, r.Birth_Date, r.ID_org, r.Work_Start_Date 
from project p 
inner join works w on p.ID_Project = w.ID_Project 
inner join researcher r on w.ID_Researcher = r.ID_Researcher 
where p.ID_Project = 15; /*edit parameters to customize QUERY*/


/* ----------- 3.2 VIEWS  -------------- */
create view researcher_projects as 
SELECT r.ID_Researcher, r.First_Name, r.Last_Name, p.ID_Project, p.Title as Project_Title, p.Funding_Amount 
from researcher r 
inner join works w on r.ID_Researcher = w.ID_Researcher 
inner join project p on w.ID_Project = p.ID_Project;

create view submissions as 
select p.ID_Project, p.Title as Name, d.Title as Submission_Title, d.Description  
from project p inner join deliverable d on p.ID_Project = d.ID_Project ; 


/* ----------- QUERY 3.3 -------------- */
select pf.Field_Title, p.ID_Project, p.Title, r.ID_Researcher, r.First_Name, r.Last_Name 
from project_field pf 
inner join project p on pf.ID_Project = p.ID_Project 
inner join works w on p.ID_Project = w.ID_Project 
inner join researcher r on w.ID_Researcher = r.ID_Researcher 
where pf.Field_Title = 'Education and Human Society' /*edit parameters to customize QUERY*/
	and DATEDIFF(CURDATE(), r.Work_Start_Date) > 365 /* researcher started work on the org at least a year ago */
	and DATEDIFF(CURDATE(), p.Start_Date) > 365      /* project started at least a year ago */ 
    and DATEDIFF(CURDATE(), p.Finish_Date) < 0;		 /* project is active */ 
    
    
/* ----------- QUERY 3.4 -------------- */
select k.ID, o.Name, k.year, k.Number from (select n.ID as ID, n.year as year, n.Number as Number from 
(select ID_org as ID, year(Start_Date) as year, count(ID_Project) as Number from project group by ID_org, year(Start_Date)) n 
where (n.Number >= 10 and (n.ID,n.year+1,n.Number) in (select p.ID, p.year, p.Number from 
(select ID_org as ID, year(Start_Date) as year, count(ID_Project) as Number from project group by ID_org, year(Start_Date)) p))) k 
inner join organization o on o.ID_Org = k.ID;


/* ----------- QUERY 3.5 -------------- */
select sf1.Name, sf2.Name, count(pf.ID_Project) as number_of_projects 
from scientific_field sf1 
inner join scientific_field sf2 on sf1.Name <> sf2.Name and sf1.Name < sf2.Name 
join project_field pf on pf.Field_Title = sf1.Name 
where (pf.ID_Project, sf2.Name) in (select ID_Project, Field_Title from project_field) 
group by sf1.Name, sf2.Name 
order by number_of_projects DESC  
limit 3;


/* ----------- QUERY 3.6 -------------- */
select r.ID_Researcher, r.First_Name, r.Last_Name, TIMESTAMPDIFF(year, r.Birth_Date, CURDATE()) as Age, count(p.ID_Project) as Number_of_Active_Projects 
from researcher r 
inner join works w on r.ID_Researcher = w.ID_Researcher 
inner join project p on w.ID_Project = p.ID_Project 
where DATEDIFF(CURDATE(), p.Finish_Date) < 0  /* check if project is active */
group by r.ID_Researcher having Age < 40 
order by Number_of_Active_Projects DESC
limit 10;


/* ----------- QUERY 3.7 -------------- */
select e.First_Name, e.Last_Name, o.Name, p.Funding_Amount 
from executive e 
inner join project p on e.ID_Executive = p.ID_Executive 
inner join organization o on p.ID_org = o.ID_Org 
where o.Category = 'Company' 
order by p.Funding_Amount DESC 
limit 5;


/* ----------- QUERY 3.8 -------------- */
select r.ID_Researcher, r.First_Name, r.Last_Name, count(p.ID_Project) as Number_of_Projects_without_Submissions 
from researcher r 
inner join works w on r.ID_Researcher = w.ID_Researcher 
inner join project p on w.ID_Project = p.ID_Project 
where p.ID_Project not in (select ID_Project from deliverable) 
group by r.ID_Researcher 
having Number_of_Projects_without_Submissions > 4;










