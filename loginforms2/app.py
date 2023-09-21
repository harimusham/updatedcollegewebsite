import sqlite3
from flask import Flask,render_template,request, redirect, url_for
from datetime import date


app = Flask(__name__)


# Global variables
mark_list = []



@app.route('/insertf-data', methods=['POST','GET'])
def insert_data():
    if request.method == 'POST':
        facid=request.form.get('facid')
        fusername=request.form.get('fusername')
        fpassword=request.form.get('fpassword')
        fnames = request.form.get('fname')
        fdepartment = request.form.get('fdepartment')
        fdesignation=request.form.get('fdesignation')
        fmobile=request.form.get('fmobilenumber')
        femail=request.form.get('femail')
        fspecification=request.form.get('fspecification')
        faddress=request.form.get('faddress')
        conn = sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Facultyss(facid,fusername,fpassword,fname, fdepartment,fdesignation,fmobile,femail,fspecification,faddress) VALUES (?,?,?,?,?,?,?,?,?,?)', (facid,fusername,fpassword,fnames,fdepartment,fdesignation,fmobile,femail,fspecification,faddress))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('facultydetails.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('logins.html')

@app.route("/faculty-login", methods=["POST"])
def flogin():
    if  request.method == 'POST':
        fusername = request.form.get('fusername')
        fpassword = request.form.get("fpassword")
        connection = sqlite3.connect('logins2.db')
        cursor = connection.cursor()
    
        print(fusername, fpassword)
        # Use parameterized query to prevent SQL injection
        query = "SELECT facid, fname, fusername, fpassword FROM Facultyss WHERE fusername = ? AND fpassword = ?"
        cursor.execute(query, (fusername, fpassword))
        results = cursor.fetchall()
        cursor.close()
        print(results)
        if len(results) == 0:
            error_message = "Invalid Fusername or Password"  # Set an error message
            return render_template('logins.html', error_message=error_message)  # Pass the message to the template
        else:
        # return render_template('welcomefact.html',fname=results[0][1], name=results[0][2], facid=results[0][0])
            return redirect(url_for('getprofile',fname=results[0][1], name=results[0][2], facid=results[0][0]))
    return redirect(url_for('login'))
    
@app.route("/getprofile")
def getprofile():
    fname = request.args.get("fname")
    name = request.args.get("name")
    facid = request.args.get("facid")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    # Use parameterized query to prevent SQL injection
    query = f"SELECT * FROM Facultyss WHERE facid={facid}"
    cursor.execute(query)
    results = cursor.fetchone()
    cursor.close()
    return render_template('welcomefact.html', name=name,facid=facid, fname=fname,  is_profile=True, profileresults=results)

@app.route('/inserts-data', methods=['POST','GET'])
def insertsData():
    if request.method == 'POST':
        sid=request.form.get('sid')
        username=request.form.get('susername')
        password=request.form.get('spassword')
        name = request.form.get('sname')
        fathername = request.form.get('sfathername')
        mothername=request.form.get('smothername')
        mobilenumber=request.form.get('smobilenumber')
        pmobilenumber=request.form.get('pmobilenumber')
        dob=request.form.get('dob')
        gender=request.form.get('gender')
        email=request.form.get('semail')
        course=request.form.get('scourse')
        sscmarks=request.form.get('sscmarks')
        intermarks=request.form.get('sintermarks')
        aadharnumber=request.form.get('saadharnumber')
        address=request.form.get('address')
        city=request.form.get('city')
        state=request.form.get('state')
        country=request.form.get('country')
        registrationapproved=request.form.get('regapproved')
        conn = sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Studentss(sid,username,password,name,fathername,mothername,mobilenumber,pmobilenumber,dob,gender,email,course,sscmarks,intermarks, aadharnumber,address,city,state,country,registrationapproved) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (sid,username,password,name,fathername,mothername,mobilenumber,pmobilenumber,dob,gender,email,course,sscmarks,intermarks,aadharnumber,address,city,state,country,registrationapproved))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('studentdetails.html')

@app.route('/student-login',methods=['POST'])
def stulogin():
    if  request.method == 'POST':
        username=request.form.get("susername")
        password=request.form.get("spassword")
        connection=sqlite3.connect('logins2.db')
        cursor=connection.cursor()
        print(username,password)
        query = "SELECT *  FROM Studentss WHERE username = ? AND password = ?"
        # query="SELECT username,password FROM students where  username="+username+" password="+password+";"
        cursor.execute(query, (username, password))
        results=cursor.fetchall()
        cursor.close()
        if(len(results)==0):
            serror_message = "Invalid Susername or Password"  # Set an error message
            return render_template('logins.html', serror_message=serror_message)
        else:
            return redirect(url_for('spdisplay', sid=results[0][0],suser=results[0][1]))
            # return render_template('welcomestudent.html',student=results[0])
    return redirect(url_for('login'))

