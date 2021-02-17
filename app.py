# from flask import Flask,render_template,request
# from flask_wtf,file import FileField
import cv2
from time import sleep
import os
import random
import logging
from flask_socketio import SocketIO, send,emit
from flask import *
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# from chatterbot.trainers import ListTrainer
from flask_mail import Mail,Message
from werkzeug.utils import secure_filename
def Content():
    TOPIC_DICT = {"Basics":[["Introduction to Python","/introduction-to-python-programming/"],
                            ["Print functions and Strings","/python-tutorial-print-function-strings/"],
                            ["Math basics with Python 3","/math-basics-python-3-beginner-tutorial/"]],
                  "Web Dev":[]}

    return TOPIC_DICT
TOPIC_DICT=Content()
print(__file__)
import os
import sqlite3

project_dir=os.path.dirname(os.path.abspath(__file__))
myApp=Flask(__name__)

#///////////////////////chat bot confuration

# //////////////Email configuration
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'ah.schoolsmail@gmail.com',
    "MAIL_PASSWORD": 'Networks1.'
}
myApp.config.update(mail_settings)
mail=Mail(myApp)
# /////////////////////////////
print(project_dir)
myApp.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( myApp )
from flask_sqlalchemy import SQLAlchemy
TOPIC_DICT=Content
project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir,"SchoolDb.db"))
myApp.config["SQLALCHEMY_DATABASE_URI"] = database_file
myApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(myApp)
# db.create_all()
# exit()
userLoginName=''
idNum=0

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40),unique=True, nullable=False, primary_key = False)
    email = db.Column(db.String(40),unique=False, nullable=False)
    phone=db.Column(db.String(40),unique=False,nullable=True)
    picture=db.Column(db.String(40),unique=False,nullable=True)

    # picture=db.Column(db.String(40),unique=False,nullable=True)
    password = db.Column(db.String(40),unique=False, nullable=False)
# db.create_all()
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role=db.Column(db.String(40),nullable=False,primary_key=False)
    userName=db.Column(db.String(40),unique=True,nullable=False,primary_key=False)
    pasword=db.Column(db.String(40),unique=False,nullable=False)
    email=db.Column(db.String(40),unique=False,nullable=False)
    picture=db.Column(db.String(40),unique=False,nullable=True)
    phone=db.Column(db.String(40),unique=False,nullable=True)
    stdClass=db.Column(db.String(40),unique=False,nullable=True)
    
class SliderPic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic1 = db.Column(db.String(40), nullable=True, primary_key=False)
    pic2 = db.Column(db.String(40), nullable=True, primary_key=False)
    pic3 = db.Column(db.String(40), nullable=True, primary_key=False)
    


# bot = ChatBot("Abdul Aziz")
# trainer = ListTrainer(bot)
# trainer.train(['What is your name?', 'My name is aziz'])
# english_bot = ChatBot("Welcome To A-H Schools", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("chatterbot.corpus.english")

# # def addChat(chating):
# str1="which school"
# str2="ntu"
# bot = ChatBot("Abdul Aziz")
# trainer = ListTrainer(bot)
# trainer.train([str1, str2])     
# # english_bot = ChatBot("Welcome To A-H Schools", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# # trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("chatterbot.corpus.english")


# db.create_all()
# 
app.secret_key = 'super secret key'

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json )

# @myApp.route("/get")
# def get_bot_response():
#     userText = request.args.get('msg')
#     return str(english_bot.get_response(userText))


# @myApp.route("/chatbot")
# def chattingbot():
#     return render_template("chat.html")

@myApp.route('/chat',methods=["POST","GET"])
def chat():
    return render_template("mssage.html")

@myApp.route('/registration')
def reg():
    return render_template("dynamicForm.html")

@myApp.route('/adminLogin')
def adminLogin():
    return render_template("login.html")

@myApp.route('/sidea')
def adm():

    return render_template("adminSideNav.html")

@myApp.route('/')
def myHome():

    return render_template("mainHome.html")


