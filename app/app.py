# -*- coding: utf-8 -*-
"""
Created on Wed May 18 15:35:19 2022

@author: Apostolos
"""

from flask import Flask, request, redirect
from flask_mysqldb import MySQL
from flask import url_for
from flask import render_template
import mysql.connector

#HOW TO CONNECT TO DATABASE


app = Flask(__name__)
app.secret_key=''
mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     passwd=""
)
@app.route('/', methods=['GET', 'POST'])
def init():
    return render_template('index.html')

@app.route('/start', methods=['GET', 'POST'])
def neo():
    return render_template('landing.html')

@app.route('/executives', methods=['GET', 'POST'])
def execu():
    try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM executive")
            column_names = [i[0] for i in mycursor.description]
            executives = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('executives.html', executives = executives)
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg) 


@app.route('/executives/delete/<int:executiveID>', methods = ['GET', 'POST'])
def deleteExec(executiveID):
    query = f"DELETE FROM executive WHERE ID_Executive = {executiveID};"
    try:
        mycursor = mydb.cursor()
        mycursor.execute("Use based")
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        #flash("Student deleted successfully", "primary")
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg)
    return redirect(url_for("execu"))


@app.route('/executives/update/<int:executiveID>', methods = ['GET', 'POST'])
def updateExec(executiveID):
    if (request.method == "GET"):
        query = f"select *FROM executive WHERE ID_Executive = {executiveID};"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            column_names = [i[0] for i in mycursor.description]
            execut = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('executives_update.html', execut = execut)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        try: 
        #query = "INSERT INTO executive(First_Name, Last_Name, Branch) VALUES ('{}', '{}', '{}');".format(newExecutive['First_Name'].data, newExecutive['Last_Name'].data, newExecutive['Branch'].data)
            FirstName = request.form['fname']
            LastName = request.form['lname']
            Branch = request.form['branch']
            query = (f"update executive set First_Name = COALESCE(NULLIF(('%s'),''),First_Name),Last_Name= COALESCE(NULLIF(('%s'),''),Last_Name), Branch = COALESCE(NULLIF(('%s'),''),Branch) where ID_Executive = {executiveID}" %(FirstName,LastName,Branch))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)



@app.route("/executives/create", methods = ["GET", "POST"]) ## "GET" by default
def createExe():
    if (request.method == "GET"):
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT DISTINCT Branch from executive")
            column_names = [i[0] for i in mycursor.description]
            br = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template("executives_create.html", br = br)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    elif (request.method == "POST" ):
        try: 
        #query = "INSERT INTO executive(First_Name, Last_Name, Branch) VALUES ('{}', '{}', '{}');".format(newExecutive['First_Name'].data, newExecutive['Last_Name'].data, newExecutive['Branch'].data)
            FirstName = request.form['fname']
            LastName = request.form['lname']
            Branch = request.form['branch']
            query = ("INSERT INTO executive(First_Name, Last_Name, Branch) VALUES (NULLIF('%s',''), NULLIF('%s',''), NULLIF('%s',''))" %(FirstName,LastName,Branch))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)

    
@app.route('/organizations', methods=['GET', 'POST'])
def org():
    try:
            mydb = mysql.connector.connect(
                 host="localhost",
                 user="root",
                 passwd=""
            )
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM organization")
            column_names = [i[0] for i in mycursor.description]
            organizations = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('organizations.html', organizations = organizations)
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg) 
        
@app.route('/organizations/delete/<int:orgID>', methods = ['GET', 'POST'])
def deleteorg(orgID):
    query = f"DELETE FROM organization WHERE ID_Org = {orgID};"
    try:
        mycursor = mydb.cursor()
        mycursor.execute("Use based")
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        #flash("Student deleted successfully", "primary")
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg)
    return redirect(url_for("org"))