@app.route("/spdisplay")
def spdisplay():
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    cursor.close()
    if(len(results)==0):
        error_message = "Invalid Username or Password"  # Set an error message
        return render_template('logins.html', error_message=error_message)
    else:
        return render_template('welcomestudent.html',student=results[0], is_profile=True)

@app.route("/smdisplay")
def smdisplay():
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    query = "SELECT * FROM Markss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    marks = cursor.fetchall()
    cursor.close()
    if(len(results)==0):
        print("please provide valid login details")
    else:
        return render_template('welcomestudent.html',student=results[0], is_marks=True, marks=marks)
    
@app.route("/sadisplay")
def sadisplay():
    susername=request.args.get("suser")
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    cursor.close()
    if(len(results)==0):
        print("please provide valid login details")
    else:
        return render_template('welcomestudent.html',student=results[0], is_attendance=True,susername=susername)


@app.route("/sndisplay")
def sndisplay():
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    query = "SELECT * FROM notes"
    cursor.execute(query)
    notes = cursor.fetchall()
    cursor.close()
    if(len(results)==0):
        print("please provide valid login details")
    else:
        return render_template('welcomestudent.html',student=results[0], is_notes=True, notes=notes)

@app.route("/scdisplay")
def scdisplay():
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db',timeout=30)
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    query = "SELECT * FROM jobborad"
    cursor.execute(query)
    jobs = cursor.fetchall()
    cursor.close()
    if(len(results)==0):
        print("please provide valid login details")
    else:
        return render_template('welcomestudent.html',student=results[0], is_career=True, jobs=jobs)


@app.route('/f-addmarks',methods=['GET','POST'])
def faddmarks():
    fname = request.args.get("fname")
    name = request.args.get("name")
    facid = request.args.get("facid")
    if request.method=="POST":
        sid=request.form.get('sid')
        syear=request.form.get('syear')
        mlinternal=request.form.get('mlint')
        mlexternal=request.form.get('mlext')
        mltotal=request.form.get('mltotal')
        mlgrade=request.form.get('mlgrade')
        cdinternal=request.form.get('cdint')
        cdexternal=request.form.get('cdext')
        cdtotal=request.form.get('cdtotal')
        cdgrade=request.form.get('cdgrade')
        slinternal=request.form.get('slint')
        slexternal=request.form.get('slext')
        sltotal=request.form.get('sltotal')
        slgrade=request.form.get('slgrade')
        dppminternal=request.form.get('dppmint')
        dppmexternal=request.form.get('dppmext')
        dppmtotal=request.form.get('dppmtotal')
        dppmgrade=request.form.get('dppmgrade')
        cgpa=request.form.get('cgpa')
        gpa=request.form.get('gpa')
        conn=sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Markss(sid,semister,mlinternal,mlexternal,mltotal,mlgrade,cdinternal,cdexternal,cdtotal,cdgrade,slinternal,slexternal,sltotal,slgrade,dppminternal,dppmexternal,dppmtotal,dppmgrade,cgpa,gpa) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(sid,syear,mlinternal,mlexternal,mltotal,mlgrade,cdinternal,cdexternal,cdtotal,cdgrade,slinternal,slexternal,sltotal,slgrade,dppminternal,dppmexternal,dppmtotal,dppmgrade,cgpa,gpa))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('welcomefact.html', fname=fname, name=name,facid=facid, add_marks=True)
    # return render_template('faddmarks.html')

@app.route('/getmarks',methods=['GET','POST'])
def getmarks():
    fname = request.args.get("fname")
    if request.method=="POST":
        sid=request.form.get("sid")
        conn=sqlite3.connect('logins2.db')
        cursor=conn.cursor()
        query="select * from Markss where sid="+sid+";"
        cursor.execute(query)
        results=cursor.fetchall()   
        conn.commit()
        cursor.close()
        conn.close()
        print(list[results])
        if(len(results)==0):
            print("invalid number provided ")
        else:
            return render_template('displaymarks.html', fname=fname, sid=sid, results=results)
    return render_template('getmarks.html')



@app.route("/add_attendance", methods=["GET", "POST"])
def add_attendance():
    global mark_list
    today = date.today()
    def total_days():
        start_date = date(2023, 9, 7)
        return int((today-start_date).days)
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    # Use parameterized query to prevent SQL injection
    query = "SELECT sid, attendance, name FROM Studentss"
    cursor.execute(query)
    students = cursor.fetchall()
    if request.method=="POST":
        for student in students:
            is_present = request.form.get(str(student[0]))
            
            no_of_days_present = (student[1] * (total_days()-1)) / 100
            if is_present=="1":
                no_of_days_present += 1
            new_attendance = int((no_of_days_present / total_days())*100)
            
            query = "UPDATE Studentss SET attendance=? WHERE sid=?"
            cursor.execute(query, (new_attendance, student[0]))
            connection.commit()
            mark_list.append(today)
    cursor.close()
    connection.close()
    if date.today() in mark_list:
        is_completed = True
    else:
        is_completed = False
            
    return render_template("add_attendance.html", students=students, is_completed=is_completed, today=today)


 
