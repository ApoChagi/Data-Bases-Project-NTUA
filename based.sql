create schema based;
use based;
CREATE TABLE `organization` (
  `ID_Org` int(11) NOT NULL AUTO_INCREMENT,
  `Abbreviation` varchar(5) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Street_Name` varchar(45) NOT NULL,
  `Street_Number` int(4) NOT NULL CHECK (`Street_Number` > 0),
  `Postcode` int(7) NOT NULL CHECK (`Postcode` > 0),
  `City` varchar(45) NOT NULL,
  `Category` varchar(45) NOT NULL,
  `Budget_Ministry_of_Education` int(9) DEFAULT NULL CHECK (`Budget_Ministry_of_Education` >= 0),
  `Budget_Private_Actions` int(9) DEFAULT NULL CHECK (`Budget_Private_Actions` >= 0),
  `Budget_Equity` int(9) DEFAULT NULL CHECK (`Budget_Equity` >= 0),
  PRIMARY KEY (`ID_Org`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `executive` (
  `ID_Executive` int(11) NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(45) NOT NULL,
  `Last_Name` varchar(45) NOT NULL,
  `Branch` varchar(100) NOT NULL,
  PRIMARY KEY (`ID_Executive`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `program` (
`ID_Program` int NOT NULL auto_increment,
`Branch` varchar(100) NOT NULL,
PRIMARY KEY (`ID_Program`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `scientific_field` (
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `researcher` (
  `ID_Researcher` int(11) NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(45) NOT NULL,
  `Last_Name` varchar(45) NOT NULL,
  `Gender` varchar(6) NOT NULL,
  `Birth_Date` date NOT NULL,
  `ID_org` int(11) NOT NULL,
  `Work_Start_Date` date NOT NULL CHECK (year(`Work_Start_Date`) - year(`Birth_Date`) > 0),
  PRIMARY KEY (`ID_Researcher`),
  KEY `ID_org` (`ID_org`),
  CONSTRAINT `ID_org_Researcher` FOREIGN KEY (`ID_org`) REFERENCES `organization` (`ID_Org`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `organization_phone_numbers` (
  `ID_Org` int(11) NOT NULL,
  `Phone_Number` varchar(10) NOT NULL,
  PRIMARY KEY (`ID_Org`, `Phone_Number`),
  CONSTRAINT `ID_Org_P` foreign key (`ID_Org`) REFERENCES `organization` (`ID_Org`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `project` (
  `ID_Project` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(45) NOT NULL,
  `Description` varchar(45) NOT NULL,
  `Start_Date` date NOT NULL,
  `Finish_Date` date NOT NULL CHECK (to_days(`Finish_Date`) - to_days(`Start_Date`) > 0),
  `Funding_Amount` int(11) NOT NULL CHECK (`Funding_Amount` >= 100000 and `Funding_Amount` <= 1000000),
  `Duration` int(11) GENERATED ALWAYS AS (year(`Finish_Date`) - year(`Start_Date`)) VIRTUAL CHECK (`Duration` <= 4),
  `ID_org` int(11) NOT NULL,
  `ID_Researcher_in_Charge` int(11) NOT NULL,
  `ID_Evaluator` int(11) NOT NULL,
  `Evaluation_Grade` int(2) NOT NULL CHECK (`Evaluation_Grade` >= 0 and `Evaluation_Grade` <= 10),
  `Evaluation_Date` date NOT NULL CHECK (to_days(`Evaluation_Date`) - to_days(`Start_Date`) < 0),
  `ID_Program` int(11) NOT NULL,
  `ID_Executive` int(11) NOT NULL,
  PRIMARY KEY (`ID_Project`),
  KEY `ID_org` (`ID_org`),
  KEY `ID_Researcher_in_Charge` (`ID_Researcher_in_Charge`),
  KEY `ID_Evaluator` (`ID_Evaluator`),
  KEY `ID_Program` (`ID_Program`),
  KEY `ID_Executive` (`ID_Executive`),
  CONSTRAINT `ID_Evaluator_Project` FOREIGN KEY (`ID_Evaluator`) REFERENCES `researcher` (`ID_Researcher`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ID_Executive_Project` FOREIGN KEY (`ID_Executive`) REFERENCES `executive` (`ID_Executive`) ON UPDATE CASCADE,
  CONSTRAINT `ID_Program_Project` FOREIGN KEY (`ID_Program`) REFERENCES `program` (`ID_Program`) ON UPDATE CASCADE,
  CONSTRAINT `ID_Researcher_in_Charge_Project` FOREIGN KEY (`ID_Researcher_in_Charge`) REFERENCES `researcher` (`ID_Researcher`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ID_org_Project` FOREIGN KEY (`ID_org`) REFERENCES `organization` (`ID_Org`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




CREATE TABLE `deliverable` (
  `ID_Project` int(11) NOT NULL,
  `Title` varchar(45) NOT NULL,
  `Description` varchar(45) NOT NULL,
  `Delivery_Date` date NOT NULL,
  PRIMARY KEY (`ID_Project`,`Title`),
  CONSTRAINT `ID_Project_del` FOREIGN KEY (`ID_Project`) references `project` (`ID_Project`) on delete cascade on update cascade
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `works` (
  `ID_Project` int(11) NOT NULL,
  `ID_Researcher` int(11) NOT NULL,
  PRIMARY KEY (`ID_Project`,`ID_Researcher`),
  KEY `ID_Project` (`ID_Project`),
  KEY `ID_Researcher` (`ID_Researcher`),
  CONSTRAINT `ID_Researcher_Works` FOREIGN KEY (`ID_Researcher`) REFERENCES `researcher` (`ID_Researcher`) ON DELETE cascade ON UPDATE CASCADE,
  CONSTRAINT `ID_Project_Works` FOREIGN KEY (`ID_Project`) REFERENCES `project` (`ID_Project`) ON DELETE cascade ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `project_field` (
  `ID_Project` int(11) NOT NULL,
  `Field_Title` varchar(50) NOT NULL,
  PRIMARY KEY (`ID_Project`,`Field_Title`),
  KEY `ID_Project` (`ID_Project`),
  KEY `Field_Title` (`Field_Title`),
  CONSTRAINT `ID_Project_Field` FOREIGN KEY (`ID_Project`) REFERENCES `project` (`ID_Project`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Title_Field` FOREIGN KEY (`Field_Title`) REFERENCES `scientific_field` (`Name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DELIMITER $$
create trigger hmmm before insert on works
FOR each row
begin
        if (new.ID_Researcher = (select ID_Evaluator as m from project where ID_Project = new.ID_Project)) then

        signal sqlstate '45000' SET MESSAGE_TEXT = 'A researcher cannot work in a project which he evaluated.';
  END IF;
  end;
  $$
  DELIMITER ;
  
  DELIMITER $$
  create trigger mhh before update on project
  for each row
  begin
		if (new.ID_Evaluator = (select ID_Researcher from works where (ID_Project = new.ID_Project and ID_Researcher = new.ID_Evaluator))) then
        signal sqlstate '45000' SET MESSAGE_TEXT = 'This researcher works or worked in the selected project. Therefore he cannot be its evaluator';
        end if;
	end;
    $$
  DELIMITER ;
  
  DELIMITER $$
  create trigger insp after insert on project
  for each row
  begin
		INSERT INTO works (`ID_Project`, `ID_Researcher`) values (new.ID_Project, new.ID_Researcher_in_Charge);
        end;
        $$
DELIMITER ;
  
DELIMITER $$
create trigger updp after update on project
for each row
begin
		if ((datediff(curdate(),new.Finish_Date) < 0) and new.ID_Researcher_in_charge not in (select ID_Researcher from works where ID_Project = new.ID_Project)) then
        INSERT INTO works (`ID_Project`, `ID_Researcher`) values (new.ID_Project, new.ID_Researcher_in_Charge);
        end if;
        end;
        $$
DELIMITER ;

DELIMITER $$
create trigger delr before delete on researcher
for each row 
begin 
		if (old.ID_Researcher in (select ID_Evaluator from project)) then
        signal sqlstate '45000' SET MESSAGE_TEXT = 'You cannot delete an evaluator. To do so set a new evaluator to the corresponding project.';
        end if;
        end;
        $$
DELIMITER ;

DELIMITER $$
create trigger delr2 before delete on researcher
for each row 
begin 
		if (old.ID_Researcher in (select ID_Researcher_in_Charge from project)) then
        signal sqlstate '45000' SET MESSAGE_TEXT = 'You cannot delete a chief. To do so set a new chief to the corresponding project.';
        end if;
        end;
        $$
DELIMITER ;

DELIMITER $$
create trigger delex before delete on executive
for each row 
begin 
		if (old.ID_Executive in (select ID_Executive from project)) then
        signal sqlstate '45000' SET MESSAGE_TEXT = 'You cannot delete this executive. To do so set a new executive to the corresponding project.';
        end if;
        end;
        $$
DELIMITER ;

DELIMITER $$
create trigger delprf before delete on project_field
for each row
begin 
	if ((select count(old.ID_Project) from project_field where ID_Project = old.ID_Project) = 1) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'Every project must have at least one Field Title.';
    end if;
    end;
    $$
DELIMITER ;

DELIMITER $$
create trigger rescheck before insert on works
for each row
begin
	if ((select ID_org from project where ID_Project = new.ID_Project) <> (select ID_org from researcher where ID_Researcher = new.ID_Researcher)) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A researcher can only work in projects which belong to their organization.';
    end if;
    end;
    $$
DELIMITER ;

DELIMITER $$
create trigger resc before delete on works
for each row
begin
	if (old.ID_Researcher = (select ID_Researcher_in_Charge from project where ((ID_Project = old.ID_Project) and (datediff(curdate(), Finish_Date) < 0)))) then
	signal sqlstate '45000' SET MESSAGE_TEXT = 'A chief researcher cannot be deleted when the project is active. To do so you must first set a new chief.';
    end if;
    end;
$$
DELIMITER ;
		
DELIMITER $$
create trigger budget before insert on organization
for each row
begin
	if ((new.Category = 'Company') and (new.Budget_Equity = null)) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A company must have a not null Equity Budget';
    elseif (new.Category = 'Research Center' and (new.Budget_Ministry_of_Education = null or new.Budget_Private_Actions = null)) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A research center must have a not null Budget from Ministry of Education and from Private Actions';
    elseif (new.Category = 'University' and new.Budget_Ministry_of_Education = null) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A university must have a not null Budget from Ministry of Education';
    end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger budgetn before insert on organization
for each row
begin
	if ((new.Category = 'Company') and (new.Budget_Ministry_of_Education >=0 or new.Budget_Private_Actions >=0)) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A company cannot have a not null Budget from Ministry of Education or from Private Actions';
    elseif (new.Category = 'Research Center' and (new.Budget_Equity >= 0)) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A research center cannot have a not null Equity Budget';
    elseif (new.Category = 'University' and (new.Budget_Equity >=0 or new.Budget_Private_Actions >=0)) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A university cannot have a not null budget from Equity or from Private Actions';
    end if;
    end;
$$
DELIMITER ;


DELIMITER $$
create trigger budgetu before update on organization
for each row
begin
	if ((new.Category = 'Company') and (new.Budget_Ministry_of_Education >=0 or new.Budget_Private_Actions >=0)) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A company cannot have a not null Budget from Ministry of Education or from Private Actions';
    elseif (new.Category = 'Research Center' and (new.Budget_Equity >= 0)) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A research center cannot have a not null Equity Budget';
    elseif (new.Category = 'University' and (new.Budget_Equity >=0 or new.Budget_Private_Actions >=0)) then
    signal sqlstate '45000' SET MESSAGE_TEXT = 'A university cannot have a not null budget from Equity or from Private Actions';
    end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger inr before insert on researcher
for each row
begin
	if ((dayname(new.Work_Start_Date) is null) or (dayname(new.Birth_Date) is null)) then
    signal sqlstate '45000' set message_text = 'You inserted a non valid date type. Insert a (YY-MM-DD) date.';
    end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger upr before update on researcher
for each row
begin
	if ((dayname(new.Work_Start_Date) is null) or (dayname(new.Birth_Date) is null)) then
    signal sqlstate '45000' set message_text = 'You inserted a non valid date type. Insert a (YY-MM-DD) date.';
    end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger inp before insert on project
for each row
begin
	if ((dayname(new.Start_Date) is null) or (dayname(new.Finish_Date) is null) or (dayname(new.Evaluation_Date))) then
    signal sqlstate '45000' set message_text = 'You inserted a non valid date type. Insert a (YY-MM-DD) date.';
    end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger upp before update on project
for each row
begin
	if ((dayname(new.Start_Date) is null) or (dayname(new.Finish_Date) is null) or (dayname(new.Evaluation_Date))) then
    signal sqlstate '45000' set message_text = 'You inserted a non valid date type. Insert a (YY-MM-DD) date.';
    end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger ind before insert on deliverable
for each row
begin
	if (dayname(new.Delivery_Date) is null) then
    signal sqlstate '45000' set message_text = 'You inserted a non valid date type. Insert a (YY-MM-DD) date.';
    end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger upd before insert on deliverable
for each row
begin
	if (dayname(new.Delivery_Date) is null) then
    signal sqlstate '45000' set message_text = 'You inserted a non valid date type. Insert a (YY-MM-DD) date.';
    end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger resup before update on researcher
for each row
begin
	if ((new.ID_org <> old.ID_org) and (old.ID_Researcher in (select w.ID_Researcher as ID from works w inner join project p on w.ID_Project=p.ID_Project where datediff(curdate(), p.Finish_Date) < 0 group by ID))) then
    signal sqlstate '45000' set message_text = 'You cannot change the organization when the researcher is currently working in a project. To do so first delete from works.';
	end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger resupc after update on researcher
for each row
begin
	if ((new.ID_org <> old.ID_org)) then
    delete from works where ID_Researcher = old.ID_Researcher;
	end if;
    end;
$$
DELIMITER ;

DELIMITER $$
create trigger scifii before delete on scientific_field
for each row
begin
	if (old.Name in (select Field_Title from project_field group by Field_Title)) then
    signal sqlstate '45000' set message_text = 'You cannot delete a scientific field which characterizes a project';
    end if;
    end;
$$
DELIMITER ;

create index startdate on project(Start_Date);
create index finishdate on project(Finish_Date);
create index birthdate on researcher(Birth_Date);

create view submissions as 
select p.ID_Project, p.Title as Name, d.Title as Submission_Title, d.Description  
from project p inner join deliverable d on p.ID_Project = d.ID_Project;

create view researcher_projects as 
SELECT r.ID_Researcher, r.First_Name, r.Last_Name, p.ID_Project, p.Title as Project_Title, p.Funding_Amount 
from researcher r 
inner join works w on r.ID_Researcher = w.ID_Researcher 
inner join project p on w.ID_Project = p.ID_Project;