@app.route('/organizations/update/<int:orgID>', methods = ['GET', 'POST'])
def updateOrg(orgID):
    if (request.method == "GET"):
        query = f"select *FROM organization WHERE ID_Org = {orgID};"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            column_names = [i[0] for i in mycursor.description]
            org = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.execute("SELECT DISTINCT Category from organization")
            column_names = [i[0] for i in mycursor.description]
            category = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('organizations_update.html', org = org, category = category)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
       try: 
           Abbrev = request.form['abbrev']
           Name = request.form['name']
           StreetName = request.form['sname']
           Streetnum = request.form['snum']
           Postcode = request.form['postc']
           City = request.form['city']
           Category = request.form['categ']
           minb = request.form['mined']
           if len(minb) == 0:
               minb = None
               if (Category == 'University' or Category == 'Research Center'):
                   minb = '0'
           prac = request.form['prac']
           if len(prac) == 0:
               prac = None
               if (Category == 'Research Center'):
                   prac = '0'
           eqb = request.form['eq']
           if len(eqb) == 0:
               eqb = None
               if (Category == 'Company'):
                   eqb = '0'
           #query = ("update organization set Abbreviation = (%s), Name = (%s), Street_Name = (%s), Street_Number = (%s), Postcode = (%s), City = (%s), Category = (%s) Budget_Ministry_of_Education = (%s), Budget_Private_Actions = (%s), Budget_Equity = (%s) WHERE ID_Org = {orgID}", (Abbrev,Name,StreetName,Streetnum,Postcode,City,Category,minb,prac,eqb))
           mycursor = mydb.cursor()
           mycursor.execute("Use based")
           mycursor.execute("update organization set Abbreviation = COALESCE(NULLIF((%s),''),Abbreviation), Name = COALESCE(NULLIF((%s),''),Name), Street_Name = COALESCE(NULLIF((%s),''),Street_Name), Street_Number = COALESCE(NULLIF((%s),''),Street_Number), Postcode = COALESCE(NULLIF((%s),''),Postcode), City = COALESCE(NULLIF((%s),''),City), Category = (%s), Budget_Ministry_of_Education = (%s), Budget_Private_Actions = (%s), Budget_Equity = (%s) WHERE ID_Org = (%s)", (Abbrev,Name,StreetName,Streetnum,Postcode,City,Category,minb,prac,eqb,orgID))
           mydb.commit()
           mycursor.close()
           return redirect(url_for("init"))
       except mysql.connector.Error as err:
           msg = err.msg
           return render_template("landing.html", msg = msg)




@app.route("/organizations/create", methods = ["GET", "POST"]) ## "GET" by default
def createorg():
    if (request.method == "GET"):
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT DISTINCT Category from organization")
            column_names = [i[0] for i in mycursor.description]
            category = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template("organizations_create.html", category = category)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    elif (request.method == "POST" ):
        try: 
            Abbrev = request.form['abbrev']
            Name = request.form['name']
            StreetName = request.form['sname']
            Streetnum = request.form['snum']
            Postcode = request.form['postc']
            City = request.form['city']
            Category = request.form['categ']
            minb = request.form['mined']
            if len(minb) == 0:
                minb = None
                if (Category == 'University' or Category == 'Research Center'):
                    minb = '0'
            prac = request.form['prac']
            if len(prac) == 0:
                prac = None
                if (Category == 'Research Center'):
                    prac = '0'
            eqb = request.form['eq']
            if len(eqb) == 0:
                eqb = None
                if (Category == 'Company'):
                    eqb = '0'
            #query = ("INSERT INTO organization (`Abbreviation`,`Name`,`Street_Name`,`Street_Number`,`Postcode`,`City`,`Category`,`Budget_Ministry_of_Education`,`Budget_Private_Actions`,`Budget_Equity`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [Abbrev, Name,StreetName, Streetnum, Postcode, City, Category, minb, prac, eqb])
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("INSERT INTO organization (`Abbreviation`,`Name`,`Street_Name`,`Street_Number`,`Postcode`,`City`,`Category`,`Budget_Ministry_of_Education`,`Budget_Private_Actions`,`Budget_Equity`) VALUES (NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), NULLIF(%s,''), %s, %s, %s, %s)", (Abbrev, Name,StreetName, Streetnum, Postcode, City, Category, minb, prac, eqb))
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)

    ## else, response for GET request
    return render_template('organizations_create.html')


@app.route('/researchers', methods=['GET', 'POST'])
def res():
    try:
            mydb = mysql.connector.connect(
                 host="localhost",
                 user="root",
                 passwd=""
            )
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM researcher")
            column_names = [i[0] for i in mycursor.description]
            researchers = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('researchers.html', researchers = researchers)
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg) 
        
@app.route('/researchers/delete/<int:resID>', methods = ['GET', 'POST'])
def deleteres(resID):
    query = f"DELETE FROM researcher WHERE ID_Researcher = {resID};"
    try:
        mycursor = mydb.cursor()
        mycursor.execute("Use based")
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        #flash("Student deleted successfully", "primary")
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg)
    return redirect(url_for("res"))

@app.route('/researchers/update/<int:resID>', methods = ['GET', 'POST'])
def updateRes(resID):
    if (request.method == "GET"):
        query = f"select *FROM researcher WHERE ID_Researcher = {resID};"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            column_names = [i[0] for i in mycursor.description]
            res = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('researchers_update.html', res = res)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        try: 
            FirstName = request.form['fname']
            LastName = request.form['lname']
            Gender = request.form['gen']
            Bdate = request.form['bdate']
            org = request.form['org']
            Workstart = request.form['wstart']
            query = (f"update researcher set First_Name = COALESCE(NULLIF(('%s'),''),First_Name), Last_Name = COALESCE(NULLIF(('%s'),''),Last_Name), Gender = ('%s'), Birth_Date = COALESCE(NULLIF(('%s'),''),Birth_Date), ID_Org = COALESCE(NULLIF(('%s'),''),ID_Org), Work_Start_Date = COALESCE(NULLIF(('%s'),''),Work_Start_Date) WHERE ID_Researcher = {resID}" %(FirstName,LastName,Gender,Bdate,org,Workstart))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)



