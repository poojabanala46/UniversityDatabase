from flask import Flask, render_template, request, redirect, url_for
import mysql.connector


app = Flask(__name__)

c = mysql.connector.connect(
host = "localhost",
user = "root",
database = "project",
passwd = "********"
)

a = c.cursor()


@app.route('/')
def login():
    return render_template('login.html') 
 

@app.route('/course',methods=['GET', 'POST'])
def course():
    
    if request.method == "POST":
        global id
        id = request.form['username']
        pwd = request.form['password']
        print(id)
        a.execute('''SELECT S_Name FROM project.student_info WHERE Student_ID=%s AND pwd=%s''', (id, pwd,))
        d = a.fetchall()
        
        if(d):
            return render_template('course.html', username=d)
        else: 
            msg = "wrong credentials"
            return render_template('login.html', msg=msg)
            
            
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        global CCode
        CCode = request.form['CCode']
        a.execute('''SELECT s.SNo, s.CName, s.CCode, count(s.SNo) as studentcount ,s.Max_Enrollment,s.S_SSN,s.Lecture_Schedule,S.Weekdays FROM project.section s , project.register r WHERE r.CCode=%s AND s.CCode=r.CCode AND s.SNo = r.SNo GROUP BY s.SNo''',(CCode,))
        e = a.fetchall()
        msg = ""
        if e:
            return render_template('home.html', courseDetails=e)
        else:
            msg = "Invalid Course ID or Table is Empty"
            print("wrong")
            return render_template('course.html', msg=msg)


@app.route('/rform',methods=['GET','POST']) 
def rform():
    print(CCode,"username")
    print("id values in register page", id, CCode)
    return render_template('rform.html', id=id, CCode=CCode)


@app.route('/register', methods=['POST'])
def register():
    print("Enter please")
    SNo = request.form['sno']
    cname = request.form['cname']
    a.execute('''SELECT count(CCode) as C FROM project.register WHERE Student_ID= %s''', (id,))
    f = a.fetchall()
    y= str(f)
    x= int(y[2])
    print("id values", id, CCode)
    if x < 4:
        a.execute("insert into project.register values (%s,%s,%s,%s)", (id, SNo, CCode, cname))
        c.commit()
        return "successfully registered"
    else:
        msg = "Invalid input"
        return render_template('rform.html', msg)
    

@app.route('/classlist/<sid>/<code>', methods=['GET', 'POST'])
def classlist(sid, code):
    a.execute("SELECT h.CCode,h.SNo,r.cname,h.Lecture_Schedule,h.BCode,h.Room_NO,h.Weekdays,h.S_SSN,s.Student_ID,s.S_Name,s.Major,s.CLASS_Year FROM project.held h,project.student_info s,project.register r WHERE h.CCode=%s AND h.SNo= %s AND h.CCode=r.CCode AND h.SNo=r.SNo AND r.Student_ID=s.Student_ID order by s.S_Name;", (code, sid))
    det = a.fetchall()
    return render_template('classlist.html', det = det)
