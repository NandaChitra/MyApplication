from flask import Flask, redirect, render_template, flash, url_for
from flask import request, session
from flask_session import Session
import mysql.connector as mysql

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def MyhomeRoot():
    return render_template('MyLogin.html')

@app.route("/My_Login_Process", methods=['POST'])
def My_Login_Process():
    uid = request.form["username"]
    pwd = request.form["password"]
    try:
        db_connect = mysql.connect(
            host="localhost", database="mydatabase", user="root", passwd="admin", use_pure=True)
        sql = "Select username, password From mypassword where username = " + "'" + uid + "'"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cno = mycursor.fetchall()
        res = [tuple(str(item) for item in t) for t in cno]
        #print(res)
    except Exception as err:
        print(err)
        return render_template('MyError.html')
    if len(res) == 0:
        status = 0
        return render_template('MyError.html')
    else:
        usrid  = res[0][0]
        passwd = res[0][1]
        if (usrid == uid and pwd == passwd):
            return render_template('MyHome.html', usrid=usrid)
        else:
            """status = 0"""
            return render_template('MyError.html')

@app.route("/ViewStudent")
def ViewStudent():
    try:
        db_connect = mysql.connect(
            host="localhost", database="mydatabase", user="root", passwd="admin", use_pure=True)
        sql = "Select USN, Name, Phone, Marks From student"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cdata = mycursor.fetchall()
        return render_template("ShowStudent.html", cdata=cdata)
    except Exception as err:
        print(err)
        return render_template('MyError.html')

@app.route("/AddStudent", methods=['POST'])
def AddStudent():
    try:
        usn = request.form["usn"]
        name = request.form["name"]
        phone = request.form["phone"]
        db_connect = mysql.connect(
            host="localhost", database="mydatabase", user="root", passwd="admin", use_pure=True)
        sql = "INSERT INTO Student(USN,Name,Phone) VALUES (" + "'" + usn + "'" + "," + "'" + name +"'" + "," + "'"+phone+"'" + ")" 
        #print(sql)
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        db_connect.commit()
        return render_template("MyHome.html")
    except Exception as err:
        print(err)
        return render_template('MyError.html')

@app.route("/SaveStudentMarks", methods=['POST'])
def SaveStudentMarks():
    try:
        user_USN = request.form["userUSN"]
        user_mks  = request.form["userMarks"]
        
        print(user_USN)
        print(user_mks)
        db_connect = mysql.connect(
            host="localhost", database="mydatabase", user="root", passwd="admin", use_pure=True)
        sql_std = "UPDATE Student SET Marks = " + user_mks +" WHERE USN = " + "'" + user_USN + "'"
        print(sql_std)
        mycursor = db_connect.cursor()
        mycursor.execute(sql_std)
        db_connect.commit()

        sql = "Select USN, Name, Phone, Marks From student"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cdata = mycursor.fetchall()
        return render_template("EnterMarks.html", cdata=cdata)
    except Exception as err:
        print(err)
        return render_template('MyError.html')

@app.route("/MarksData")
def MarksData():
    try:
        db_connect = mysql.connect(
            host="localhost", database="mydatabase", user="root", passwd="admin", use_pure=True)
        sql_std = "Select USN, Name, Phone, Marks From student"
        mycursor = db_connect.cursor()
        mycursor.execute(sql_std)
        cdata = mycursor.fetchall()
        return render_template("EnterMarks.html", cdata=cdata)
    except Exception as err:
        print(err)
        return render_template('Error.html')
        
@app.route("/MyHome")
def MyHome():
    return render_template("MyHome.html")

@app.route("/MyError")
def MyError():
    return render_template("MyError.html")

@app.route("/InsertStudent")
def InsertStudent():
    return render_template("NewStudent.html")



@app.route("/Edit")
def Edit():
    return render_template("Edit.html")


if __name__ == '__main__':
    app.run()