@myApp.route('/register',methods=["POST","GET"])
def register():
    UserReg1 = admin()
    UserReg1.name=request.form['nameReg']
    userName = UserReg1.name
    userName = userName.replace(" ", "")
    UserReg1.name = userName
    UserReg1.email = request.form['emailReg']
    UserReg1.password = request.form['passReg']
    # confirmPass=request.form['confirmReg']
    db.session.add(UserReg1)
    db.session.commit()
    return render_template("login.html")


@myApp.route('/userLogin')
def userLoginPoint():
    return render_template("loginUser.html")

@myApp.route('/loginUserOK',methods=["GET","POST"])
def loginUserOK2():
    # loginUser = user()
    if request.method == "POST":

        try:
            user1 = request.form['userLogin1']
            userLoginName = user1
            userFound = user.query.filter_by(userName=user1).first()
            userPass = request.form['passLogin1']
            userRole=request.form['roleUser']
            try:
                # if (userRole=="Student"):
                if user1 == userFound.userName:
                    print("found")
                    if userRole==userFound.role=="Student":
                        if userFound.userName == user1 and userPass == userFound.pasword:
                            # if userRole=="Student":
                            print("Studnet")
                            return render_template('OnlyForStudent.html', data={userFound})
                        else:
                            return render_template("loginUser.html", login=">>Invalid Password")
                    elif userRole==userFound.role=="Teacher":    # break:
                        print("Teacher")
                        return render_template('OnlyForTeacher.html', data={userFound})
                    else:
                        return render_template("loginUser.html",clr="rgb(70, 127, 202)" ,login="Please Select Correct Role" ,loginT2="Verify Your UserName,Password")
                            
                        # elif userFound.userName == user1 and userPass == userFound.pasword and userRole=="Teacher":
                        #     return render_template('OnlyForTeacher.html', data={userFound})
                else:
                    return render_template("loginUser.html", login=">>Not a member please Sign_up")

# 237417
            except:
                return render_template("loginUser.html", login=">>Invalid UserName")

        except OSError as error:
            print(error)
            print("exception")
            return render_template("loginUser.html", login=">>Not a member please Contact Admin")

@myApp.route('/logoutTO')
def logOut():
    return render_template("mainHome.html")


myUserName=''

@myApp.route('/loginOK',methods=["POST","GET"])
def login():
    if request.method == "POST":
        loginUser=admin()
        # vid=Video()
        try:
            user = request.form['userLogin']
            userLoginName=user
            userFound = admin.query.filter_by(name=user).first()
            userPass=request.form['passLogin']
            try:
                if user==userFound.name:
                    print("found")
                    if userFound.name == user and userPass == userFound.password:

                        myUserName=userFound.name

                        return render_template('adminSideNav.html' ,adminLogin=myUserName)
                    else:
                        return render_template("login.html", login=">>Not a member please Sign_up")
            except:
                return render_template("login.html", login=">>Invalid UserName")
        except OSError as error:
            print(error)
            print("exception")
            return render_template("login.html",login=">>Not a member please Sign_up")

@myApp.route('/showUser')
def showUser():
    return render_template("secondPage.html")

@myApp.route('/adminAllOption')
def adminPanal():
    return render_template("mainHome.html")

@myApp.route('/form')
def add1User():
    return render_template("form.html")

name='asdasd'

@myApp.route('/student')
def showStudent():

    userFound=user.query.filter_by(role="Student")
    return render_template("student.html",data=userFound)

@myApp.route('/studentOnly')
def showStudent1():
    r=db.engine.execute("select userName,email,phone,role,email,picture from user where role Like \'Student\'")
    userFound=user.query.filter_by(role="Student")
    return render_template("studentOnly.html",data=userFound)

@myApp.route('/teacher')
def showTeacher():
    userFound=user.query.filter_by(role="Teacher")
    return render_template("teacher.html",data=userFound)