@app.route("/researchers/create", methods = ["GET", "POST"]) ## "GET" by default
def createres():
    if (request.method == "POST" ):
        try: 
            FirstName = request.form['fname']
            LastName = request.form['lname']
            Gender = request.form['gen']
            Bdate = request.form['bdate']
            org = request.form['org']
            Workstart = request.form['wstart']
            query = ("insert into researcher (`First_Name`, `Last_Name`, `Gender`, `Birth_Date`, `ID_Org`, `Work_Start_Date`) values (NULLIF('%s',''), NULLIF('%s',''), '%s', '%s', '%s', '%s')" %(FirstName,LastName,Gender,Bdate,org,Workstart))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)

    ## else, response for GET request
    return render_template('researchers_create.html')

        
@app.route('/programs', methods=['GET', 'POST'])
def prog():
    try:
            mydb = mysql.connector.connect(
                 host="localhost",
                 user="root",
                 passwd=""
            )
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM program")
            column_names = [i[0] for i in mycursor.description]
            programs = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('programs.html', programs = programs)
    except mysql.connector.Error as err:
       msg = err.msg
       return render_template("landing.html", msg = msg) 


@app.route('/programs/delete/<int:progID>', methods = ['GET', 'POST'])
def deleteprog(progID):
    query = f"DELETE FROM program WHERE ID_Program = {progID};"
    try:
        mycursor = mydb.cursor()
        mycursor.execute("Use based")
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        #flash("Student deleted successfully", "primary")
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg)
    return redirect(url_for("prog"))

@app.route('/programs/update/<int:progID>', methods = ['GET', 'POST'])
def updateProg(progID):
    if (request.method == "GET"):
        query = f"select *FROM program WHERE ID_Program = {progID};"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            column_names = [i[0] for i in mycursor.description]
            prog = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('programs_update.html', prog = prog)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        try: 
            Branchp = request.form['br']
            query = (f"update program set Branch = COALESCE(NULLIF(('%s'),''),Branch) WHERE ID_Program = {progID}" %(Branchp))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)



@app.route("/programs/create", methods = ["GET", "POST"]) ## "GET" by default
def createpro():
    if (request.method == "GET"):
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT DISTINCT Branch from program")
            column_names = [i[0] for i in mycursor.description]
            branchp = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('programs_create.html', branchp = branchp)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    elif (request.method == "POST" ):
        try: 
            Branchp = request.form['br']
            query = ("insert into program (Branch) values (NULLIF('%s',''))" %(Branchp))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)

    ## else, response for GET request
    return render_template('programs_create.html')

        
@app.route('/projects', methods=['GET', 'POST'])
def proj():
    try:
            mydb = mysql.connector.connect(
                 host="localhost",
                 user="root",
                 passwd=""
            )
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM project")
            column_names = [i[0] for i in mycursor.description]
            projects = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('projects.html', projects = projects)
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg) 
        
@app.route('/projects/delete/<int:projID>', methods = ['GET', 'POST'])
def deleteproj(projID):
    query = f"DELETE FROM project WHERE ID_Project = {projID};"
    try:
        mycursor = mydb.cursor()
        mycursor.execute("Use based")
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()
        #flash("Student deleted successfully", "primary")
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg)
    return redirect(url_for("proj"))

@app.route('/projects/update/<int:projID>', methods = ['GET', 'POST'])
def updateProj(projID):
    if (request.method == "GET"):
        query = f"select *FROM project WHERE ID_Project = {projID};"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            column_names = [i[0] for i in mycursor.description]
            proj = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('projects_update.html', proj = proj)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        try: 
            Title = request.form['title']
            Description = request.form['desc']
            Startdate = request.form['sdat']
            Finishdate = request.form['fdat']
            Funding = request.form['fun']
            Org = request.form['org']
            Chief = request.form['resc']
            Evaluator = request.form['eval']
            Grade = request.form['grade']
            Evaldate = request.form['evdat']
            Prog = request.form['prog']
            Executive = request.form['exec']
            query = (f"update project set Title = COALESCE(NULLIF(('%s'),''),Title), Description = COALESCE(NULLIF(('%s'),''),Description), Start_Date = COALESCE(NULLIF(('%s'),''),Start_Date), Finish_Date = COALESCE(NULLIF(('%s'),''),Finish_Date), Funding_Amount = COALESCE(NULLIF(('%s'),''),Funding_Amount), ID_Org = COALESCE(NULLIF(('%s'),''),ID_Org), ID_Researcher_in_Charge = COALESCE(NULLIF(('%s'),''),ID_Researcher_in_Charge), ID_Evaluator = COALESCE(NULLIF(('%s'),''),ID_Evaluator), Evaluation_Grade = COALESCE(NULLIF(('%s'),''),Evaluation_Grade), Evaluation_Date = COALESCE(NULLIF(('%s'),''),Evaluation_Date), ID_Program = COALESCE(NULLIF(('%s'),''),ID_Program), ID_Executive = COALESCE(NULLIF(('%s'),''),ID_Executive) WHERE ID_Project = {projID}" %(Title,Description,Startdate,Finishdate,Funding,Org,Chief,Evaluator,Grade,Evaldate,Prog,Executive))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
        