@app.route("/add_notes",methods=["GET","POST"])
def add_notes():
    fname = request.args.get("fname")
    name = request.args.get('name')
    facid = request.args.get("facid")
    if request.method=="POST":
        facname=request.form.get('facname')
        subcode=request.form.get('subcode')
        subname=request.form.get('subname')
        sublink=request.form.get('sublink')
        conn=sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes(facname,subcode,subname,sublink) values(?,?,?,?)',(facname,subcode,subname,sublink))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('welcomefact.html',add_notes=True, name=name, fname=fname, facid=facid)
 
@app.route('/add_jobs',methods=["GET","POST"], endpoint='add_jobs')
def addjobs():
    name = request.args.get("name")
    facid = request.args.get("facid")
    fname=request.args.get('fname')
    if request.method=="POST":
        companyname=request.form.get('companyname')  
        email=request.form.get('email')
        jobposition=request.form.get('jobposition')
        location=request.form.get('location')
        requriments=request.form.get('requriments')
        url=request.form.get('url')
        conn = sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO jobborad(Company_Name,email,JOB_POSITION,location,Requriments,url) VALUES (?,?,?,?,?,?)', (companyname,email,jobposition,location,requriments,url))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('welcomefact.html',add_jobs=True,fname=fname, name=name, facid=facid)
@app.route('/insert_parentdata',methods=["GET","POST"])
def insertpdata():
    if request.method=="POST":
        pid=request.form.get('pid')
        pusername=request.form.get('pusername')
        ppassword=request.form.get('ppassword')
        ssid=request.form.get('ssid')
        conn=sqlite3.connect('logins2.db')
        cursor=conn.cursor()
        cursor.execute('INSERT INTO parents(pid,pusername,ppassword,STUID) VALUES (?,?,?,?)', (pid,pusername,ppassword,ssid))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('insertparentdetails.html')

@app.route('/p_login',methods=['GET','POST'])
def plogin():
    if  request.method == 'POST':
        pusername=request.form.get('pusername')
        ppassword=request.form.get("ppassword")
        connection=sqlite3.connect('logins2.db')
        cursor=connection.cursor()
        print(pusername,ppassword)
        query = "SELECT * FROM parents WHERE pusername = ? AND ppassword = ?"
        # query="SELECT username,password FROM students where  username="+username+" password="+password+";"
        cursor.execute(query, (pusername, ppassword))
        results=cursor.fetchall()
        if(len(results)==0):
            perror_message = "Invalid Pusername or Password"  # Set an error message
            return render_template('logins.html', perror_message=perror_message)
        else:
            return redirect(url_for('ppdisplay', pid=results[0][0],pusername=pusername,stuid=results[0][3]))
            # return render_template('welcomeparent.html',pid=results[0][0],pusername=pusername,results=results[0],stuid=results[0][3])
    return redirect(url_for('login'))
       
    
@app.route("/ppdisplay")
def ppdisplay():
    stuid = request.args.get("stuid")
    pusername = request.args.get("pusername")
    conn = sqlite3.connect('logins2.db')
    cursor = conn.cursor()
    query = "SELECT * from Studentss WHERE sid = ?"
    cursor.execute(query, (stuid, ))
    results = cursor.fetchall()
    print(results)
    if(len(results)==0):
        print("No results please try again")
    else:
        return render_template('welcomeparent.html', stuid=stuid, results = results[0], is_profile=True, pusername=pusername)

@app.route('/pmdisplay')
def pmdisplay():
    pid = request.args.get("pid")
    stuid=request.args.get("stuid")
    pusername=request.args.get("pusername")
    # pusername=request.form.get('pusername')
    # stuid=request.form.get('stuid')
    # pid=request.form.get('pid')
    conn=sqlite3.connect('logins2.db')
    cursor = conn.cursor()
    query = "SELECT * From  Markss WHERE sid = ?"
    cursor.execute(query,(stuid,))
    results=cursor.fetchall()
    print(results)
    if(len(results)==0):
        print("no results please try again")
    else:
        return render_template('welcomeparent.html',stuid=stuid,pid=pid,results=results[0],pusername=pusername,is_smarks=True)
    
   
@app.route("/padisplay")
def padisplay():
    stuid = request.args.get("stuid")
    pusername=request.args.get("pusername")
    conn=sqlite3.connect('logins2.db')
    cursor = conn.cursor()
    query = "SELECT sid, attendance FROM Studentss WHERE sid = ?"
    cursor.execute(query,(stuid,))
    results=cursor.fetchall()
    if(len(results)==0):
        print("No results please try again")
    else:
        return render_template('welcomeparent.html', stuid=stuid, results = results[0], is_attendance=True, pusername=pusername)
 


if __name__ == '__main__':
    app.run(debug=True)