@myApp.route('/addUser',methods=["GET","POST"])
def addUser():

    try:
         if request.method=="POST":
            user1=user()
            user1.userName=request.form['name']
            name=user1.userName
            name=name.replace(" ","")
            user1.userName=name
            user1.email=request.form['email']
            user1.phone=request.form['phone']
            user1.role=request.form['role']
            user1.pasword=random.randint(1001,1000000)
            # files save kerne kac ode

            folderName = os.path.dirname(os.path.abspath(__file__)) + '//static'
            filename = secure_filename( request.files['file'].filename)
            request.files['file'].save(os.path.join(folderName, filename))
            user1.picture=filename
            print(user1.picture)
            userName1 = user1.userName
            # userName1 = userName1.replace(" ", "")
            user1.userName = userName1
            msg = Message(subject="Welcome To Ah-Schools",
                          sender="ah.schoolsmail@gmail.com",
                          recipients=[user1.email],  # replace with your email for testing
                          body="Your userName :"+user1.userName+"\n Your Password :"+str(user1.pasword)+"\n \n Please Use these Credential to login to your User Account \n\n Thanku!\n\nFollow https://ah-schools.herokuapp.com/userLogin to Login"
                          )
            mail.send(msg)
            db.session.add(user1)
            db.session.commit()
            print(request.form.get('email'))
            print(request.form.get('name'))
            getUser = user.query.all()
            getUserName = admin.query.all()
            return render_template('adminSideNav.html',users=getUser,login='abdul')


    except OSError as error:
        print(error)
        print("exception")


@myApp.route('/users')
def showAllUser():
    getUser = user.query.all()
    return render_template('adminSideNav.html',users=getUser,adminLogin=myUserName)


@myApp.route('/searchStd',methods=["POST"])
def searchUser():
    user1=request.form['searchStd']
    try:
        userFound = user.query.filter_by(email=user1).first()
        myUser = user.query.filter_by(role="Student")
        if userFound.role=='Student':
            return render_template('student.html', data={userFound})
    except:
        return render_template('student.html', data=myUser,err="error", found="Not Found")

@myApp.route('/searchTeacher',methods=["POST"])
def searchTeacher():
    user1=request.form['searchTeacher']
    try:
        userFound = user.query.filter_by(email=user1).first()
        myUser = user.query.filter_by(role="Teacher")
        if userFound.role=='Teacher':
            return render_template('teacher.html', data={userFound})
    except:
        return render_template('teacher.html', data=myUser,err="error", found="Not Found")

@myApp.route('/deleteStudent',methods=["POST"])
def DeleteUser():

    userName1=request.form['target_user']
    userFound=user.query.filter_by(userName=userName1).first()
    db.session.delete(userFound)
    db.session.commit()
    myUser=user.query.all()

    userFound = user.query.filter_by(role="Student")
    return render_template("student.html", data=userFound)

    print("delete")
@myApp.route('/deleteTeacher',methods=["POST"])
def DeleteUserStd():
     userName1=request.form['target_user']
     userFound=user.query.filter_by(userName=userName1).first()
     db.session.delete(userFound)
     db.session.commit()
     myUser=user.query.all()
     userFound = user.query.filter_by(role="Teacher")
     return render_template("teacher.html", data=userFound)
     # return render_template('shwoUser.html',users=myUser,login=userLoginName)

@myApp.route('/update',methods=["POST"])
def updateText():
    userName1=request.form['target_userUpdate']
    userFound=user.query.filter_by(userName=userName1).first()
    userFound.userName=request.form['updateText']
    db.session.commit()
    myUser = user.query.filter_by(userName=userFound.userName).first()
    if myUser.role=="Student":
        return render_template('OnlyForStudent.html', data={myUser})
    elif myUser.role=="Teacher":
        return render_template('OnlyForTeacher.html', data={myUser})

@myApp.route('/updateEmail',methods=["POST"])
def updateEmail1():
    Email=request.form['target_userUpdateEmail1']
    userFound=user.query.filter_by(userName=Email).first()
    userFound.email=request.form['updateEmail12']
    db.session.commit()
    myUser = user.query.filter_by(email=userFound.email).first()
    if myUser.role=="Student":
        return render_template('OnlyForStudent.html', data={myUser})
    elif myUser.role=="Teacher":
        return render_template('OnlyForTeacher.html', data={myUser})


if __name__=="__main__":
    # myApp.run(debug=True)
    socketio.run(myApp,debug=True)