@app.route("/projects/create", methods = ["GET", "POST"]) ## "GET" by default
def createproj():
    if (request.method == "GET"):
            return render_template("projects_create.html")
    elif (request.method == "POST" ):
        try: 
            Title = request.form['title']
            Description = request.form['desc']
            Startdate = request.form['sdat']
            Finishdate = request.form['fdat']
            Funding = request.form['fun']
            Org = request.form['org']
            Chief = request.form['resc']
            Evaluator = request.form['eval']
            Grade = request.form['grade']
            Evaldate = request.form['evdat']
            Prog = request.form['prog']
            Executive = request.form['exec']
            query = ("insert into project (Title, Description, Start_Date, Finish_Date, Funding_Amount, ID_Org, ID_Researcher_in_Charge, ID_Evaluator, Evaluation_Grade, Evaluation_Date, ID_Program, ID_Executive) values (NULLIF('%s',''), NULLIF('%s',''), '%s', '%s', NULLIF('%s',''), '%s', '%s', '%s', NULLIF('%s',''), '%s', '%s', '%s')" %(Title,Description,Startdate,Finishdate,Funding,Org,Chief,Evaluator,Grade,Evaldate,Prog,Executive))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)



@app.route('/organization_phone_numbers', methods=['GET', 'POST'])
def pho_num():
    if request.method == 'POST':
        ido = request.form['org']
        if (len(ido) == 0):
            msg = "You must fill the corresponding fields and then click submit button. Otherwise your action will not be submitted."
            return render_template("landing.html", msg = msg)
        ph = request.form['phone']
        if (len(ph) == 0):
            msg = "You must fill the corresponding fields and then click submit button. Otherwise your action will not be submitted."
            return render_template("landing.html", msg = msg)
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("DELETE FROM organization_phone_numbers WHERE ID_Org = (%s) and Phone_Number = (%s)", (ido,ph))
            mydb.commit()
            mycursor.close()
            return redirect(url_for("pho_num"))
        except mysql.connector.Error as err:
           msg = err.msg
           return render_template("landing.html", msg = msg)
    else:
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM organization_phone_numbers")
            column_names = [i[0] for i in mycursor.description]
            telephones = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('phone_numbers.html', telephones = telephones)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg) 
        
@app.route('/organization_phone_numbers/update/<int:orgID>', methods = ['GET', 'POST'])
def updatePhon(orgID):
    if (request.method == "GET"):
        query = f"select *FROM organization_phone_numbers WHERE ID_Org = {orgID};"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            column_names = [i[0] for i in mycursor.description]
            phones = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('phone_numbers_update.html', phones = phones)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        try: 
            oldphone = request.form['old']
            Phonenum = request.form['phone']
            query = (f"update organization_phone_numbers set ID_Org = {orgID}, Phone_Number = ('%s') WHERE (ID_Org = {orgID} and Phone_Number = ('%s'))" %(Phonenum,oldphone))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    
        
@app.route("/organization_phone_numbers/create", methods = ["GET", "POST"]) ## "GET" by default
def createorgpho():
    if (request.method == "GET"):
        return render_template('phone_numbers_create.html')
    elif (request.method == "POST" ):
        try: 
            org = request.form['orgs']
            Phonenum = request.form['phone']
            query = ("insert into organization_phone_numbers (ID_Org, Phone_Number) values (NULLIF('%s',''), NULLIF('%s',''))" %(org, Phonenum))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)


    
@app.route('/works', methods=['GET', 'POST'])
def works():
    if request.method == 'POST':
        idr = request.form['res']
        if (len(idr) == 0):
            msg = "You must fill the corresponding fields and then click submit button. Otherwise your action will not be submitted."
            return render_template("landing.html", msg = msg)
        idp = request.form['pr']
        if (len(idp) == 0):
            msg = "You must fill the corresponding fields and then click submit button. Otherwise your action will not be submitted."
            return render_template("landing.html", msg = msg)
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("DELETE FROM works WHERE ID_Project = (%s) and ID_Researcher = (%s)", (idp,idr))
            mydb.commit()
            mycursor.close()
            return redirect(url_for("works"))
        except mysql.connector.Error as err:
           msg = err.msg
           return render_template("landing.html", msg = msg)
    else:
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM works")
            column_names = [i[0] for i in mycursor.description]
            works = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('works.html', works = works)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg) 
        
@app.route('/works/update/<int:resID>', methods = ['GET', 'POST'])
def updateWork(resID):
    if (request.method == "GET"):
        query = f"select ID_Project from project where ID_org = (select ID_org from researcher where ID_Researcher = {resID});"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            column_names = [i[0] for i in mycursor.description]
            proj = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            query = f"select ID_Project from works where ID_Researcher = {resID};"
            mycursor.execute(query)
            column_names = [i[0] for i in mycursor.description]
            Oldproj = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('works_update.html', proj = proj, Oldproj = Oldproj)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        try: 
            oldproj = request.form['oldproj']
            proj = request.form['proj']
            query = ("update works set ID_Project = ('%s'), ID_Researcher = ('%s') where (ID_Project = ('%s') and ID_Researcher = ('%s'))" %(proj,str(resID),oldproj,str(resID)))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
        
@app.route("/works/create", methods = ["GET", "POST"]) ## "GET" by default
def creatework():
    if (request.method == "GET"):
            return render_template('works_create.html')
    elif (request.method == "POST" ):
        try: 
            proj = request.form['proj']
            resear = request.form['res']
            query = ("insert into works (ID_Project, ID_Researcher) values (NULLIF('%s',''), NULLIF('%s',''))" %(proj, resear))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
        
@app.route('/scientific_fields', methods=['GET', 'POST'])
def scif():
    if (request.method == "POST"):
        nn = request.form['name']
        if (len(nn) == 0):
            msg = "You must fill the corresponding fields and then click submit button. Otherwise your action will not be submitted."
            return render_template("landing.html", msg = msg)
        query = f"DELETE FROM scientific_field WHERE Name = '{nn}';"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("scif"))
        except mysql.connector.Error as err:
           msg = err.msg
           return render_template("landing.html", msg = msg)
    else:
        try:       
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM scientific_field")
            column_names = [i[0] for i in mycursor.description]
            fields = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('scientific_fields.html', fields = fields)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg) 
        
@app.route('/scientific_fields/update', methods = ['GET', 'POST'])
def updateScifi():
    if (request.method == "GET"):
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM scientific_field")
            column_names = [i[0] for i in mycursor.description]
            ff = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('scientific_fields_update.html', ff = ff)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        try: 
            oldname = request.form['oldname']
            Name = request.form['name']
            query = ("update scientific_field set Name = COALESCE(NULLIF(('%s'),''),Name) where Name = ('%s')" %(Name,oldname))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
        

@app.route("/scientific_fields/create", methods = ["GET", "POST"]) ## "GET" by default
def createscifi():
    if (request.method == "GET"):
            return render_template('scientific_fields_create.html')
    elif (request.method == "POST" ):
        try: 
            Name = request.form['name']
            query = ("insert into scientific_field (Name) values (NULLIF('%s',''))" %(Name))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)


@app.route('/project_fields', methods=['GET', 'POST'])
def prof():
    if request.method == 'POST':
        idpf = request.form['prf']
        if (len(idpf) == 0):
            msg = "You must fill the corresponding fields and then click submit button. Otherwise your action will not be submitted."
            return render_template("landing.html", msg = msg)
        nn = request.form['ff']
        if (len(nn) == 0):
            msg = "You must fill the corresponding fields and then click submit button. Otherwise your action will not be submitted."
            return render_template("landing.html", msg = msg)
       
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("DELETE FROM project_field WHERE ID_Project = (%s) and Field_Title = (%s)", (idpf,nn))
            mydb.commit()
            mycursor.close()
            return redirect(url_for("prof"))
        except mysql.connector.Error as err:
           msg = err.msg
           return render_template("landing.html", msg = msg)
    else:
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM project_field")
            column_names = [i[0] for i in mycursor.description]
            pfield = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('project_fields.html', pfield = pfield)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg) 
        
        
@app.route('/project_fields/update/<int:projID>', methods = ['GET', 'POST'])
def updateProf(projID):
    if (request.method == "GET"):
        query = f"select Field_Title from project_field where ID_Project = {projID};"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            column_names = [i[0] for i in mycursor.description]
            projf = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.execute("select *from scientific_field")
            column_names = [i[0] for i in mycursor.description]
            fields = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('project_fields_update.html', projf = projf, fields = fields)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        try:
            oldfield = request.form['oldft']
            fieldt = request.form['ft']
            query = ("update project_field set ID_Project = ('%s'), Field_Title = ('%s') where ID_Project = ('%s') and Field_Title = ('%s')" %(str(projID),fieldt,str(projID),oldfield))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
        
@app.route("/project_fields/create", methods = ["GET", "POST"]) ## "GET" by default
def createprojf():
    if (request.method == "GET"):
           try:
               mycursor = mydb.cursor()
               mycursor.execute("Use based")
               mycursor.execute("SELECT Name from scientific_field")
               column_names = [i[0] for i in mycursor.description]
               scifi = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
               mycursor.close()
               return render_template("project_fields_create.html", scifi = scifi)
           except mysql.connector.Error as err:
               msg = err.msg
               return render_template("landing.html", msg = msg)
    elif (request.method == "POST" ):
        try: 
            proj = request.form['proj']
            fieldt = request.form['ft']
            query = ("insert into project_field (ID_Project, Field_Title) values (NULLIF('%s',''), '%s')" %(proj, fieldt))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
        
        
@app.route('/deliverables', methods=['GET', 'POST'])
def deliv():
    if (request.method == "POST"):
        pr = request.form['proj']
        if (len(pr) == 0):
            msg = "You must fill the corresponding fields and then click submit button. Otherwise your action will not be submitted."
            return render_template("landing.html", msg = msg)
        title = request.form['title']
        if (len(title) == 0):
            msg = "You must fill the corresponding fields and then click submit button. Otherwise your action will not be submitted."
            return render_template("landing.html", msg = msg)
        query = f"DELETE FROM deliverable WHERE ID_Project = {pr} and Title = '{title}';"
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("deliv"))
        except mysql.connector.Error as err:
           msg = err.msg
           return render_template("landing.html", msg = msg)
    try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM deliverable")
            column_names = [i[0] for i in mycursor.description]
            deliverables = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('deliverables.html', deliverables = deliverables)
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg) 
        
        
@app.route('/deliverables/update/<int:projID>', methods = ['GET', 'POST'])
def updateDel(projID):
    if (request.method == "GET"):
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM deliverable where ID_Project = ('%s')" %(projID))
            column_names = [i[0] for i in mycursor.description]
            deliv = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('deliverables_update.html', deliv = deliv)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        try: 
            oldproj = projID
            oldtitle = request.form['oldtitle']
            proj = request.form['proj']
            title = request.form['title']
            Description = request.form['desc']
            Deldate = request.form['deld']
            query = ("update deliverable set ID_Project = COALESCE(NULLIF(('%s'),''),ID_Project), Title = COALESCE(NULLIF(('%s'),''),Title), Description = COALESCE(NULLIF(('%s'),''),Description), Delivery_Date = COALESCE(NULLIF(('%s'),''),Delivery_Date) where ID_Project = ('%s') and Title = ('%s')" %(proj, title, Description, Deldate,oldproj,oldtitle))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
                
        
@app.route("/deliverables/create", methods = ["GET", "POST"]) ## "GET" by default
def createdel():
    if (request.method == "GET"):
            return render_template('deliverables_create.html')
    elif (request.method == "POST" ):
        try: 
            proj = request.form['proj']
            title = request.form['title']
            Description = request.form['desc']
            Deldate = request.form['deld']
            query = ("insert into deliverable (ID_Project, Title, Description, Delivery_Date) values ('%s', NULLIF('%s',''), NULLIF('%s',''), '%s')" %(proj, title, Description, Deldate))
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute(query)
            mydb.commit()
            mycursor.close()
            return redirect(url_for("init"))
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
                
@app.route("/query1", methods = ["GET", "POST"])
def qu1():
    if (request.method == "GET"):
        try:
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM program")
            column_names = [i[0] for i in mycursor.description]
            programs = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            '''mycursor.execute("SELECT *FROM project")
            column_names = [i[0] for i in mycursor.description]
            projects = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]'''
            mycursor.close()
            return render_template('query1.html', programs = programs)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        a = 0
        sd = request.form['sd']
        ld = request.form['ld']
        if (len(sd) != 0 and len(ld) != 0):
            a += 1
        else:
            sd = 'b'
            ld = 'b'
        dauer = request.form['dauer']
        if len(dauer) != 0:
            a += 10
        else:
            dauer = 0
        execu = request.form['exec']
        if len(execu) != 0:
            a += 100
        else:
            execu = 0
        return redirect(url_for("qu1f", a = a, sd = sd, ld = ld, dauer = str(dauer), execu = str(execu)))
            
            
@app.route("/query1/<int:a>/<string:sd>/<string:ld>/<int:dauer>/<int:execu>", methods = ["GET", "POST"])
def qu1f(a, sd,ld,dauer,execu):     
    if (request.method == "GET"):   
        if (a == 0):
            msg = "You have to choose at least one criterion."
            return render_template("landing.html", msg = msg)
        elif (a == 1):
            try:
                mycursor = mydb.cursor()
                mycursor.execute("Use based")
                mycursor.execute("select *from project where (year(Start_date) >= (%s) and year(Start_Date) <= (%s))", (sd,ld))
                column_names = [i[0] for i in mycursor.description]
                projects = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
                return render_template("qu1.html", projects = projects)
            except mysql.connector.Error as err:
                msg = err.msg
                return render_template("landing.html", msg = msg)
        elif (a == 10):
            try:
                mycursor = mydb.cursor()
                mycursor.execute("Use based")
                mycursor.execute("SELECT *FROM project where Duration = ('%s')" %(dauer))
                column_names = [i[0] for i in mycursor.description]
                projects = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
                return render_template("qu1.html", projects = projects)
            except mysql.connector.Error as err:
                msg = err.msg
                return render_template("landing.html", msg = msg)
        elif (a == 100):
            try:
                mycursor = mydb.cursor()
                mycursor.execute("Use based")
                mycursor.execute("select *from project where ID_Executive = ('%s')" %(execu))
                column_names = [i[0] for i in mycursor.description]
                projects = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
                return render_template("qu1.html", projects = projects)
            except mysql.connector.Error as err:
                msg = err.msg
                return render_template("landing.html", msg = msg)
        elif (a == 11):
            try:
                mycursor = mydb.cursor()
                mycursor.execute("Use based")
                mycursor.execute("SELECT *FROM project where (Duration = ('%s') and (year(Start_date) >= ('%s') and year(Start_Date) <= ('%s')))" %(dauer,sd,ld) )
                column_names = [i[0] for i in mycursor.description]
                projects = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
                return render_template("qu1.html", projects = projects)
            except mysql.connector.Error as err:
                msg = err.msg
                return render_template("landing.html", msg = msg)
        elif (a == 101):
            try:
                mycursor = mydb.cursor()
                mycursor.execute("Use based")
                mycursor.execute("SELECT *FROM project where (ID_Executive = ('%s') and (year(Start_date) >= ('%s') and year(Start_Date) <= ('%s')))" %(execu,sd,ld))
                column_names = [i[0] for i in mycursor.description]
                projects = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
                return render_template("qu1.html", projects = projects)
            except mysql.connector.Error as err:
                msg = err.msg
                return render_template("landing.html", msg = msg)
        elif (a == 110):
            try:
                mycursor = mydb.cursor()
                mycursor.execute("Use based")
                mycursor.execute("SELECT *FROM project where (ID_Executive = ('%s') and Duration = ('%s'))" %(execu,dauer))
                column_names = [i[0] for i in mycursor.description]
                projects = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
                return render_template("qu1.html", projects = projects)
            except mysql.connector.Error as err:
                msg = err.msg
                return render_template("landing.html", msg = msg)
        elif (a == 111):
            try:
                mycursor = mydb.cursor()
                mycursor.execute("Use based")
                mycursor.execute("SELECT *FROM project where (ID_Executive = ('%s') and Duration = ('%s') and (year(Start_date) >= ('%s') and year(Start_Date) <= ('%s')))" %(execu,dauer,sd,ld))
                column_names = [i[0] for i in mycursor.description]
                projects = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
                return render_template("qu1.html", projects = projects)
            except mysql.connector.Error as err:
                msg = err.msg
                return render_template("landing.html", msg = msg)
    
@app.route("/qu1/<int:idd>", methods = ["GET"])
def qu1ff(idd) :
    try:
        mycursor = mydb.cursor()
        mycursor.execute("Use based")
        mycursor.execute("SELECT w.ID_Researcher, r.First_Name, r.Last_Name FROM works w inner join researcher r on r.ID_Researcher = w.ID_Researcher where w.ID_Project = ('%s')" %(idd))
        column_names = [i[0] for i in mycursor.description]
        qu1 = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
        mycursor.close()
        return render_template('qu1f.html', qu1 = qu1, ii = idd)
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg)
    

@app.route("/query21", methods = ["GET"])
def qu2f():
    try:
        mycursor = mydb.cursor()
        mycursor.execute("Use based")
        mycursor.execute("select *from researcher_projects")
        column_names = [i[0] for i in mycursor.description]
        qu2f = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
        mycursor.execute("select ID_Researcher, count(ID_Project) as Num from works group by ID_Researcher")
        column_names = [i[0] for i in mycursor.description]
        qu2fs = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
        mycursor.close()
        return render_template('qu2f.html', qu2f = qu2f, qu2fs = qu2fs)
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg)
    
@app.route("/query22", methods = ["GET"])
def qu2s():
    try:
        mycursor = mydb.cursor()
        mycursor.execute("Use based")
        mycursor.execute("select *from submissions")
        column_names = [i[0] for i in mycursor.description]
        qu2s = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
        mycursor.close()
        return render_template('qu2s.html', qu2s = qu2s)
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg)
    
@app.route("/query3", methods = ["GET", "POST"])
def qu3():
    if (request.method == "GET"):
        try:       
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("SELECT *FROM scientific_field")
            column_names = [i[0] for i in mycursor.description]
            fields = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('query3.html', fields = fields)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
    else:
        field = request.form['choice']
        return redirect(url_for("qu3f", field = field))
    
@app.route("/query3/<field>", methods = ["GET", "POST"])
def qu3f(field):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("select pf.Field_Title, p.ID_Project, p.Title, r.ID_Researcher, r.First_Name, r.Last_Name from project_field pf inner join project p on pf.ID_Project = p.ID_Project inner join works w on p.ID_Project = w.ID_Project inner join researcher r on w.ID_Researcher = r.ID_Researcher where (pf.Field_Title = %s and DATEDIFF(CURDATE(), r.Work_Start_Date) > 365 and DATEDIFF(CURDATE(), p.Start_Date) > 365 and DATEDIFF(CURDATE(), p.Finish_Date) < 0)", [field])
        column_names = [i[0] for i in mycursor.description]
        qu3 = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
        mycursor.close()
        return render_template('qu3.html', qu3 = qu3)
    except mysql.connector.Error as err:
        msg = err.msg
        return render_template("landing.html", msg = msg)
    
@app.route("/query4", methods = ["GET", "POST"])
def qu4f():
    if (request.method == "GET"):
        try:       
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("select k.ID as ID, o.Name as Name, k.year as year, k.Number as Num from (select n.ID as ID, n.year as year, n.Number as Number from (select ID_org as ID, year(Start_Date) as year, count(ID_Project) as Number from project group by ID_org, year(Start_Date)) n where (n.Number >= 10 and (n.ID,n.year+1,n.Number) in (select p.ID, p.year, p.Number from (select ID_org as ID, year(Start_Date) as year, count(ID_Project) as Number from project group by ID_org, year(Start_Date)) p))) k inner join organization o on o.ID_Org = ID ")
            column_names = [i[0] for i in mycursor.description]
            qu4 = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('qu4.html', qu4 = qu4)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)    
            
@app.route("/query5", methods = ["GET", "POST"])
def qu5f():
    if (request.method == "GET"):
        try:       
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("select sf1.Name as name1, sf2.Name as name2, count(pf.ID_Project) as number_of_projects from scientific_field sf1 inner join scientific_field sf2 on sf1.Name <> sf2.Name and sf1.Name < sf2.Name join project_field pf on pf.Field_Title = sf1.Name where (pf.ID_Project, sf2.Name) in (select ID_Project, Field_Title from project_field) group by sf1.Name, sf2.Name order by number_of_projects DESC  limit 3")
            column_names = [i[0] for i in mycursor.description]
            qu5 = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('qu5.html', qu5 = qu5)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)    

@app.route("/query6", methods = ["GET", "POST"])
def qu6f():
    if (request.method == "GET"):
        try:       
            mycursor = mydb.cursor()
            mycursor.execute("Use based")
            mycursor.execute("select r.ID_Researcher, r.First_Name, r.Last_Name, TIMESTAMPDIFF(year, r.Birth_Date, CURDATE()) as Age, count(w.ID_Project) as Number_of_Active_Projects from researcher r inner join works w on r.ID_Researcher = w.ID_Researcher inner join project p on w.ID_Project = p.ID_Project where DATEDIFF(CURDATE(), p.Finish_Date) < 0  group by r.ID_Researcher having Age < 40 order by Number_of_Active_Projects DESC LIMIT 10")
            column_names = [i[0] for i in mycursor.description]
            qu6 = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
            mycursor.close()
            return render_template('qu6.html', qu6 = qu6)
        except mysql.connector.Error as err:
            msg = err.msg
            return render_template("landing.html", msg = msg)
        
@app.route("/query7", methods = ["GET", "POST"])
def qu7f():
     if (request.method == "GET"):
         try:       
             mycursor = mydb.cursor()
             mycursor.execute("Use based")
             mycursor.execute("select e.First_Name, e.Last_Name, o.Name, p.Funding_Amount from executive e inner join project p on e.ID_Executive = p.ID_Executive inner join organization o on p.ID_org = o.ID_Org where o.Category = 'Company' order by p.Funding_Amount DESC limit 5")
             column_names = [i[0] for i in mycursor.description]
             qu7 = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
             mycursor.close()
             return render_template('qu7.html', qu7 = qu7)
         except mysql.connector.Error as err:
             msg = err.msg
             return render_template("landing.html", msg = msg)       
        
    #and DATEDIFF(CURDATE(), p.Finish_Date) < 0

@app.route("/query8", methods = ["GET", "POST"])
def qu8f():
     if (request.method == "GET"):
         try:       
             mycursor = mydb.cursor()
             mycursor.execute("Use based")
             mycursor.execute("select r.ID_Researcher, r.First_Name, r.Last_Name, count(p.ID_Project) as Number_of_Projects_without_Submissions from researcher r inner join works w on r.ID_Researcher = w.ID_Researcher inner join project p on w.ID_Project = p.ID_Project where p.ID_Project not in (select ID_Project from deliverable) group by r.ID_Researcher having Number_of_Projects_without_Submissions > 4")
             column_names = [i[0] for i in mycursor.description]
             qu8 = [dict(zip(column_names, entry)) for entry in mycursor.fetchall()]
             mycursor.close()
             return render_template('qu8.html', qu8 = qu8)
         except mysql.connector.Error as err:
             msg = err.msg
             return render_template("landing.html", msg = msg)       
        






